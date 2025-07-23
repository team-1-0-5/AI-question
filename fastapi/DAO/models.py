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
    user_id = fields.IntField(pk=True)
    file_id = fields.IntField()
    class Meta:
        table = "user_file"


class Speech(Model):
    speech_id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255,null=True)
    begin_time = fields.DatetimeField()

    class Meta:
        table = "speech"


class Create(Model):
    speech_id = fields.IntField()
    user_id = fields.IntField()

    class Meta:
        table = "create_speech"


class SpeechFile(Model):
    speech_id = fields.IntField()
    file_id = fields.IntField()

    class Meta:
        table = "speech_file"


class QuestionUser(Model):
    question_id = fields.IntField(pk=True)
    user_id = fields.IntField()
    user_answer = fields.CharField(max_length=255, null=True)
    class Meta:
        table = "question_user"
        unique_together = ("question_id", "user_id")


# 题库表
class Question(Model):
    question_id = fields.IntField(pk=True)
    options = fields.CharField(max_length=255)
    answer = fields.CharField(max_length=255)
    question = fields.CharField(max_length=255)
    class Meta:
        table = "question"

# allocation（答题分配）
class Allocation(Model):
    user_id = fields.IntField(pk=True)
    question_id = fields.IntField()
    times = fields.DatetimeField()
    class Meta:
        table = "allocation"
        unique_together = ("user_id", "question_id", "times")

# join_speech（听众加入演讲）
class JoinSpeech(Model):
    user_id = fields.IntField(pk=True)
    speech_id = fields.IntField()
    class Meta:
        table = "join_speech"
        unique_together = ("user_id", "speech_id")

# speech_question（演讲题目关联）
class SpeechQuestion(Model):
    speech_id = fields.IntField()
    question_id = fields.IntField()
    class Meta:
        table = "speech_question"
        unique_together = ("question_id",)