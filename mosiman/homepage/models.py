from django.db import models

from datetime import datetime

# Create your models here.

class PortfolioPiece(models.Model):
    cardphoto = models.ImageField(upload_to='homepage/static/homepage/', blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField(default="")
    date = models.DateTimeField(default = datetime.now, blank=True)
    cardfooter = models.CharField(max_length = 150, default="")
    cardlink = models.TextField(default="")

    @property
    def staticpath(self, *args, **kwargs):
        return "/" + "/".join(self.cardphoto.name.split('/')[1:])

    def __str__(self):
        return self.title

