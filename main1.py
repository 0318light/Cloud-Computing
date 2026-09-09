from fastapi import FastAPI

app = FastAPI()
# FastAPI 애플리케이션 객체를 생성

# @app.get("/") --- 데코레이터
# def root():   --- 함수
#     return {"message": "hello"}


@app.get("/")
# 요청은 ⓐ 어떤 http 메서드로, ⓑ 어떤 데이터를 실어서, ⓒ 어떤 URL에 접근하는가의 세 부분으로 구성
# ⓑ 데이터에는 경로, 쿼리, body, header가 해당

# GET 메서드 + / 요청이 들어오면 아래 함수를 호출하라는 의미
def root():
    return {"message": "hello"}
# 이 둘을 묶어서 path operation이라고 함

# 1.
# path operation → path operation decorator + path operation function
# @app.get("/") : path operation decorator
# 함수에 붙여 놓은 이름표로서 "나는 이런 요청을 담당하는 함수야"가 내용

# 2.
# def root(): : path operation function

# -----------------------------------------------------------------------------------------

# 실행
# uvicorn main1:app --reload
# main1.py 파일 안의 FastAPI() 객체 app를 uvicorn 서버로 실행
# --reload: 코드가 수정되어 저장될 때마다 서버를 자동으로 재시작하는 개발용 옵션

# FastAPI() 객체는 ASGI 애플리케이션
# ASGI (Asynchronous Server Gateway Interface)는 파이썬 웹 서버와 웹 애플리케이션 사이의 통신 규약(인터페이스)

# 사용자 >>> 요청 >>> 파이썬 웹 서버 (uvicorn) >>> 요청 >>> 웹 애플리케이션 (FastAPI 인스턴스)
# 사용자 <<< 응답 <<< 파이썬 웹 서버 (uvicorn) <<< 응답 <<< 웹 애플리케이션 (FastAPI 인스턴스)
# 요청과 응답이 ASGI에서 정한 형식으로 이루어짐을 의미

# 파이썬 웹 서버: 네트워크 포트를 열고, 클라이언트의 TCP/HTTP 연결을 받고, HTTP 프로토콜을 해석하는 역할 → 창구 역할
# 웹 애플리케이션: 어떤 경로에 어떤 요청이 오면 어떤 함수를 실행하고 어떤 응답을 만들지를 정의한 로직 → 창구 건너 담당 직원

# 웹 애플리케이션과 path operation은 포함관계
# FastAPI() 인스턴스 내에 여러 개의 path operation이 있는 형태