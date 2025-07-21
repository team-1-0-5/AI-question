DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # 根据实际数据库类型修改
            "credentials": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "root",
                "database": "ai_question",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["__main__","speaker"],  # 指向当前模块的模型
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "UTC"
}