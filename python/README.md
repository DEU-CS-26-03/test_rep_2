# Virtual Try-On — Python AI API Server

FastAPI 기반 가상 피팅 AI 추론 서버. CatVTON 모델을 사용하며 Mock / Real 모드 전환을 지원한다.

---

## 기술 스택

| 항목 | 내용 |
|---|---|
| Language | Python 3.10+ |
| Framework | FastAPI 0.115.0 / Uvicorn 0.30.0 |
| AI Model | CatVTON (ICLR 2025) |
| 실행 모드 | Mock / Real 전환 가능 |

---

## 디렉토리 구조

python/<br>
├── app/<br>
│ ├── main.py<br>
│ ├── core/ # 설정, 상수<br>
│ ├── routers/ # API 엔드포인트<br>
│ ├── schemas/ # 요청/응답 모델<br>
│ ├── services/ # 비즈니스 로직<br>
│ └── repositories/ # 인메모리 저장소<br>
├── vton/<br>
│ └── catvton_runner.py # CatVTON 추론 실행부<br>
├── workspace/<br>
│ ├── uploads/ # 업로드 파일<br>
│ ├── results/ # 추론 결과<br>
│ └── temp/<br>
├── mock/<br>
│ └── mock_result.jpg<br>
├── Dockerfile<br>
└── requirements.txt<br>


---

## 실행

```bash
# 1. 환경변수 설정
cp .env.example .env

# 2. 의존성 설치
cd python
pip install -r requirements.txt

# 3. 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Swagger UI
http://localhost:8000/docs
```
---
## API 목록
| 메서드  | 경로                | 설명                 |
| ---- | ----------------- | ------------------ |
| GET  | /health           | 서버 상태              |
| GET  | /models/status    | 모델 상태              |
| POST | /user-images      | 사용자 사진 업로드         |
| GET  | /user-images/{id} | 사용자 사진 조회          |
| POST | /garments         | 상의 이미지 업로드         |
| GET  | /garments/{id}    | 상의 이미지 조회          |
| POST | /tryons           | 피팅 작업 생성           |
| GET  | /tryons/{id}      | 작업 상태 조회 (polling) |
| GET  | /results/{id}     | 결과 이미지 조회          |

## 피팅 흐름

```text
POST /user-images  →  POST /garments  →  POST /tryons
→  GET /tryons/:id (polling, status: completed 확인)
→  GET /results/:id
```
### 작업 상태값
```queued → processing → completed / failed```

### Mock/Real 모드
.env 파일의 USE_MOCK 값으로 전환한다.

| 항목     | USE_MOCK=true    | USE_MOCK=false |
| ------ | ---------------- | -------------- |
| AI 추론  | 생략 (mock 이미지 반환) | CatVTON 실제 실행  |
| GPU 필요 | ❌                | ✅ CUDA 8GB+    |
| 용도     | 개발 / 프론트 연동 테스트  | 실제 데모 시연       |
Real 모드 전환 시 vton/catvton_runner.py 의 run_catvton() 에 추론 코드를 삽입한다.

### CatVTON 최소 추론 환경
| GPU VRAM | RAM             | CUDA  | 해상도        |
| -------- | --------------- | ----- | ---------- |
| 8GB 이상   | 16GB+ (32GB 권장) | 11.x+ | 1024 × 768 |

---

## 제약 사항 (1차 MVP)
- 로그인/인증 없음
- 상의(top) / 정면 사진만 지원
- 동시 1개 작업만 처리
- 인메모리 저장 (재시작 시 초기화)

## Docker 실행
```bash
docker-compose up --build
```
```text
undefined
```
