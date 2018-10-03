from django.contrib import admin

from .models import Entry

from markdownx.admin import MarkdownxModelAdmin
# Register your models here.

admin.site.register(Entry, MarkdownxModelAdmin)
