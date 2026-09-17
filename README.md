# FastAPI Quickstart Project

FastAPI 프레임워크와 Uvicorn 서버를 활용하여 만든 기초 Web API 프로젝트입니다.

---

## 📌 코드 구성 및 역할

```python
from fastapi import FastAPI

app = FastAPI() # FastAPI 객체 생성 (통신 규칙 및 경로 관리)

@app.get("/")   # GET (READ): 루트 경로('/')로 들어오는 요청 감지
def root():     # 요청 발생 시 실행될 응답 처리 함수
    return {"message": "hello"}  # JSON 형태로 클라이언트에 응답 전달
