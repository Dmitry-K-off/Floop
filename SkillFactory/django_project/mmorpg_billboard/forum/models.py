from django.db import models
from django.contrib.auth.models import User

# Project models.

"""
Category model represents different categories for announcements.
Each announcement belongs to one category.
"""
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


"""
Announcement model represents individual announcements created by users.
Each announcement is linked to a user and a category.
"""
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    images = models.FileField(upload_to='announcements/images/', blank=True, null=True)
    videos = models.FileField(upload_to='announcements/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


"""
Response model represents responses to announcements.
Each response is linked to a user and an announcement.
"""
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик на {self.announcement.title}"