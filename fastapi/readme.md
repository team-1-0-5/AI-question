# 环境配置
1. 安装python3.8，并配置环境变量等
2. 安装mysql数据库
3. 安装python库：在命令行运行 
  - `pip install asyncmy`
  - `pip install tortoise-orm`
  - `pip install fastapi "uvicorn[standard]" pydantic`
4. 在sql中创建数据库`create database ai_question;`
5. 找到本目录下ai_question.sql文件，在命令行中cd到本目录，输入`mysql -u root -p ai_question < ai_question.sql` ，root为你mysql用户名
6. 在config.py中修改root用户的密码
7. 运行`file.py`