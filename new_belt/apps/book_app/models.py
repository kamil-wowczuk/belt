# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist

#####################################################################

def is_email(value):
    try:
        validate_email(value)
    except ValidationError:
        print 'def is_email', value, 'Is not a valid email address'
        return False
    else:
        print 'def is_email', value, 'Is a valid email address'
        return True

def user_exists(value):
    try:
        user = User.objects.get(email=value)
    except ObjectDoesNotExist:
        print 'def users_exists', value, 'User does not exist'
        return False
    else:
        print 'def users_exists', value, 'User exists'
        return True

####################################################################

class UserManager(models.Manager):
#####################################################################
    def register(self, name, alias, email, password, confirm_password):
        min_name = 2 #require name length
        min_pass = 8 #required password length
        if user_exists(email) == False and len(name) > min_name and len(password) > min_pass and is_email(email) and password == confirm_password:
            User.objects.create(name=name, alias=alias, email=email, password=password)
            return True
        else:
            return False
#####################################################################
    def login(self, email, password):
        if user_exists(email) == True:
            user = User.objects.get(email=email)
            if user.password == password:
                return {'result':'positive', 'user_id':user.id}
            else:
                return {'result':'negative'}
        else:
            return {'result':'negative'}
#####################################################################

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=45)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    author = models.ForeignKey(Author)
    user = models.ManyToManyField(User, related_name='books')
    def __str__(self):
        return self.title



class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User, related_name='reviews')
    book = models.ManyToManyField(Book, related_name='reviews')