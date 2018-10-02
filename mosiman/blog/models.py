from django.db import models

from datetime import datetime

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField()
    content = models.TextField
