// service-d/main.go
package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

type Payload struct {
	Value int    `json:"value"`
	Data  string `json:"data"`
}

const matrixSize = 120

// 전역 변수에 행렬 곱셈 결과를 저장 (동시 요청 고려 시 동기화 필요)
var globalMatrixResult [matrixSize][matrixSize]float64

// matrixMultiply는 50×50 행렬의 곱셈을 실제로 수행합니다.
func matrixMultiply() {
	var a, b, c [matrixSize][matrixSize]float64

	// 행렬 a와 b를 초기화 (예시: a는 i+j, b는 i-j)
	for i := 0; i < matrixSize; i++ {
		for j := 0; j < matrixSize; j++ {
			a[i][j] = float64(i + j)
			b[i][j] = float64(i - j)
		}
	}

	// 행렬 곱셈: c = a * b
	for i := 0; i < matrixSize; i++ {
		for j := 0; j < matrixSize; j++ {
			sum := 0.0
			for k := 0; k < matrixSize; k++ {
				sum += a[i][k] * b[k][j]
			}
			c[i][j] = sum
		}
	}

	globalMatrixResult = c
	log.Printf("Matrix multiplication completed. c[0][0]=%f", c[0][0])
}

// generate1KBData는 prefix를 반복하여 1KB(1024바이트) 문자열을 생성합니다.
func generate1KBData(prefix string) string {
	return strings.Repeat(prefix, 1024)
}

func calHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed in Service E", http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	var payload Payload
	if err := json.Unmarshal(body, &payload); err != nil {
		http.Error(w, "Error parsing JSON", http.StatusBadRequest)
		return
	}
	log.Printf("Service E received: value=%d, data size=%d", payload.Value, len(payload.Data))

	// 실제 행렬 곱셈 수행
	matrixMultiply()

	// 최종 처리: value를 1 증가시키고 'D' 접두사를 사용한 1KB 문자열 생성
	finalPayload := Payload{
		Value: payload.Value + 1,
		Data:  generate1KBData("E"),
	}

	log.Printf("Service E final processing done. Final value: %d", finalPayload.Value)

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
		port = "11005"
	}
	http.HandleFunc("/cal", calHandler)
	log.Printf("Service E is running on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
