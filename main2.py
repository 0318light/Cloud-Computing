from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello"}
# 라우팅 (routing)은 "요청을 함수로 연결하는 동작"
# GET 메서드로 "/" 경로에 요청이 들어오면 → root() 함수를 실행 → {"message": "hello"}를 응답으로 반환
# ------------------------라우팅-------------------------



# 사용자 >>> 요청 >>> 파이썬 웹 서버 (uvicorn) >>> 요청 >>> 웹 애플리케이션 (FastAPI 인스턴스)
# ----------------- 요청을 보내서 테스트

# 1.
# curl

# 2.
# .http 파일

# 3.
# http://127.0.0.1:8000/docs


# 같은 경로("/todos")라도 메서드가 다르면 다른 요청이 되고 다른 함수로 라우팅
@app.get("/todos")
def get_todos():
    return {"method": "GET", "message": "할 일 목록을 조회합니다"}

@app.post("/todos")
def create_todo():
    return {"method": "POST", "message": "할 일을 생성합니다"}

@app.put("/todos")
def update_todo():
    return {"method": "PUT", "message": "할 일을 수정합니다"}

@app.delete("/todos")
def delete_todo():
    return {"method": "DELETE", "message": "할 일을 삭제합니다"}