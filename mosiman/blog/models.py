from django.db import models
from django.utils.text import slugify

from datetime import datetime

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField()
    content = models.TextField(default="")

    def save(self, *args, **kwargs):
     self.slug = slugify(self.title)
     #this line below save every fields of the model instance
     super(Entry, self).save(*args, **kwargs) 
