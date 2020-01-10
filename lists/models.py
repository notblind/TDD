from django.db import models

# Create your models here.

class Item(models.Model):
	text = models.TextField(blank=False)
	date = models.DateField(auto_now_add=True)