from django.db import models

from django import forms

class User(models.Model):
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    # Fix the invulnerability by hashing password in the database
    # password = models. hashed?

    def __str__(self):
        return self.username


class Bubble(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bubbles')
    bubble_text = models.CharField(max_length=500)
    pub_time = models.DateTimeField('time published')

    def __str__(self):
        return self.bubble_text
    
            