from datetime import date
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('Book', 'Book'),
    ('Video', 'Video'),
    ('Audio', 'Audio'),
    ('Software', 'Software'),
    ('Image', 'Image'),
]

class Material(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    file = models.FileField(upload_to='materials/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=255, default="Unknown")
    release_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.title} ({self.category})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey('Material', related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.material.title} {self.rating}/5"

class DownloadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.material.title}"
     
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favourites = models.ManyToManyField(Material, blank=True)
    picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

