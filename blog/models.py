from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic=models.CharField(max_length=50)
    content=models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.topic
