from tortoise import Model, fields


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    user_type = fields.IntField()

    class Meta:
        table = "user"


class File(Model):
    file_id = fields.IntField(pk=True)
    file_address = fields.CharField(max_length=255)
    file_type = fields.CharField(max_length=20)

    class Meta:
        table = "file"


class UserFile(Model):
    user_id = fields.IntField()
    file_id = fields.IntField()

    class Meta:
        table = "user_file"


class Speech(Model):
    speech_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, null=True)
    begin_time = fields.DatetimeField()
    state = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "speech"


class Create(Model):
    speech_id = fields.IntField(pk=True)
    user_id = fields.IntField()

    class Meta:
        table = "create_speech"


class SpeechFile(Model):
    speech_id = fields.IntField()
    file_id = fields.IntField(pk=True)

    class Meta:
        table = "speech_file"


class JoinSpeech(Model):
    speech_id = fields.IntField()
    user_id = fields.IntField()

    class Meta:
        table = "join_speech"
        unique_together = ("speech_id", "user_id")
