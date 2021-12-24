from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt    # 取消csrf
from . import forms
from . import models
import uuid
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
# Create your views here.
smtpObj = smtplib.SMTP_SSL(host='smtp.qq.com',port=465)
smtpObj.login('407535695@qq.com',"xbqtivpxbgshcaie")


@csrf_exempt
def index(request):
    title = '首页'
    return render(request, 'index.html', locals())


@csrf_exempt
def login(request):
    title = '登录'
    error = ''
    login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():  # 判断是否填写完成
            user = login_form.cleaned_data  # 清理数据
            user_info = models.User.objects.get(username=user['username'])
            request.session['is_login'] = True
            request.session['username'] = user['username']
            request.session['school_name'] = ''
            request.session['profession_name'] = ''
            request.session['province'] = user_info.province
            request.session['student_type'] = user_info.subject
            request.session['epoch'] = '本科批'
            request.session['profession_name'] = ''
            return redirect('/')
        else:
            # 获取全局的error信息,只显示第一个
            if login_form.errors.get('__all__'):
                error = login_form.errors.get('__all__')[0]

    return render(request, 'login.html', locals())


@csrf_exempt
def register(request):
    title = '注册'
    error = ''
    register_form = forms.RegisterForm()
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():    # 判断是否填写完成
            user = register_form.cleaned_data  # 清理数据
            models.User.objects.create(username=user['username'], password=user['password1'],email=user['email'],rank=60000)
            return redirect('/login/')
        else:
            # 获取全局的error信息,只显示第一个
            if register_form.errors.get('__all__'):
                error = register_form.errors.get('__all__')[0]

    return render(request, 'register.html', locals())

@csrf_exempt
def forget(request):
    global smtpObj
    title = '忘记密码'
    error = ''
    forget_form = forms.ForgetForm()
    is_email_send = False
    if request.method == 'POST': 
        forget_form = forms.ForgetForm(request.POST)
        if forget_form.is_valid():  # 判断是否填写完成
            user = models.User.objects.filter(email=forget_form.cleaned_data['email']).first()
            uuid_code= str(uuid.uuid1())
            message = MIMEText('http://127.0.0.1:8000/change/'+uuid_code, 'plain', 'utf-8')
            
            subject = 'Python SMTP 邮件测试'
            message['Subject'] = Header(subject, 'utf-8')
            
            smtpObj.sendmail('407535695@qq.com', user.email,message.as_string())
            user.code_time = int(time.time())+1800
            user.code = uuid_code
            user.is_active=True  
            user.save()
            message = '修改成功'
            is_email_send = True
            print(is_email_send)
            
            
        else:
            # 获取全局的error信息,只显示第一个
            if forget_form.errors.get('__all__'):
                error = forget_form.errors.get('__all__')[0]    
    return render(request, 'forget.html', locals())


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    request.session.flush()
    return redirect("/")


@csrf_exempt
def student_info(request):
    title = '个人信息'
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有信息一说，跳去登录界面
        return redirect("/login/")
    username = request.session.get('username', None)
    user = models.User.objects.get(username=username)
    if request.method == 'GET':
        student_form = forms.StudentInfoForm(initial={
            'sex': user.sex,
            'province': user.province,
            'subject': user.subject,
            'score': user.score,
            'rank': user.rank,
        })
    if request.method == 'POST':
        student_form = forms.StudentInfoForm(request.POST)
        if student_form.is_valid():  # 判断是否填写完成
            user.sex = student_form.cleaned_data['sex']
            user.province = student_form.cleaned_data['province']
            user.subject = student_form.cleaned_data['subject']
            user.score = student_form.cleaned_data['score']
            user.rank = student_form.cleaned_data['rank']
            user.save()
            message = '修改成功'
            request.session['student_type'] = student_form.cleaned_data['subject']
    return render(request, 'student_info.html', locals())




@csrf_exempt
def change(request,uuid):
    title = '修改密码'
    error = ''
    change_form = forms.ChangeForm()
    is_timeover = False
    if request.method == 'GET':
        user = models.User.objects.filter(code= uuid).first()
        if user is None :
            is_timeover = True
        elif user.code_time < time.time():
            user.code = None
            user.code_time = None
            user.save()
            is_timeover = True
    
        
    if request.method == 'POST': 
        change_form = forms.ChangeForm(request.POST)
        if change_form.is_valid():  # 判断是否填写完成
           
           
            user = models.User.objects.filter(code= uuid).first()
            user.password=change_form.cleaned_data['password1']
            user.is_active=True
            print('3')  
            user.save()
            message = '修改成功'
            return redirect('/login/')
        
        else:
            # 获取全局的error信息,只显示第一个
            if  change_form.errors.get('__all__'):
                error = change_form.errors.get('__all__')[0]    
    return render(request, 'change.html', locals())
