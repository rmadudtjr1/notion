from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.conf import settings
import shutil, os
from random import randint
from .models import Notion
import datetime, json
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json
import pdb

def index(request):
    try:
        notion = Notion.objects.filter(user=request.user.username).values()
        url = notion[0].get('url')
        return redirect(f"/notion/{url}")
    except:
        return render(request, 'notion.html')

def createNewPage(request):
    if not request.user.is_active:
        msg = "<script>"
        msg += "alert('로그인 후 사용 가능합니다.');";
        msg += 'location.href="/login";'
        msg += "</script>";
        return HttpResponse(msg);
    else :
        username = request.user.username;
        originFilePath = os.path.join(settings.BASE_DIR, "template");
        originFile = originFilePath + "\\origin.html"
        destinationPath = os.path.join(originFilePath, username);
        pageNum = randint(1, 9999999999);
        pageNum = str(f'{pageNum:0>10}') + ".html";

        if not os.path.isdir(destinationPath):
            os.mkdir(destinationPath)

        n = Notion();
        n.user = username;
        n.url = f'{pageNum}';
        n.date = datetime.datetime.now()
        n.save()

        shutil.copyfile(originFile, os.path.join(destinationPath, pageNum))
        return redirect(f'/notion/{pageNum}')
    
def pageNum(request, pageNum):
    if request.user.is_active:
        # 현재 사용자와 관련된 모든 Notion 객체 가져오기
        notions = Notion.objects.filter(user=request.user.username)
        # 현재 페이지와 관련된 Notion 객체 가져오기
        now = get_object_or_404(Notion, url=pageNum)
        print(now)
        username = request.user.username
        content = {
            'notions': notions,
            'now': now,
        }
        return render(request, f'{username}/{pageNum}', content)
    else:
        msg = "<script>"
        msg += "alert('로그인 후 사용 가능합니다.');"
        msg += 'location.href="/login";'
        msg += "</script>"
        return HttpResponse(msg)

def save(request, notionId):
    notion = Notion.objects.get(id=notionId)
    data = json.loads(request.body)
    notion.title = data['title'];
    notion.save();
    
    return JsonResponse({"message" : data['title']}, status=200)

def saveBody(request, notionId):
    notion = Notion.objects.get(id=notionId)
    data = json.loads(request.body)
    notion.content = data['content']
    notion.save();
    
    return JsonResponse({"message" : data['content']}, status=200)

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html');
    else :
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password);

        if user is not None:
            auth.login(request, user)
            msg = "<script>";
            msg += f"alert('{username}님 환영합니다.');";
            msg += "location.href='/';";
            msg += "</script>";
            return HttpResponse(msg);
        else:
            msg = "<script>";
            msg += "alert('로그인 아이디/비밀번호가 틀립니다. 다시 로그인 하세요.');";
            msg += "location.href='/login';";
            msg += "</script>";
            return HttpResponse(msg);

def logout(request):
    auth.logout(request);
    return render(request, 'logout.html');


def createAccount(request):
    if request.method == 'GET':
        return render(request, "register.html")
    elif request.method == 'POST':
        username = request.POST.get("username");
        password = request.POST.get("password");
        password2 = request.POST.get('password2');

        if password == password2:
            try:
                User.objects.create_user(username=username, password=password)
                msg = "<script>"
                msg += "alert('회원가입이 완료되었습니다.');";
                msg += "location.href='/login/';"
                msg += "</script>";
                return HttpResponse(msg)
            except:
                msg = "<script>";
                msg += "alert('같은 아이디가 존재합니다. 다시 가입하세요.');";
                msg += "location.href='/register';";
                msg += "</script>";
                return HttpResponse(msg);
        else :
            msg = "<script>";
            msg += "alert('비밀번호가 같지 않습니다. 다시 가입하세요.');";
            msg += "location.href='/register';";
            msg += "</script>";
            return HttpResponse(msg);


def sendEmail(request):
    url = request.GET.get('url');
    try :
        toEmail = request.GET.get('emails')
        toEmail = toEmail.split(',')
        email = EmailMessage(
            f'{request.user.username} 공유', #이메일 제목
            f'''안녕하세요. {request.user.username} 님이 공유하신 페이지 입니다.

http://localhost:8000/guest/{request.user.username}/{url}
            ''', #내용
            to=toEmail, #받는 이메일
        )
        result = email.send()

        if result == 1:
            msg = "<script>"
            msg += "alert('이메일 전송이 완료되었습니다.');";
        else:
            msg = "<script>"
            msg += "alert('이메일 전송에 실패 했습니다.');";
    except:
        msg = "<script>"
        msg += "alert('이메일 전송에 실패 했습니다.');";
    
    msg += f"location.href='/notion/{url}';";
    msg += "</script>"
    
    return HttpResponse(msg);


def guest(request, user, pageNum):  
    notion = Notion.objects.filter(user=user).values()
    now = Notion.objects.filter(url=f'{pageNum}').values()
    username = user;
    content = {
        'notion':notion,
        'now':now[0],
    }
    return render(request, f'{username}/{pageNum}', content);
    
def createChild(request, notionId, url):
    
    username = request.user.username
    originFilePath = os.path.join(settings.BASE_DIR, "template")
    originFile = os.path.join(originFilePath, "origin.html")
    destinationPath = os.path.join(originFilePath, username)
    pageNum = randint(1, 9999999999)
    pageNum = f'{pageNum:0>10}.html'

    if not os.path.isdir(destinationPath):
        os.mkdir(destinationPath)

    # 부모 Notion 객체 가져오기
    parent_notion = get_object_or_404(Notion, id=notionId)

    # 자식 Notion 생성
    child_notion = Notion.objects.create(user=username, url=pageNum, date=datetime.datetime.now(), parent=parent_notion)
    
    shutil.copyfile(originFile, os.path.join(destinationPath, pageNum))
    return redirect(f'/notion/{pageNum}')
