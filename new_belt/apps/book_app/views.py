# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Book, Review, Author
from django.core.exceptions import ValidationError, ObjectDoesNotExist


######################### INDEX
def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
    user_id = request.session['user_id']
    if user_id == 0:
        return render(request, 'book_app/index.html')
    else:
        return redirect('/books')

######################### Logout
def logout(request):
    request.session['user_id'] = 0
    return redirect('/')

########################## Register
def register(request):
    if request.method == 'POST':
        data = {
            'name':request.POST['name'],
            'alias':request.POST['alias'],
            'email':request.POST['email'],
            'password':request.POST['password'],
            'confirm_password':request.POST['confirm_password']
        }

    User.objects.register(data['name'], data['alias'], data['email'], data['password'], data['confirm_password'])
    return redirect('/')

########################## Login
def login(request):
    if request.method == 'POST':
        data = {
            'email':request.POST['email'],
            'password':request.POST['password']
        }
        login_result = User.objects.login(data['email'], data['password'])
        if login_result['result'] == 'positive':
            print 'User_id from models is ', login_result['user_id']
            request.session['user_id'] = login_result['user_id']
            return redirect('/books')
        elif login_result['result'] == 'negative':
            return redirect('/')

def books(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        'user_name':user.name,
        'books':Book.objects.all()
    }
    return render(request, 'book_app/books.html', context)

def add(request):
    return render(request, 'book_app/add.html')

def add_book(request):

    if request.method == 'POST':
        user = User.objects.get(pk=request.session['user_id'])

        data = {
            'title':request.POST['title'],
            'content':request.POST['review'],
            'rating':request.POST['rating'],
        }

        #Create new author or add author 
        author_name = request.POST['new_author']
        print 'About to see if a new author was provided'
        if len(author_name) > 0:
            try:
                print ' Trying to get existin author '
                author = Author.objects.get(name=author_name)
            except:
                print 'Trying to create a new author'
                author = Author.objects.create(name=author_name)
        else:            
            print 'About to set author to existing author '
            author_name = request.POST['author']
            author = Author.objects.get(name=author_name)
        print 'Author is ', author

        #Create book entry
        try:
            book = Book.objects.get(name=data['title'])
        except:
            book = Book.objects.create(name=data['title'], author=author, user=user)
            print 'New book added'



    return redirect('/books')