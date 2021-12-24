from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from user.views import logout
from . import models
from . import forms


def search_school_profession(request):
    if not request.session.get('is_login', None):
        # 没登录去登录
        return redirect("/login/")
    user = User.objects.get(username=request.session['username'])
    rank = user.rank
    title = '推荐专业'
    page = 1
    if request.method == 'GET':
        page = request.GET.get('page')
        if request.GET.get('rank') is not None:
            rank = int(request.GET.get('rank'))
    if request.method == 'POST':
        request.session['profession_name'] = request.POST.get('profession_name')
        request.session['province'] = request.POST.get('province')
        request.session['student_type'] = request.POST.get('student_type')
        request.session['epoch'] = request.POST.get('epoch')
        if request.POST.get('rank')!='':
            rank = int(request.POST.get('rank'))
    if rank < 15000:
        trank = 10000
        schools = models.One_School.objects.filter(
            profession_name__contains=request.session['profession_name'],
            student_type__contains=request.session['student_type'],
            epoch__contains=request.session['epoch'],
            school_province__contains=request.session['province'],
            lowest_rank__range=(rank*0.8, trank), 
            student_type=request.session['student_type']
            )
    else :
        step = int(rank*0.05)
        for i in range(0, 6*step, step):
            schools = models.One_School.objects.filter(
                profession_name__contains=request.session['profession_name'],
                student_type__contains=request.session['student_type'],
                epoch__contains=request.session['epoch'],
                school_province__contains=request.session['province'],
                lowest_rank__range=(max(rank-2*step,rank - i), rank + i), 
                student_type=request.session['student_type']
                )
    schools = sorted(schools)

    paginator = Paginator(schools, 25)
    schools = paginator.get_page(page)

    school_form = forms.school_form(initial={
        'profession_name': request.session['profession_name'], 'province': request.session['province'],
        'student_type': request.session['student_type'],
        'epoch': request.session['epoch'],
        'rank':rank
    })
    school_form.student_type = None
    return render(request, 'search_school_profession.html', locals())
