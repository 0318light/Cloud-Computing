from fastapi import FastAPI
from typing import Optional

app = FastAPI()

todos = [
    {"id": 1, "title": "우유 사기", "completed": False, "tags": ["장보기"]},
    {"id": 2, "title": "책 반납하기", "completed": True, "tags": ["긴급"]},
    {"id": 3, "title": "빨래하기", "completed": False, "tags": ["집안일", "긴급"]},
]


# 쿼리 파라미터가 있는 요청
# 쿼리 파라미터는 ?로 시작
# GET http://127.0.0.1:8000/todos?completed=true 에서 ?completed=true
# ?completed=true의
# completed는 파라미터, true는 값

# 경로 파라미터는 데코레이터의 경로에 표시하지만 쿼리 파라미터는 데코레이어의 경로에 표시하지 않고 함수의 매개변수로만 전달
# @app.get("/todos/{id}")
# GET /todos/1                              <----- 경로 파라미터
# def get_todo(id: int):
#   ...
# @app.get("/todos")
# GET /todos?completed=true                 <----- 쿼리 파라미터
# def get_todos(completed: bool = None):
#   ...


@app.get("/todos")
# GET http://127.0.0.1:8000/todos
# GET http://127.0.0.1:8000/todos?completed=true
# GET http://127.0.0.1:8000/todos?completed=false
def get_todos(completed: Optional[bool] = None):
    # completed: Optional[bool] = None에서
    # Optional[bool]는 Union[bool, None]와 동일 == bool | None
    # 의미는 "bool이거나 None"
    #  = None 이 부분은 값이 전달되지 않으면 디폴트 값은 None이라는 의미

    # 함수 get_todos()의 파라미터 completed는 경로 파라미터가 아님 → 경로에 {completed} 형태로 없음
    # 경로에는 없는데 단순 타입이면 쿼리 파라미터
    # 나머지 경우는 이후에 설명 (BaseModel을 상속한 Pydantic 클래스)
    if completed is None: # GET http://127.0.0.1:8000/todos
        return todos
    return [todo for todo in todos if todo["completed"] == completed]
    # 전달받은 completed에 해당하는 것만 선택


# 여러 개의 쿼리 파라미터
@app.get("/todos/search")
# GET http://127.0.0.1:8000/todos/search?completed=true&title=우유
def search_todos(completed: Optional[bool] = None, title: Optional[str] = None):
    result = todos      # 아래 if 문에 해당이 모두 안될 경우 리턴할 result
    if completed is not None:
        result = [todo for todo in result if todo["completed"] == completed]
    if title is not None:
        result = [todo for todo in result if title in todo["title"]]
    return result

# 기본값이 있는 필수/선택 쿼리 파라미터
@app.get("/todos/page")
# GET http://127.0.0.1:8000/todos/page
# GET http://127.0.0.1:8000/todos/page?page=2
# GET http://127.0.0.1:8000/todos/page?page=2&size=1

# 쿼리 파라미터를 안 보내도 에러 없이 기본값으로 동작하는 이유는
# 쿼리 파라미터가 함수 파라미터로 전달되고 기본 값이 지정되어 있기 때문
def get_todos_page(page: int = 1, size: int = 10):
    # pagination: 전체 데이터를 나누어서 전달하는 방식
    start = (page - 1) * size   # todos는 파이썬 리스트라서 시작 인덱스는 0
    end = start + size          # size만큼
    return todos[start:end]

# 필수 쿼리 파라미터
@app.get("/todos/keyword")
# GET http://127.0.0.1:8000/todos/keyword?keyword=우유  → 정상 동작
# GET http://127.0.0.1:8000/todos/keyword               → keyword 없음, 422 에러 발생
def get_todos_by_keyword(keyword: str):
    # keyword 파라미터는 기본 값이 없으므로 값을 반드시 전달해야 함
    # 따라서 keyword는 필수 쿼리 파라미터가 되는 것
    return [todo for todo in todos if keyword in todo["title"]]

# 쿼리 파라미터를 반복해서 요청으로 전달하면 내부에서 리스트 형태로 처리
from typing import List
from fastapi import Query

# 리스트 형태로 쿼리 파라미터를 받아서 처리해야 하는 경우에 해당하는 예제
@app.get("/todos/tags")
# GET http://127.0.0.1:8000/todos/tags?tags=긴급
# GET http://127.0.0.1:8000/todos/tags?tags=긴급&tags=집안일
# 쿼리 파라미터 tags를 한번 또는 여러번 사용

def get_todos_by_tags(tags: List[str] = Query(default=[])):
    # tags: List[str] → tags 쿼리 파라미터 타입은 문자열 리스트 → tags 파라미터는 여러 번 반복 사용됨을 알려줌
    # = Query(default=[])에서 Query()는 placeholder 객체
    # placeholder 객체는 자리를 맡아두는 역할
    # 이 자리에는 쿼리 파라미터가 올 것이고 일단 빈 리스트로 시작합니다~

    if not tags:    # tags가 비어 있는 리스트이면
        return todos
    return [todo for todo in todos if any(tag in todo["tags"] for tag in tags)]
    #                                     -------------------
    #                                     "긴급" in ["장보기"], "집안일" in ["장보기"]
    #                                     "긴급" in ["긴급"], "집안일" in ["긴급"]
    #                                     "긴급" in ["집안일", "긴급"], "집안일" in ["집안일", "긴급"]
    
    # 1.
    # 조건 if any(tag in todo["tags"] for tag in tags)을 만족하면
    # [todo for todo in todos]를 실행하는 것

    # 2.
    # GET http://127.0.0.1:8000/todos/tags?tags=긴급&tags=집안일
    # 이 경우 tags는 ["긴급", "집안일"]

    # 3. 
    # todos = [
    #     {"id": 1, "title": "우유 사기", "completed": False, "tags": ["장보기"]},
    #     {"id": 2, "title": "책 반납하기", "completed": True, "tags": ["긴급"]},
    #     {"id": 3, "title": "빨래하기", "completed": False, "tags": ["집안일", "긴급"]},
    # ]
    # 의 각각의 항목에 대해서 tags 필드에 tags가 포함되어 있으면 추가