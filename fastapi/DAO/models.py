from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    user_type = fields.IntField()
