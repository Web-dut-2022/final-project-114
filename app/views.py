from django.shortcuts import render, HttpResponse, redirect, reverse
from app import models
import json
import datetime


# Create your views here.

# 装饰器 判断session里面是否有is_login参数
def required_login(func):
    def inner(*args, **kwargs):
        request = args[0]
        # cookie写法
        # if request.COOKIES.get('is_login'):

        # session写法
        if request.session.get('is_login'):
            return func(*args, **kwargs)
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps({'status': 0}))
            return redirect(reverse('login'))

    return inner


@required_login
def books(request):
    books = models.Book.objects.all()
    return render(request, 'books.html', {'books': books})


@required_login
def authors(request):
    authors = models.Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


@required_login
def publish(request):
    publish = models.Publish.objects.all()
    return render(request, 'publish.html', {'publish': publish})


@required_login
def borrow(request):
    borrows = models.Borrow.objects.all()
    return render(request, 'borrows.html', {'borrows': borrows})


@required_login
def add_book(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('name')
        price = request.POST.get('price')
        date = request.POST.get('date')
        publish = request.POST.get('publish')
        authors = request.POST.getlist('authors')
        print(title, price, date, publish, authors)

        new_book = models.Book.objects.create(title=title, price=price, pub_date=date, publish_id=publish)
        new_book.authors.add(*authors)
        return redirect(reverse('books'))
    publishers = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request, 'add_book.html', {'publishers': publishers, 'authors': authors})


@required_login
def add_author(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        age = request.POST.get('age')
        tel = request.POST.get('tel')
        addr = request.POST.get('addr')
        # print(name, age, tel, addr)

        new_author = models.Author.objects.create(name=name, age=age, tel=tel, addr=addr)
        return redirect(reverse('authors'))

    return render(request, 'add_author.html', {})


@required_login
def add_publish(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        addr = request.POST.get('addr')
        new_publish = models.Publish.objects.create(name=name, email=email, addr=addr)
        return redirect(reverse('publish'))

    return render(request, 'add_publish.html', {})


@required_login
def edit_book(request, edit_id):
    book_obj = models.Book.objects.get(id=edit_id)
    if request.method == 'POST':
        title = request.POST.get('name')
        price = request.POST.get('price')
        date = request.POST.get('date')
        publish = request.POST.get('publish')
        authors = request.POST.get('authors')
        book_obj.title = title
        book_obj.price = price
        book_obj.pub_date = date
        book_obj.publish_id = publish
        book_obj.save()
        book_obj.authors.set(authors)
        return redirect(reverse("books"))
    publishers = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request, 'edit_book.html', {'book_obj': book_obj, 'publishers': publishers, 'authors': authors})


@required_login
def edit_author(request, edit_id):
    author_obj = models.Author.objects.get(id=edit_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        tel = request.POST.get('tel')
        addr = request.POST.get('addr')
        author_obj.name = name
        author_obj.age = age
        author_obj.tel = tel
        author_obj.addr = addr
        author_obj.save()
        return redirect(reverse("authors"))

    return render(request, 'edit_author.html', {'author_obj': author_obj})


@required_login
def edit_publish(request, edit_id):
    publish_obj = models.Publish.objects.get(id=edit_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        addr = request.POST.get('addr')
        publish_obj.name = name
        publish_obj.email = email
        publish_obj.addr = addr
        publish_obj.save()
        return redirect(reverse("publish"))

    return render(request, 'edit_publish.html', {'publish_obj': publish_obj})


@required_login
def del_book(request):
    # print(request.POST)
    del_id = request.POST.get('del_id')
    del_list = models.Book.objects.filter(id=del_id)
    # print(del_list)
    del_list.delete()
    return HttpResponse(json.dumps({'status': 1}))


@required_login
def del_author(request):
    del_id = request.POST.get('del_id')
    del_list = models.Author.objects.filter(id=del_id)
    # print(del_list)
    del_list.delete()
    return HttpResponse(json.dumps({'status': 1}))


@required_login
def del_publish(request):
    # print(request.POST)
    del_id = request.POST.get('del_id')
    del_list = models.Publish.objects.filter(id=del_id)
    # print(del_list)
    del_list.delete()
    return HttpResponse(json.dumps({'status': 1}))


def login(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        is_admin = request.POST.get('is_admin')

        user_list = models.User.objects.filter(name=name, pwd=pwd)

        if user_list:
            user_obj = user_list.first()
            ret = redirect(reverse('books'))
            # cookie写法
            # ret.set_cookie('is_login', True)
            # ret.set_cookie('user', name)
            # ret.set_cookie('last_time', user_obj.last_time)

            # session写法,安全
            request.session['is_login'] = True
            request.session['user'] = name
            request.session['last_time'] = str(user_obj.last_time)
            user_obj.last_time = datetime.datetime.now()
            user_obj.save()
            return ret
    return render(request, "login.html")


@required_login
def logout(request):
    ret = redirect(reverse('login'))
    # cookie写法
    # ret.delete_cookie('is_login')
    # ret.delete_cookie('user')
    # ret.delete_cookie('last_time')

    # session写法
    request.session.flush()
    return ret


def register(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        confirm = request.POST.get('confirm')
        if pwd == confirm:
            new_user = models.User.objects.create(name=name, pwd=pwd, is_admin=False )
            return redirect(reverse('login'))
        else:
            return redirect(reverse('register'))
    return render(request, 'register.html', {})

