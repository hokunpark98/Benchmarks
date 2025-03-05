package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

func main() {
	// PORT 환경변수에서 포트를 읽어오고, 없으면 기본값 11000 사용
	port := "11000" // 또는 os.Getenv("PORT")로 읽어올 수 있습니다.

	// 포워딩할 대상 URL 파싱
	targetURL, err := url.Parse("http://productpage.heart.svc.cluster.local:9080/productpage")
	if err != nil {
		log.Fatalf("Error parsing target URL: %v", err)
	}

	// ReverseProxy 생성 (단일 호스트 대상)
	proxy := httputil.NewSingleHostReverseProxy(targetURL)

	// 기존 Director를 감싸서 요청 URL 경로를 정확히 targetURL의 경로로 설정
	originalDirector := proxy.Director
	proxy.Director = func(req *http.Request) {
		originalDirector(req)
		// 요청 URL 경로를 백엔드가 원하는 정확한 경로로 설정 (trailing slash 없음)
		req.URL.Path = targetURL.Path
	}

	// "/run" 요청에 대해 proxy가 대상 URL로 포워딩하도록 핸들러 등록
	http.HandleFunc("/run", func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received /run request; forwarding to %s", targetURL.String())
		proxy.ServeHTTP(w, r)
	})

	log.Printf("Server is listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
