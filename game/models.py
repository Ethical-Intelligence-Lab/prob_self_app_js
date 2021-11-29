from django.db import models


# Create your models here.

class Participant(models.Model):
    data = models.JSONField(max_length=None, null=True)
    accept_dt = models.DateTimeField(auto_now_add=True, null=True)
    finish_dt = models.DateTimeField(null=True)
    elapsed_sec = models.IntegerField(null=True)
    worker_id = models.CharField(max_length=100, unique=True)
    assignment_id = models.CharField(max_length=100)
    hit_id = models.CharField(max_length=100)
    game_type = models.CharField(max_length=50, null=True)
    finished_game = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.worker_id} {self.accept_dt}"


class Demographics(models.Model):
    participant = models.OneToOneField(Participant,
                                       on_delete=models.CASCADE,
                                       primary_key=True)
    ethnicity = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    edu = models.CharField(max_length=200)
    age = models.IntegerField()
    game_exp = models.IntegerField()

    def __str__(self):
        return f" Demographics: {self.participant}"
