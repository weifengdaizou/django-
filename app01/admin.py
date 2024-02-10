from django.contrib import admin

from app01 import models
# Register your models here.


admin.site.register(models.Userinfo)
admin.site.register(models.Bole)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.Article2Tag)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Comment)
