from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="author")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.body
