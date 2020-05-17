from django.contrib.auth.models import User
from djongo import models

from howru_helpers import UTCTime


class Patient(models.Model):
    identifier = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100, null=True)
    #picture = models.ImageField()
    picture = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=1, null=True)
    language = models.CharField(choices=[("GB", "English"), ("ES", "Spanish")], max_length=2)
    username = models.CharField(max_length=20, null=True)
    _schedule = models.DateTimeField(
        db_column="schedule"
    )
    @property
    def schedule(self):
        return self._schedule
    @schedule.setter
    def schedule(self, value):
        utc_result = UTCTime.get_utc_result(value)
        self._schedule = utc_result


class Question(models.Model):
    identifier = models.ObjectIdField()
    responses = models.TextField()
    text = models.CharField(max_length=100)
    creator_id = models.CharField(max_length=100)
    public = models.BooleanField()
    language = models.CharField(choices=[("GB", "English"), ("ES", "Spanish")], max_length=2)


class JournalEntry(models.Model):
    question_id = models.GenericObjectIdField()
    patient_id = models.CharField(max_length=10)
    doctor_id = models.GenericObjectIdField()
    class Meta:
        abstract = True


class PendingQuestion(JournalEntry):
    answering = models.BooleanField()


class AnsweredQuestion(JournalEntry):
    answer_date = models.DateTimeField()
    response = models.CharField(max_length=100)
