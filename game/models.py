from django.db import models

# Create your models here.

"""
class Participants(models.Model):
    env_object = models.BinaryField(max_length=None)
    cookie_id = models.CharField(max_length=30, primary_key=True)
    load_date = models.DateTimeField(auto_now_add=True, null=True)
    done = models.BooleanField(default=False)
    step_count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f" {self.cookie_id} {self.load_date}"
        """