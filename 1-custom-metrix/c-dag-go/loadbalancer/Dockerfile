# 1. 빌드 단계
FROM golang:1.20-alpine AS builder
WORKDIR /app

# 소스 파일 복사
COPY loadbalancer.go .

# 정적 바이너리 빌드를 위해 CGO_ENABLED=0 옵션 추가
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o loadbalancer loadbalancer.go

# 2. 최종 실행 단계
FROM alpine:latest
WORKDIR /app

# curl 설치 (컨테이너 내부에서 테스트용)
RUN apk add --no-cache curl

# 빌드된 바이너리와 원본 소스 복사
COPY --from=builder /app/loadbalancer .

# 포트 노출
EXPOSE 11000

# 컨테이너 실행 시 loadbalancer 실행
CMD ["./loadbalancer"]
