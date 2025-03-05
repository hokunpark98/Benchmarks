// service-b/main.go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"time"
)

type Payload struct {
	Value int    `json:"value"`
	Data  string `json:"data"`
}

var globalMatrixResult [50][50]float64

func matrixMultiply() {
	const size = 50
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

func generate1KBData(prefix string) string {
	return strings.Repeat(prefix, 1)
}

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
		http.Error(w, "Method Not Allowed in Service B", http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body in Service B", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	var payload Payload
	if err := json.Unmarshal(body, &payload); err != nil {
		http.Error(w, "Error parsing JSON in Service B", http.StatusBadRequest)
		return
	}

	log.Printf("Service B received: value=%d, data size=%d", payload.Value, len(payload.Data))

	// 계산 작업
	matrixMultiply()

	// 새로 전달할 Payload
	newPayload := Payload{
		Value: payload.Value + 1,
		Data:  generate1KBData("B"),
	}

	// 0.5 확률로 nextServiceURL 혹은 service-e로 요청 보내기
	var destinationURL string
	if rand.Float64() < 0.5 {
		destinationURL = "http://service-c.heart.svc.cluster.local:11003/cal"
		log.Printf("Service B: Forwarding to Service C -> %s", destinationURL)
	} else {
		destinationURL = "http://service-e.heart.svc.cluster.local:11005/cal"
		log.Printf("Service B: Forwarding to Service E -> %s", destinationURL)
	}

	finalPayload, err := forwardRequest(destinationURL, newPayload)
	if err != nil {
		log.Printf("Service B error forwarding: %v", err)
		http.Error(w, "Error forwarding request in Service B", http.StatusInternalServerError)
		return
	}

	log.Printf("Service B received final payload: %+v", finalPayload)

	responseBytes, err := json.Marshal(finalPayload)
	if err != nil {
		http.Error(w, "Error generating response in Service B", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(responseBytes)
}

func main() {
	// 랜덤 시드 초기화 (한 번만 실행)
	rand.Seed(time.Now().UnixNano())

	port := os.Getenv("PORT")
	if port == "" {
		port = "11002"
	}
	http.HandleFunc("/cal", calHandler)
	log.Printf("Service B is running on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
