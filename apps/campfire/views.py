from django.shortcuts import render,HttpResponse, redirect
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from .forms import QuesForm,AnsForm,NewMessage,ReplyForm
from .models import *
import json
import bcrypt

def splash(request):
    return render(request,'campfire/login_reg.html')

def log_reg(request):
    if (request.method == 'POST'):
        if(request.POST['attempt'] == "register"):
            response = User.objects.check_reg(request.POST)
        if(request.POST['attempt'] == "login"):
            response = User.objects.check_login(request.POST)
        if not response[0]:
            for key,value in response[1].items():
                print(key,value)
                messages.error(request,value,extra_tags=key)
            return redirect ('/')
        request.session['user'] = {'first_name': response[1].first_name,
                                    'id': response[1].id,
                                    'email':response[1].email,
                                    'user_level': response[1].userlevel,
                                    }
        return redirect ('/articles')
    return redirect ('/')

def wall(request):
    return render(request,'campfire/app.html')

def profile(request):
    user_profile = Profile.objects.get(user_id = int(request.session['user']['id']))
    return render(request,'campfire/profile.html',{'user_profile':user_profile})

def editProfile(request):
    user_profile = Profile.objects.get(user_id = int(request.session['user']['id']))
    return render(request,'campfire/edit_profile.html',{'user_profile':user_profile})

def updateProfile(request):
    if (request.method == 'POST'):
        newuser = Profile.objects.get(user_id = int(request.session['user']['id']))
        print(newuser)
        newuser.job_title = request.POST['title']
        newuser.location = request.POST['location']
        newuser.bio = request.POST['bio']
        newuser.url = request.POST['url']
        newuser.save()
        return redirect('/profile')
    else:
        return redirect('/profile')

def network(request):
    user_profiles = Profile.objects.all()
    return render(request,'campfire/network.html',{'user_profiles':user_profiles})

def qanda(request):
    all_questions = Question.objects.all()
    return render(request,'campfire/qanda.html',{'all_questions':all_questions})

def addQuestion(request):
    args={
        'form' : QuesForm(),
    }
    return render(request,'campfire/question.html',args)

def addAnswer(request,number):
    args={
        'quest' : Question.objects.get(id=number),
        'answers' : Answer.objects.filter(answers = number),
        'form' : AnsForm()
    }
    return render(request,'campfire/answer.html',args)

def createAns(request):
    if request.method == "POST":
        form = AnsForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            print(post_item)
            post_item.answered_by = User.objects.get(id=request.session['user']['id'])
            post_item.answers = Question.objects.get(id=int(request.POST['quesId']))
            post_item.save()
            # newans = Answer.objects.last()
            # print(newans)
            return redirect('/'+request.POST['quesId']+'/addAnswer')

            # return render(request,'campfire/answer1.html',{'newans':newans})
    else:
        form = AnsForm()
    return redirect('/'+request.POST['quesId']+'/addAnswer')


def createQuest(request):
    if request.method == "POST":
        form = QuesForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            print(post_item)
            post_item.posted_by = User.objects.get(id=request.session['user']['id'])
            post_item.save()
            form.save_m2m()
            return redirect('/qanda')
    else:
        form = QuesForm()
    return redirect('/addQuestion')


def inbox(request):
    args={
        'messages' : Message.objects.filter(received_by_id=request.session['user']['id'])
    }

    return render(request,'campfire/inbox.html',args)

def newmess(request):
    args={
        'form' : NewMessage(),
        'users' : User.objects.all()
    }
    return render(request,'campfire/newmess.html',args)

def createMsg(request):
    if request.method == "POST":
        form = NewMessage(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.sent_by = User.objects.get(id=request.session['user']['id'])
            post_item.received_by = User.objects.get(id=request.POST['recipient'])
            post_item.save()
            return redirect('/inbox')
    else:
        form = NewMessage()
    return redirect('/newmess')


def delMess(request,number):
    this_Mess = Message.objects.get(id=int(number))
    this_Mess.delete()
    return redirect('/inbox')

def reply(request,number):
    args={
        'msg' : Message.objects.get(id=number),
        'replies' : Message.objects.filter(parent_id = number),
        'form' : ReplyForm()
    }
    return render(request,'campfire/reply.html',args)

def createReply(request):
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            post_item = form.save(commit=False)
            post_item.sent_by = User.objects.get(id=request.session['user']['id'])
            post_item.received_by = User.objects.get(id=int(request.POST['toId']))
            post_item.parent_id = request.POST['msgId']
            post_item.save()
            return redirect('/reply/'+request.POST['msgId'])
    else:
        form = NewMessage()
    return redirect('/reply/'+request.POST['msgId'])

def articles(request):
    return render(request,'campfire/articles.html')

def logout(request):
    request.session.flush()
    return redirect('/')
