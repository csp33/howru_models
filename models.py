from django.contrib.auth.models import User
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models

from howru_helpers import UTCTime


class Patient(models.Model):
    identifier = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100, null=True)
    # picture = models.ImageField()
    picture = models.CharField(max_length=100, null=True)
    _gender = models.CharField(choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], max_length=1,
                               db_column="gender", null=True)
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

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if value in ["Masculino", "Male"]:
            gender = "M"
        elif value in ["Femenino", "Female"]:
            gender = "F"
        else:
            gender = "O"
        self._gender = gender


class Question(models.Model):
    responses = ArrayField(
        models.CharField(max_length=50)
    )
    text = models.CharField(max_length=100)
    creator_id = models.ForeignKey(User, on_delete=models.PROTECT)
    public = models.BooleanField()
    language = models.CharField(choices=[("GB", "English"), ("ES", "Spanish")], max_length=2)


class JournalEntry(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor_id = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class PendingQuestion(JournalEntry):
    answering = models.BooleanField()


class AnsweredQuestion(JournalEntry):
    answer_date = models.DateTimeField()
    response = models.CharField(max_length=100)
