# FastAPI Quickstart Project

FastAPI 프레임워크와 Uvicorn 서버를 활용하여 만든 기초 Web API 학습 프로젝트입니다.
`main1.py` → `main4.py` 순서로 기능이 하나씩 추가되는 구조로 되어 있습니다.

---

## 📌 실행 방법

```bash
uvicorn main1:app --reload
```

- 파일명에 따라 `main1`, `main2`, `main3`, `main4`로 바꿔서 실행하면 됩니다.
- `--reload`: 코드 저장 시 서버 자동 재시작 (개발용 옵션)
- 요청 테스트는 `.http` 파일(Part1.http) 또는 `http://127.0.0.1:8000/docs`(Swagger UI)로 가능합니다.

---

## 📁 main1.py — 기본 라우팅

FastAPI의 가장 기본 단위인 **path operation**(데코레이터 + 함수)을 다룹니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello"}
```

- `app = FastAPI()`: ASGI 애플리케이션 객체 생성
- `@app.get("/")`: GET + `/` 요청이 들어오면 아래 함수를 호출하라는 의미의 데코레이터
- 요청은 **메서드 + 데이터(경로/쿼리/body/header) + URL**로 구성됨

---

## 📁 main2.py — HTTP 메서드별 라우팅 (CRUD)

같은 경로라도 메서드가 다르면 다른 함수로 라우팅되는 것을 보여줍니다.

```python
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
```

| 메서드 | 의미 |
|---|---|
| GET | 조회 (READ) |
| POST | 생성 (CREATE) |
| PUT | 수정 (UPDATE) |
| DELETE | 삭제 (DELETE) |

---

## 📁 main3.py — 실제 데이터 + 경로 파라미터

메모리 리스트(`todos`)를 두고, 실제로 데이터를 조회/수정하는 로직을 추가합니다.

```python
todos = [
    {"id": 1, "title": "우유 사기", "completed": False},
    {"id": 2, "title": "책 반납하기", "completed": True},
    {"id": 3, "title": "빨래하기", "completed": False},
]

@app.get("/todos/{id}")
def get_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo
    return {"error": "찾을 수 없습니다"}
```

- **경로 파라미터**: `{id}` 형태로 URL에 값을 직접 실어 전달
- 타입을 `int`로 명시하면 FastAPI가 자동으로 타입 검증 + 에러 응답(422) 생성

---

## 📁 main4.py — 쿼리 파라미터, 검색, 페이지네이션

가장 확장된 버전으로, 다양한 **쿼리 파라미터** 처리 패턴을 다룹니다.

```python
from typing import Optional, List
from fastapi import Query

@app.get("/todos")
def get_todos(completed: Optional[bool] = None):
    if completed is None:
        return todos
    return [todo for todo in todos if todo["completed"] == completed]

@app.get("/todos/search")
def search_todos(completed: Optional[bool] = None, title: Optional[str] = None):
    ...

@app.get("/todos/page")
def get_todos_page(page: int = 1, size: int = 10):
    ...

@app.get("/todos/keyword")
def get_todos_by_keyword(keyword: str):
    ...

@app.get("/todos/tags")
def get_todos_by_tags(tags: List[str] = Query(default=[])):
    ...
```

| 기능 | 설명 |
|---|---|
| 선택적 필터링 | `?completed=true` 같은 옵션 쿼리 파라미터 |
| 복합 검색 | `completed` + `title` 동시 조건 검색 |
| 페이지네이션 | `page`, `size` 파라미터로 데이터 나눠서 응답 |
| 필수 쿼리 파라미터 | 값이 없으면 422 에러 (예: `keyword`) |
| 리스트형 쿼리 파라미터 | `tags=긴급&tags=집안일`처럼 반복 전달 → 리스트로 처리 |

---

## 🧪 테스트

`Part1.http` 파일에 각 버전별 요청 예시가 정리되어 있습니다. VS Code의 REST Client 확장 등으로 바로 실행해볼 수 있습니다.

---

## 📚 참고 개념 정리

- **path operation** = path operation decorator(`@app.get(...)`) + path operation function(`def root():`)
- **라우팅(routing)**: 요청을 함수로 연결하는 동작
- **ASGI**: 파이썬 웹 서버(uvicorn)와 웹 애플리케이션(FastAPI) 사이의 통신 규약
- **경로 파라미터 vs 쿼리 파라미터**: 경로 파라미터는 데코레이터 경로(`/todos/{id}`)에 표시, 쿼리 파라미터는 함수 인자로만 전달(`?key=value`)
