from fastapi import FastAPI

app = FastAPI()

todos = [
    {"id": 1, "title": "우유 사기", "completed": False},
    {"id": 2, "title": "책 반납하기", "completed": True},
    {"id": 3, "title": "빨래하기", "completed": False},
]

@app.get("/")
# GET http://127.0.0.1:8000/
def root():
    return {"message": "hello"}

@app.get("/todos")
# GET http://127.0.0.1:8000/todos
def get_todos():
    return todos

# 경로 파라미터 - 와일드 카드 (*)
@app.get("/todos/{id}")     # {} 부분은 경로 파라미터
# GET http://127.0.0.1:8000/todos/1
# GET http://127.0.0.1:8000/todos/99
# GET http://127.0.0.1:8000/todos/abc
def get_todo(id: int):
    # 매개변수 이름과 경로 파라미터 이름이 동일해야 맵핑이 됨
    # id의 타입을 int로 명시했으므로 FastAPI가 타입 검증과 에러 응답 생성을 자동으로 수행
    # 요청은 서버에 도달했지만 서버가 기대하는 형식/타입/조건과 다를 때 "422 Unprocessable Content" 에러가 발생
    # id의 타입을 명시하지 않으면 아무 일도 일어나지 않음 (타입 검증이나 자동 변환을 하지 않는다는 의미)
    for todo in todos:
        if todo["id"] == id:
            return todo
    return {"error": "찾을 수 없습니다"}

# POST는 생성, PUT은 수정
# POST의 경우 BODY는 반드시 전달해야 하는 것은 아니지만
# 생성의 목적이기 때문에 생성에 필요한 데이터를 함께 전달
@app.post("/todos")
# POST http://127.0.0.1:8000/todos
# Content-Type: application/json -------> "HTTP 요청 헤더이며 보내는 요청 본문(body)의 데이터 형식이 JSON"
# 
# {
#   "title": "우유 사기",
#   "completed": false
# }
def create_todo():
    return {"method": "POST", "message": "할 일을 생성합니다"}

# 경로 파라미터 + 수정
# PUT의 경우 BODY는 반드시 전달해야 하는 것은 아니지만
# 수정의 목적이기 때문에 수정에 필요한 데이터를 함께 전달
@app.put("/todos/{id}")
# PUT http://127.0.0.1:8000/todos/2
# Content-Type: application/json
# 
# {
#   "title": "우유와 빵 사기",
#   "completed": true
# }
def update_todo(id: int):
    return {"id": id, "method": "PUT", "message": "할 일을 수정합니다"}

# 경로 파라미터 + 삭제
@app.delete("/todos/{id}")
# DELETE http://127.0.0.1:8000/todos/3
def delete_todo(id: int):
    return {"id": id, "method": "DELETE", "message": "할 일을 삭제합니다"}