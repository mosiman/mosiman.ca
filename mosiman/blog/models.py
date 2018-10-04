from django.db import models
from django.utils.text import slugify

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


from datetime import datetime

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField()
    content = MarkdownxField()
    coverphoto = models.ImageField(upload_to='blog/static/blog/', blank=True)

    @property
    def formatted_markdown(self, *args, **kwargs):
        return markdownify(self.content)

    @property
    def staticpath(self, *args, **kwargs):
        return "/" + "/".join(self.coverphoto.name.split('/')[1:])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
     self.slug = slugify(self.title)
     #this line below save every fields of the model instance
     super(Entry, self).save(*args, **kwargs) 
