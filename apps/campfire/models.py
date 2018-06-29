from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
import bcrypt
import re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):

    def check_reg(self,postData):
        errors = {}
        if len(postData['firstName']) < 1:
            errors["firstname"] = "First Name cannot be empty"
        elif len(postData['firstName']) < 2:
            errors["firstname"] = "First Name should be atleast 2 characters"
        elif not postData['firstName'].isalpha():
            errors["firstname"] = "First Name should contain only letters"

        if len(postData['lastName']) < 1:
            errors["lastname"] = "Last Name cannot be empty"
        elif len(postData['lastName']) < 2:
            errors["lastname"] = "Last Name should be atleast 2 characters"
        elif not postData['lastName'].isalpha():
            errors["lastname"] = "Last Name should contain only letters"

        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be empty"
        elif not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "Not a Valid Email"

        if len(postData['pwd']) < 1:
            errors["pwd"] = "Password cannot be empty"
        elif len(postData['pwd']) < 8:
            errors["pwd"]= "Password must be more than 8 characters"
        elif len(postData['confpwd']) < 1:
            errors["confpwd"] = "Field cannot be empty"
        elif len(postData['confpwd']) < 8:
            errors["confpwd"]= "Password must be more than 8 characters"
        elif not(postData['pwd'] == postData['confpwd']):
            errors["pwd"] = "Passwords don't match! Please enter again"

        if (errors):
            return [False,errors]

        check_user = User.objects.filter(email = postData['email'])

        if (check_user):
            errors['email'] ="This email is already registered!"
            return [False,errors]
        if not User.objects.all():
            User.objects.create(first_name=postData['firstName'],
                                last_name = postData['lastName'],
                                email = postData['email'],
                                userlevel = 1,
                                pwdhash = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
                                )
        else:
            User.objects.create(first_name= postData['firstName'],
                                last_name = postData['lastName'],
                                email = postData['email'],
                                userlevel = 2,
                                pwdhash = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
                               )

        newuser = User.objects.get(email = postData['email'])

        Profile.objects.create(user = newuser)

        return [True,newuser]

    def check_login(self,postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if user.count() > 0 :
            if bcrypt.checkpw(postData['loginpwd'].encode(),user[0].pwdhash.encode()):
                return [True,user[0]]
        errors['login'] = "Bad Credentials!"
        return [False,errors]

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    pwdhash = models.CharField(max_length=255)
    userlevel = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return 'ID: %s | Name: %s %s | Email: %s' % (self.id, self.first_name, self.last_name, self.email)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=30, blank=True,null=True)
    location = models.CharField(max_length=30, blank=True,null=True)
    bio = models.TextField(max_length=500, blank=True,null=True)
    url = models.CharField(max_length=30,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now = True,blank=True,null=True)
    def __str__(self):
        return 'ID: %s | Job_Title: %s | Location: %s | Bio: %s | URL: %s' % (self.id, self.job_title, self.location, self.bio,self.url)


class Question(models.Model):
    title = models.CharField(max_length=100)
    desc = RichTextField()
    votes = models.IntegerField(default=0)
    posted_by = models.ForeignKey(User,related_name="questions",on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now = True,blank=True,null=True)
    def __str__(self):
        return 'ID: %s | Title: %s | Desc: %s | Votes: %s' % (self.id, self.title, self.desc,self.votes)

class Answer(models.Model):
    desc = RichTextField()
    votes = models.IntegerField(default=0)
    answers = models.ForeignKey(Question,related_name="questions",on_delete=models.CASCADE)
    answered_by = models.ForeignKey(User,related_name="posted_answer",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    def __str__(self):
        return 'ID: %s | Desc: %s | Votes: %s' % (self.id, self.desc,self.votes)

class Message(models.Model):
    subject = models.CharField(max_length=100)
    content = RichTextField()
    parent_id = models.IntegerField(null=True)
    sent_by = models.ForeignKey(User,related_name="sent_messages",on_delete=models.CASCADE)
    received_by = models.ForeignKey(User,related_name="received_messages",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    def __str__(self):
        return 'ID: %s | Subject: %s |  Content: %s ' % (self.id, self.subject,self.content)
