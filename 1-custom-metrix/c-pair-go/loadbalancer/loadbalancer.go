// loadbalancer/main.go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

// Payload는 체인 전체에서 사용하는 데이터 구조체입니다.
type Payload struct {
	Value int    `json:"value"`
	Data  string `json:"data"`
}

// generate1KBData는 prefix를 반복하여 1KB 문자열을 생성합니다.
func generate1KBData(prefix string) string {
	return strings.Repeat(prefix, 1)
}

// forwardRequest는 지정된 URL로 POST 요청을 보내고, 응답 payload를 반환합니다.
func forwardRequest(url string, payload Payload) (Payload, error) {
	jsonData, err := json.Marshal(payload)
	if err != nil {
		return Payload{}, err
	}
	client := &http.Client{Timeout: 5 * time.Second}
	req, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(jsonData))
	if err != nil {
		return Payload{}, err
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		return Payload{}, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		return Payload{}, fmt.Errorf("received status code %d: %s", resp.StatusCode, string(body))
	}
	respBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return Payload{}, err
	}
	var respPayload Payload
	if err := json.Unmarshal(respBytes, &respPayload); err != nil {
		return Payload{}, err
	}
	return respPayload, nil
}

// calHandler는 GET 요청을 받아 Service A로 payload를 전달하고 최종 결과를 반환합니다.
func calHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	// 쿼리 파라미터 "value" 읽기
	log.Println("RawQuery:", r.URL.RawQuery)
	valueStr := r.URL.Query().Get("value")
	log.Println("Parsed valueStr:", valueStr)
	if valueStr == "" {
		http.Error(w, "loadbalancer Missing 'value' query parameter", http.StatusBadRequest)
		return
	}
	value, err := strconv.Atoi(valueStr)
	if err != nil {
		http.Error(w, "Invalid 'value' query parameter", http.StatusBadRequest)
		return
	}

	// 초기 payload 생성 (여기서는 'L' 접두사 사용)
	initialPayload := Payload{
		Value: value,
		Data:  generate1KBData("L"),
	}

	// SERVICE_A_URL 환경변수가 없으면 기본값 사용
	serviceAURL := os.Getenv("SERVICE_A_URL")
	if serviceAURL == "" {
		serviceAURL = "http://service-a.heart.svc.cluster.local:11001/cal"
	}

	// Service A로 POST 요청 전송 후 최종 응답 받기
	finalPayload, err := forwardRequest(serviceAURL, initialPayload)
	if err != nil {
		log.Printf("Error forwarding to service-a: %v", err)
		http.Error(w, "Error forwarding request", http.StatusInternalServerError)
		return
	}
	log.Printf("Final payload received from chain: %+v", finalPayload)

	// 최종 결과를 클라이언트에 반환
	responseBytes, err := json.Marshal(finalPayload)
	if err != nil {
		http.Error(w, "Error generating response", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(responseBytes)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "11000"
	}
	http.HandleFunc("/cal", calHandler)
	log.Printf("Loadbalancer service is listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
