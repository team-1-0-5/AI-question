
# AI-question 项目说明

本项目为“AI-question”课设，包含前端 Vue3、后端 FastAPI、AI接口等模块。**目前项目已基本完成，主要业务流程已全部打通，支持完整的讲座、答题、统计、解析等功能。**

---
## 快速启动

1. 进入 `vue/` 目录，安装依赖并启动前端，若未安装npm，请参考npm安装：
   ```sh
   npm install
   npm run dev
   ```
2. 进入 `fastapi/` 目录，配置数据库并启动后端：
   - 参考 fastapi/readme.md 或`后端配置`配置环境及数据库
3. 浏览器访问前端页面 `http://localhost:5173/`，体验完整功能
---

## npm安装
1. 在[官网](https://nodejs.org/en/download/)下载安装
2. 在命令行配置`npm config set registry https://registry.npmjs.org/`

## 后端配置
1. 安装python3.8，并配置环境变量等
2. 安装mysql数据库
3. 安装python库：在本目录下命令行运行 
  - `pip install -r requirements.txt`
4. 在sql中创建数据库`create database ai_question;`
5. 找到本目录下ai_question.sql文件，在命令行中cd到本目录，输入`mysql -u root -p ai_question < ai_question.sql` ，root为你mysql用户名
6. 在config.py中修改root用户的密码
7. 运行`main.py`

## 项目结构

- `vue/`：前端主目录，基于 Vue3 + Vite，包含页面、组件、路由、API 封装等。
- `fastapi/`：后端接口，基于 FastAPI，含数据库模型、接口实现、文件上传、PPT转图片/文字等。
- `BESTTTTT_AI_Q/`：AI接口，提供题目生成、答案解析、文件转文字等功能。
- `README.md`：主项目说明文档。

---


## 主要功能

### 前端（vue/）
- 用户注册、登录、登出
- 讲座创建、文件上传（PPT自动转图片和文字）
- 讲座列表、历史数据、个人中心
- 听众端：加入演讲、实时PPT同步、答题、解析、热力图统计
- 演讲者端：讲座控制、发题、PPT同步、数据统计
- API 封装（`api.js`），所有接口均支持表单方式调用
- 路由守卫、页面跳转、状态管理

### 后端（fastapi/）
- 用户注册、登录、讲座创建、文件上传/下载
- PPT转图片与文字（同步处理，兼容 Windows 环境）
- 题目推送、答题、得分统计、解析
- 数据库模型、接口实现、异常处理

### AI接口（BESTTTTT_AI_Q/）
- 题目生成、答案解析、文件转文本等，已在后端接入

---
项目已基本完成，欢迎体验和反馈！
