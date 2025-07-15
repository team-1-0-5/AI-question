import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from DAO.models import User

app = FastAPI()

#数据库绑定
register_tortoise(
    app,
    db_url="mysql://root:root@localhost:3306/ai_question",
    modules={"models": ['DAO.models']},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.get("/")
async def index():
    users = await User.all()
    return users


if __name__ == '__main__':
    uvicorn.run(app)
