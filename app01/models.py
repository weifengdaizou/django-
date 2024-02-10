from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, User


# 用户表
class Userinfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatar/', default='/avatar/12.jpg')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    bolg = models.OneToOneField(to='Bole', to_field='nid', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nid) + '-->' + self.username


# 站点表
class Bole(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name='博客标题')
    site_name = models.CharField(max_length=64, verbose_name='站点名称')
    theme = models.CharField(max_length=64, verbose_name='博客主题')


# 标签表
class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)

    bolg = models.ForeignKey(to='Bole', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nid) + '-->' + self.title


# 分类表
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    bolg = models.ForeignKey(to='Bole', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nid) + '-->' + self.title


# 文章
class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章摘要')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content = models.TextField(verbose_name='文章内容')

    comment_count = models.IntegerField(default=0, verbose_name='文章总数')
    up_count = models.IntegerField(default=0, verbose_name='文章电点赞数')
    down_count = models.IntegerField(default=0)

    user = models.ForeignKey(to='Userinfo', to_field='nid', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', to_field='nid', null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag',
                                 through='Article2Tag',
                                 through_fields=('article', 'tag'))

    def __str__(self):
        return str(self.nid) + '-->' + self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag', to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]

    def __str__(self):
        return self.article.title + '--->' + self.tag.title


# 点赞
class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='Userinfo', to_field='nid', on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user')
        ]

    def __str__(self):
        return self.Userinfo.name + '--->' + self.article.title


# 评论
class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='Userinfo', to_field='nid', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    create_tiem = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', to_field='nid', null=True, on_delete=models.CASCADE)
