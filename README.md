# Cloud Computing — FastAPI 학습 저장소

FastAPI 프레임워크와 Uvicorn 서버를 중심으로, **기초 Web API → Pydantic 데이터 검증 → SQLAlchemy ORM** 순서로 학습한 내용을 정리한 저장소입니다.

| 단계 | 파일 | 내용 |
|---|---|---|
| 1. FastAPI 기초 | `main1.py` ~ `main4.py`, `Part1.http` | 라우팅, HTTP 메서드, 경로/쿼리 파라미터 |
| 2. Pydantic | `pydantic.ipynb` | 타입 힌트, `BaseModel`, `Field()`, 중첩 모델, Validator |
| 3. ORM (SQLAlchemy) | `ORM1.ipynb`, `ORM2.ipynb` | Engine, 트랜잭션, Session, `declarative_base` |

---

## ⚙️ 설치

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install fastapi uvicorn pydantic sqlalchemy
```

노트북(`.ipynb`)은 VS Code의 Jupyter 확장이나 Jupyter Notebook으로 실행합니다.

---

# Part 1. FastAPI 기초

`main1.py` → `main4.py` 순서로 기능이 하나씩 추가되는 구조로 되어 있습니다.

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

# Part 2. Pydantic — 데이터 검증/변환 (`pydantic.ipynb`)

파이썬의 타입 힌트는 강제성이 없지만, FastAPI는 **Pydantic(`BaseModel`)** 을 이용해 서버 측에서 타입 체킹을 엄격하게 수행합니다.

### 타입 힌트
| 분류 | 예시 |
|---|---|
| 단순 타입 | `str`, `int`, `float`, `bool`, `bytes`, `date`, `datetime`, `UUID`, `Decimal`, `Path` |
| 제네릭(컨테이너) 타입 | `list[X]`, `dict[K, V]` |
| BaseModel(중첩 모델) 타입 | `User`, `list[Todo]` |
| Union 타입 | `X \| Y`, `Optional[X]` |
| 정해진 값만 허용 | `Enum`, `Literal` |

### BaseModel
```python
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=20)
    priority: int = Field(ge=1, le=5)
    code: str = Field(pattern=r"^[A-Za-z0-9]+$")
    completed: bool = Field(default=False, description="할 일 완료 여부")
```

- **필수 / 선택 필드**: 기본값이 없으면 필수, 있으면 선택
- **타입 변환**: `"123"` → `123`, `"true"` → `True`, ISO 문자열/Unix timestamp → `datetime` 등 (단, `int` → `str`은 변환되지 않음)
- **`model_validate_json()`**: JSON 형식의 문자열을 바로 파싱해서 검증
- **`Field()`**: 타입 힌트만으로 표현할 수 없는 세부 제약 조건(길이, 범위, 정규식 등)
- **중첩 모델**: 모델 안에 모델(`author: User`), 리스트(`list[Todo]`), 딕셔너리(`dict[str, User]`), 여러 단계 중첩
- **커스텀 Validator**
  - `@field_validator("필드명")`: 단일 필드(또는 여러 필드에 재사용) 검증
  - `@model_validator(mode="before" | "after")`: 여러 필드를 함께 고려하는 검증 (예: 비밀번호 확인, 시작일 < 종료일)
- **`model_validate()` + `from_attributes=True`**: 딕셔너리뿐 아니라 일반 객체(ORM 객체)의 속성에서 값을 읽어 검증/변환

---

# Part 3. ORM — SQLAlchemy (`ORM1.ipynb`, `ORM2.ipynb`)

**ORM(Object-Relational Mapping)**: SQL이 아닌 파이썬 객체의 형태로 데이터베이스를 다룰 수 있게 해주는 기법입니다.
파이썬 클래스는 테이블, 클래스의 인스턴스는 테이블의 행(row)에 대응합니다.

```
FastAPI 코드 (Pydantic BaseModel로 검증)
        ↕
Session (ORM)    : [(1, "우유 사기", 0)] ↔ [Todo(id=1, title="우유 사기", completed=False)]
        ↕
Engine → Pool → Dialect → DBAPI → Database
```

### Engine
```python
from sqlalchemy import create_engine

# dialect+driver://username:password@host:port/database
engine = create_engine("sqlite:///:memory:", echo=True)   # 메모리 DB
engine = create_engine("sqlite:///todos.db")              # 파일 DB
```
- **dialect**: 사용할 DB 종류(SQLite, PostgreSQL, MySQL 등)에 맞는 SQL로 변환
- **pool**: 커넥션 재사용 / **DBAPI**: 실제 DB와 통신하는 드라이버 (SQLite 기본값 `pysqlite`)
- `echo=True`: 실행되는 SQL 문 출력, `echo="debug"`: 조회 결과 행까지 출력

### 트랜잭션 (Connection)
| 방식 | 종류 | 동작 |
|---|---|---|
| `with engine.connect() as conn:` | 명시적 트랜잭션 | `conn.commit()`을 직접 호출, 안 하면 자동 ROLLBACK |
| `with engine.begin() as conn:` | 암묵적 트랜잭션 | 정상 종료 시 자동 COMMIT, 예외 시 자동 ROLLBACK |

```python
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
                 [{"x": 1, "y": 1}, {"x": 2, "y": 4}])

with engine.connect() as conn:
    for row in conn.execute(text("SELECT x, y FROM some_table")):
        print(row.x, row.y)          # 인덱스(row[0]), 속성(row.x), mapping(row._mapping) 방식 모두 가능
```

### Session
- SQL 문을 직접 다룰 때는 **Connection**, ORM 방식으로 다룰 때는 **Session**을 사용
- `with Session(engine) as session:` → `session.add()`, `session.execute()` 후 `session.commit()`
- `with session.begin():` → 블록 종료 시 자동 commit/rollback
- **Unit of Work**: 객체 변경 사항을 모아 두었다가 `commit()` 시점에 SQL(INSERT/UPDATE/DELETE)로 한 번에 반영

### 모델 정의 — `declarative_base`
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String)

Base.metadata.create_all(engine)    # Base에 등록된 모든 테이블을 한 번에 생성
```
- `Base.metadata.tables`: `Base`를 상속한 모델(테이블)이 자동으로 등록되는 장부

### ORM ↔ Pydantic 연결
```python
from pydantic import BaseModel, ConfigDict

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)

TodoOut.model_validate(orm_todo)    # ORM 객체 → 응답용 BaseModel로 검증/변환
```

---

## 🧪 테스트 (Part 1)

`Part1.http` 파일에 각 버전별 요청 예시가 정리되어 있습니다. VS Code의 REST Client 확장 등으로 바로 실행해볼 수 있습니다.

---

## 📚 참고 개념 정리

- **path operation** = path operation decorator(`@app.get(...)`) + path operation function(`def root():`)
- **라우팅(routing)**: 요청을 함수로 연결하는 동작
- **ASGI**: 파이썬 웹 서버(uvicorn)와 웹 애플리케이션(FastAPI) 사이의 통신 규약
- **경로 파라미터 vs 쿼리 파라미터**: 경로 파라미터는 데코레이터 경로(`/todos/{id}`)에 표시, 쿼리 파라미터는 함수 인자로만 전달(`?key=value`)
- **Pydantic**: 타입 힌트를 기준으로 런타임에 데이터를 검증/변환하는 라이브러리
- **ORM**: 클래스 ↔ 테이블, 인스턴스 ↔ 행(row)을 매핑하여 SQL 대신 파이썬 객체로 DB를 다루는 기법
- **트랜잭션**: 모두 성공하거나 모두 실패하는 SQL 묶음 (COMMIT / ROLLBACK)
