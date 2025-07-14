import uvicorn
from fastapi import FastAPI, Body, Header, Form

app = FastAPI()


@app.get("/")
def index():
    """测试"""
    return "asdasdasdasdad"


@app.get("/json")
def json():
    return {"name": "99922", "code": "asss"}


@app.get("/test2/{id}")
def test2(id):
    return "id:" + id


@app.get("/test3")
def test3(id):
    """查询字符串的方式（?id=8）"""
    return "id:" + id


@app.post("/login")
def login(data=Body(None)):
    print(data)
    return data


@app.post("/login2")
def login2(username=Form(None), pw=Form(None)):
    return {"username": username, "password": pw}


if __name__ == '__main__':
    uvicorn.run(app)
