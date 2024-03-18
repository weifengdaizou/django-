import json

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
# Create your views here.
from django.contrib import auth
from django.db.models import F
from django.db.models import Avg, Max, Min, Count
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from bs4 import BeautifulSoup
from app01 import my_forms
from app01.models import *


def index(request):
    articles = Article.objects.all().order_by('create_time').reverse()

    return render(request, 'index.html', {"articles": articles})


def login(request):
    if request.method == 'POST':
        response = {'user': None, 'msg': None}
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        valid_code_print = request.POST.get('valid_code')
        valid_code_true = request.session.get('valid_code')
        print(valid_code_true, valid_code_print)
        # if valid_code_print.upper() == valid_code_true.upper():
        user = auth.authenticate(username=username, password=pwd)
        if user:
            auth.login(request, user)  # 注册用户
            response['user'] = request.user.username

            return JsonResponse({'user': username, 'msg': None})
        else:
            response['msg'] = '密码错误'
        # else:
        #     response['msg'] = '验证码错误'
        return JsonResponse(response)

    else:
        userforms = my_forms.UserForms(request.POST)
    return render(request, 'login.html', {'forms': userforms})


def getvalidCode(request):
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img = Image.new('RGB', (270, 40), random_color())

    draw = ImageDraw.Draw(img)
    sr1 = ''
    for i in range(4):
        int_num = str(random.randint(1, 9))
        upp_as = chr(random.randint(65, 90))
        low_as = chr(random.randint(97, 122))
        random_char = random.choice([int_num, upp_as, low_as])
        font = ImageFont.load_default()
        sr1 += random_char
        draw.text((50 + 50 * i, 20), random_char, font=font)

    print(sr1)
    request.session['valid_code'] = sr1
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)


def register(request):
    if request.method == 'POST':

        response = {'username': None, 'msg': None}
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = request.POST.get('re_password')
        telephone = request.POST.get('telephone')

        valid_code = request.POST.get('valid_code')
        valid_code_true = request.session.get('valid_code')
        print(valid_code_true, valid_code)
        if valid_code.upper() == valid_code_true.upper():
            userforms = my_forms.UserForms(request.POST)
            if userforms.is_valid():
                response['user'] = userforms.cleaned_data
                print(userforms.cleaned_data)
                avater = request.FILES.get('avater')
                username = userforms.cleaned_data.get('username')
                password = userforms.cleaned_data.get('password')
                telephone = userforms.cleaned_data.get('telephone')

                bolg_obj = Bole.objects.create(title=f'{username}的站点', site_name=username, theme=f'{username}主题')
                if avater:
                    Userinfo.objects.create_user(username=username, password=password, telephone=telephone, avatar=avater, bolg=bolg_obj)
                else:
                    Userinfo.objects.create_user(username=username, password=password, telephone=telephone, bolg=bolg_obj)

            else:
                response['msg'] = userforms.errors
        else:
            response['msg'] = {'error': '验证码校验失败'}
        return JsonResponse(response)

    userforms = my_forms.UserForms(request.POST)
    return render(request, 'register.html', {'forms': userforms})


def logout(request):
    auth.logout(request)
    return redirect('/blog/login/')


def get_data(user):
    if not user:
        return HttpResponse('该用户没有创建主题页面')

    bolg_obj = user.bolg

    category_list = Category.objects.filter(bolg=bolg_obj).values('pk').annotate(c=Count('article__nid')).values(
        'title', 'c')
    tag_list = Tag.objects.filter(bolg=bolg_obj).values('pk').annotate(c=Count('article__pk')).values('title', 'c')
    data_list = Article.objects.filter(user=user).extra(
        select={'y_m_d': "date_format(create_time, '%%Y-%%m')"}).values(
        'y_m_d').annotate(c=Count('pk'))
    return {'category_list': category_list, 'tags': tag_list, 'bolg': bolg_obj,
            'data_list': data_list}


def home_site(request, username, **kwargs):
    user = Userinfo.objects.filter(username=username).first()
    content = get_data(user)
    if kwargs:
        tag = kwargs.get('tag')
        param = kwargs.get('param')
        if tag == 'tag':
            articles = Article.objects.filter(user=user, tag__title=param)
        elif tag == 'category':
            articles = Article.objects.filter(user=user, category__title=param)
        elif tag == 'date':
            y, m = param.split('-')
            articles = Article.objects.filter(user=user, create_time__year=y, create_time__month=m)
    else:
        articles = Article.objects.all()
    content['articles'] = articles
    return render(request, 'home.html', content)


def arcile_datatil(request, username, arcile_id):
    user = Userinfo.objects.filter(username=username).first()

    content = get_data(user)
    arcile = Article.objects.filter(pk=arcile_id).first()
    content['arcile'] = arcile
    comment_list = Comment.objects.filter(article_id=arcile_id)
    content['comment_list'] = comment_list
    return render(request, 'arciles_datatil.html', content)


def upup(request):
    response = {'up_count': None, 'down_count': None, 'msg': None}
    article_id = request.POST.get('article')
    user_id = request.user.pk
    is_up = request.POST.get('is_up')
    is_up = True if is_up == 'true' else False
    ret = ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id)
    article = Article.objects.filter(pk=article_id)
    if ret:
        if ret.first().is_up != is_up:
            ret.update(is_up=is_up)
            if is_up:
                article.update(down_count=F('down_count') - 1)
                article.update(up_count=F('up_count') + 1)
            else:
                article.update(down_count=F('down_count') + 1)
                article.update(up_count=F('up_count') - 1)
        else:
            if is_up:
                response['msg'] = '你已经点赞过了'
            else:
                response['msg'] = '你已经踩过了'
    else:
        ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
        if is_up:
            article.update(up_count=F('up_count') + 1)
        else:
            article.update(down_count=F('down_count') + 1)
    response['up_count'] = article.first().up_count
    response['down_count'] = article.first().down_count
    return JsonResponse(response)


def comment(request):
    article_id = request.POST.get('article_id')
    pid = request.POST.get('pid')
    content = request.POST.get('content')
    user_id = request.user.pk

    ind = content.find('\n')
    content = content[ind + 1:]

    soup = BeautifulSoup(content, 'lxml')
    print(soup)

    with transaction.atomic():
        comment = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)
    response = {}
    response['create_time'] = comment.create_tiem.strftime('%Y-%m-%d')
    response['user'] = request.user.username
    response['content'] = content
    response['comment_pk'] = comment.pk

    return JsonResponse(response)


def set_tree(request):
    article_id = request.GET.get('article_id')
    comment_list = list(Comment.objects.filter(article_id=article_id).values('pk', 'parent_comment_id', 'content'))
    return JsonResponse(comment_list, safe=False)


def require_login(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/blog/login')  # 你可以更改 'login' 为你自己的登录 URL 名字
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


@require_login
def cn_backend(request):
    user_id = request.user.pk
    user = Userinfo.objects.get(pk=user_id)
    article_list = user.article_set.all()
    return render(request, 'backend.html', {"article_list": article_list})


@require_login
def add_tag(request):
    title = request.POST.get('title')
    response = {'success': None, 'msg': None}
    if title:
        user_obj = Userinfo.objects.get(pk=request.user.pk)
        bold_obj = user_obj.bolg

        ret = Tag.objects.filter(title=title, bolg=bold_obj).exists()

        if ret:
            response['msg'] = '该关键字已存在'
        else:
            tag_obj = Tag.objects.create(title=title, bolg=bold_obj)
            response['success'] = '添加成功'
            response['tag_pk'] = tag_obj.pk
            response['tag_title'] = tag_obj.title
    else:
        response['msg'] = '请输入'
    return JsonResponse(response)


@require_login
def add_category(request):
    title = request.POST.get('title')
    response = {'success': None, 'msg': None}
    if title:
        user_obj = Userinfo.objects.get(pk=request.user.pk)
        bold_obj = user_obj.bolg
        ret = Category.objects.filter(title=title, bolg=bold_obj).exists()
        if ret:
            response['msg'] = '该标签已存在'
        else:
            print(bold_obj.pk)
            category_obj = Category.objects.create(title=title, bolg=bold_obj)
            response['success'] = '添加成功'
            response['category_pk'] = category_obj.pk
            response['category_title'] = title
    else:
        response['msg'] = '请输入'

    return JsonResponse(response)


@require_login
def add_article(request):
    user_obj = Userinfo.objects.get(pk=request.user.pk)
    bold_obj = user_obj.bolg
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        desc = request.POST.get('desc')
        tag = request.POST.getlist('tag[]')
        category = request.POST.get('category')
        soup = BeautifulSoup(content, 'lxml')
        print(tag)
        with transaction.atomic():
            article_obj = Article.objects.create(title=title, desc=desc, content=content, category_id=category, user=user_obj)
            article_id = article_obj.pk
            article_tag_list = []
            for i in tag:
                article_tag = Article2Tag(tag_id=int(i), article_id=article_id)
                article_tag_list.append(article_tag)
            Article2Tag.objects.bulk_create(article_tag_list)
        return HttpResponse('/blog/cn_backend/')
    else:
        try:
            category_list = bold_obj.category_set.all()
            tag_list = bold_obj.tag_set.all()
            return render(request, 'add_article.html', {'category_list': category_list, 'tag_list': tag_list})
        except Exception as e:
            print(e)
            return render(request, 'add_article.html')

@require_login
def edit_article(request):
    user_obj = Userinfo.objects.get(pk=request.user.pk)
    bold_obj = user_obj.bolg
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        desc = request.POST.get('desc')
        tag = request.POST.getlist('tag[]')
        category = request.POST.get('category')
        article_id = request.POST.get('article_id')
        with transaction.atomic():
            Article.objects.filter(pk=article_id).update(title=title, content=content, desc=desc, category_id=category)
            Article2Tag.objects.filter(article_id=article_id).delete()
            article_tag_list = []
            for i in tag:
                article_tag = Article2Tag(tag_id=int(i), article_id=article_id)
                article_tag_list.append(article_tag)
            Article2Tag.objects.bulk_create(article_tag_list)
        return HttpResponse('/blog/cn_backend/')

    article_id = request.GET.get('article_id')
    article_obj = Article.objects.get(pk=article_id)

    my_tags = list(article_obj.article2tag_set.all())
    my_tags = [i.tag_id for i in my_tags]
    category_list = bold_obj.category_set.all()
    tag_list = bold_obj.tag_set.all()
    return render(request, 'edit_article.html',
                  {"article_obj": article_obj, 'category_list': category_list, 'tag_list': tag_list,
                   'my_tags': my_tags})


@require_login
def delete_article(request):
    article_id = request.GET.get('article_id')
    response = {'success': None, 'msg': None}
    with transaction.atomic():
        article_obj = Article.objects.get(pk=article_id)
        article_obj.article2tag_set.all().delete()
        article_obj.delete()
    response['success'] = article_id
    return JsonResponse(response)