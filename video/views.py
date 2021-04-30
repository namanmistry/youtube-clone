from django.db import models
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Channel, History, Video, Comments, Library
from account.views import *
import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Account
import shutil
from django.db.models import Q

BASE_DIR = Path(__file__).resolve().parent.parent

def upload(request):
    if request.method == "POST":
        if get_user_id() != 0:
            uploaded_thumbnail = request.FILES['thumbnail']
            uploaded_video = request.FILES['video']
            if Channel.objects.filter(Account=get_user_id()).exists():
                channel = Channel.objects.get(Account=get_user_id())
                video = Video.objects.create(title=request.POST.get('title'),description1=request.POST.get('description1'),description2=request.POST.get('description2'),thumbnail=uploaded_thumbnail,channel=channel)
                video.save()
                videos = Video.objects.all().last()
                os.mkdir(f'{BASE_DIR}\\media\\{videos.id}\\')
                fs=FileSystemStorage(BASE_DIR)
                fs.save(uploaded_video.name,uploaded_video)
                video = ffmpeg_streaming.input(f'{BASE_DIR}\\{uploaded_video.name}')
                dash = video.dash(Formats.h264())
                dash.auto_generate_representations()
                dash.output(f'{BASE_DIR}\\media\\{videos.id}\\{videos.id}.mpd')
                os.remove(f'{BASE_DIR}\\{uploaded_video.name}')
                return HttpResponse("video uploaded successfully")
            return HttpResponse("You mush have channel in order to post the video")
        return HttpResponse("You must be logged in")
    return render(request,'video/upload.html')

def create_channel(request):
    if request.method == "POST":
        if get_user_id() != 0:
            if Channel.objects.filter(Account=get_user_id()).exists():
                return HttpResponse("You Already Have Channel, You cannot create another one")
            channel =  Channel.objects.create(name=request.POST.get('name'),image=request.FILES['image'], Account=get_user_id())
            channel.save()
            return HttpResponse("Channel created successfully")
        return HttpResponse("You must be logged in")
    return render(request,'video/create_channel.html')

def home(request):
    if get_user_id():
        context = {
            'videos': Video.objects.all(),
            'watcher':get_user_id()
        }
    else:
        context = {
                'videos': Video.objects.all(),
                'watcher': 0
            }
    return render(request,'video/index.html',context)

def watch_by_id(request,id):
    if get_user_id() != 0:
        video = Video.objects.get(id=id)
        video.views = int(video.views)+1
        video.save()

        history = History.objects.create(Account=get_user_id(),video_id=id)
        history.save()
        context = {
            'video': Video.objects.get(id=id),
            'allvideos': Video.objects.all(),
            'comments': Comments.objects.filter(video_id=id),
            'numberOfComments': Comments.objects.all().count()
        }
        return render(request,'video/watch.html',context)
    return HttpResponse("Please Log in")

@csrf_exempt
def like_by_id(request,id):
    if request.method == "POST":
        if get_user_id() != 0:
            video = Video.objects.get(id=id)
            video.likes = int(video.likes)+1
            video.save()
            return HttpResponse(video.likes)
        return HttpResponse("Please Log in")
    return HttpResponse("Method not allowed")

@csrf_exempt
def dislike_by_id(request,id):
    if request.method == "POST":
        if get_user_id() != 0:
            video = Video.objects.get(id=id)
            video.dislikes = int(video.dislikes)+1
            video.save()
            return HttpResponse(video.dislikes)
        return HttpResponse("Please Log in")
    return HttpResponse("Method not allowed")

@csrf_exempt
def save_by_id(request,id):
    if request.method == "POST":
        if get_user_id() != 0:
            library = Library.objects.create(Account=get_user_id(),video_id=id)
            library.save()
            return HttpResponse("Saved To Library")
        return HttpResponse("Please log in")
    return HttpResponse("Method not allowed")

@csrf_exempt
def comment_by_id(request,id):
    if request.method == "POST":
        if get_user_id() != 0:
            data=json.loads(request.body)
            comment = Comments.objects.create(Account=get_user_id(),description=data["data"],video_id=id)
            comment.save()
            account = Account.objects.get(id=get_user_id().id)
            data ={
                'name': account.firstName,
                'description':data["data"],
                'numberOfComments': Comments.objects.filter(video_id=id).count()
            }
            return HttpResponse(json.dumps(data))
        return HttpResponse("Please log in")
    return HttpResponse("Method not allowed")

@csrf_exempt
def subscribe_by_id(request,id):
    if request.method == "POST":
        if get_user_id() != 0:
            channel = Channel.objects.get(id=id)
            channel.subscribers = int(channel.subscribers)+1
            channel.save()
            return HttpResponse(channel.subscribers)
        return HttpResponse("Please log in")
    return HttpResponse("Method not allowed")

@csrf_exempt
def delete_by_id(request,id):
    if request.method == "POST":
        if get_user_id():
            video = Video.objects.get(id=id)
            video.delete()
            shutil.rmtree(os.path.join(BASE_DIR,'media',f'{id}'))
            return HttpResponse("<h1>Video Deleted Successfully.</h1>")
        else:
            return HttpResponse("<h1>You Must Be Logged In.</h1>")
    return render(request,'video/admin.html')

def admin(request):
    if get_user_id():
        channel_id = Channel.objects.get(Account_id=get_user_id())
        context = {
            'videos': Video.objects.filter(channel_id=channel_id)
        }
        return render(request,'video/admin.html',context)
    return HttpResponse("<h1>You Must Be Logged In.</h1>")

def history(request):
    if get_user_id():
        context = {
            'history' :  History.objects.filter(Account_id=get_user_id()),
            'watcher': get_user_id()
        }
        return render(request,'video/history.html',context)
    return HttpResponse("<h1>You Must Be Logged In.</h1>")

def library(request):
    if get_user_id():
        context = {
            'library' :  Library.objects.filter(Account_id=get_user_id()),
            'watcher': get_user_id()
        }
        return render(request,'video/Library.html',context)
    return HttpResponse("<h1>You Must Be Logged In.</h1>")

@csrf_exempt
def search(request):
    if request.method == "POST":
        searchtext = request.POST.get('searchtext')
        if Video.objects.filter(Q(title__icontains=searchtext)| Q(description1__icontains=searchtext) | Q(description2__icontains=searchtext)):
            context = {
                'videos': Video.objects.filter(Q(title__icontains=searchtext)| Q(description1__icontains=searchtext) | Q(description2__icontains=searchtext))
            }

        else:  
            context = {
                'videos': Video.objects.all()
            }
        return render(request, 'video/result.html',context)