// service-a/main.go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

type Payload struct {
	Value int    `json:"value"`
	Data  string `json:"data"`
}

var globalMatrixResult [150][150]float64

// matrixMultiply: 200×200 행렬곱셈을 실제로 수행합니다.
func matrixMultiply() {
	const size = 150
	var a, b, c [size][size]float64
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			a[i][j] = float64(i + j)
			b[i][j] = float64(i - j)
		}
	}
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			sum := 0.0
			for k := 0; k < size; k++ {
				sum += a[i][k] * b[k][j]
			}
			c[i][j] = sum
		}
	}
	globalMatrixResult = c
}

// generate1KBData 생성: prefix를 반복하여 1KB 문자열을 만듭니다.
func generate1KBData(prefix string) string {
	return strings.Repeat(prefix, 1024)
}

// forwardRequest: 지정 URL로 POST 요청을 보내고 응답 payload를 반환합니다.
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

func calHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed in Service A", http.StatusMethodNotAllowed)
		return
	}
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body in Service A", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()
	var payload Payload
	if err := json.Unmarshal(body, &payload); err != nil {
		http.Error(w, "Error parsing JSON in Service A", http.StatusBadRequest)
		return
	}
	log.Printf("Service A received: value=%d, data size=%d", payload.Value, len(payload.Data))

	// 실제 연산 수행
	matrixMultiply()

	// Service A의 처리: value 증가 및 'A' 접두사를 사용
	newPayload := Payload{
		Value: payload.Value + 1,
		Data:  generate1KBData("A"),
	}

	// 다음 서비스(B) URL (환경변수 NEXT_SERVICE_URL로 재정의 가능)
	nextServiceURL := os.Getenv("NEXT_SERVICE_URL")
	if nextServiceURL == "" {
		nextServiceURL = "http://service-b.heart.svc.cluster.local:11002/cal"
	}

	// Service B로 전달하고 응답받기
	finalPayload, err := forwardRequest(nextServiceURL, newPayload)
	if err != nil {
		log.Printf("Service A error forwarding to Service B: %v", err)
		http.Error(w, "Error forwarding request in Service A", http.StatusInternalServerError)
		return
	}
	log.Printf("Service A received final payload: %+v", finalPayload)

	responseBytes, err := json.Marshal(finalPayload)
	if err != nil {
		http.Error(w, "Error generating response in Service A", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(responseBytes)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "11001"
	}
	http.HandleFunc("/cal", calHandler)
	log.Printf("Service A is running on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
