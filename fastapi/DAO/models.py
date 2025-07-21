from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    user_type = fields.IntField()


class File(Model):
    file_id = fields.IntField(pk=True)
    file_address = fields.CharField(max_length=255)
    file_type = fields.CharField(max_length=20)

    class Meta:
        table = "file"


class UserFile(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    file = fields.ForeignKeyField('models.File', related_name='user_files')

    class Meta:
        table = "user_file"


class Speech(Model):
    speech_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    begin_time = fields.DatetimeField()

    class Meta:
        table = "speech"
