from fastapi import FastAPI

app = FastAPI() # FastAPI() 객체 호출

@app.get("/")  # GET(READ)/POST(CREATE(write))/PUSH(UPDATE)/DELETE
def root(): 
    return {"message":"hello"}