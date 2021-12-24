from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import User
from . import models
from . import forms


def recommend_school(request):
    if not request.session.get('is_login', None):
        # 没登录去登录
        return redirect("/login/")
    title = '推荐学校'
    user = User.objects.get(username=request.session['username'])
    rank = user.rank
    page = 1
    if request.method == 'GET':
        page = request.GET.get('page')
        if request.GET.get('rank') is not None:
            rank = int(request.GET.get('rank'))
    if request.method == 'POST':
        # request.session['school_name'] = request.POST.get('school_name')
        request.session['province'] = request.POST.get('province')
        # request.session['student_type'] = request.POST.get('student_type')
        request.session['epoch'] = request.POST.get('epoch')
        request.session['student_type'] = request.POST.get('student_type')
        if request.POST.get('rank')!='':
            rank = int(request.POST.get('rank'))
    
    if rank < 20000:
        trank = 15000
        schools = models.School_info.objects.filter(
            student_type__contains=request.session['student_type'],
            epoch__contains=request.session['epoch'],
            school_province__contains=request.session['province'],
            lowest_rank__range=(rank*0.8, trank), 
            student_type=request.session['student_type']
            )
    else :
        step = int(rank*0.05)
        for i in range(0, 4*step, step):
            print(max(0,rank - i))
            schools = models.School_info.objects.filter(
                student_type__contains=request.session['student_type'],
                epoch__contains=request.session['epoch'],
                school_province__contains=request.session['province'],
                lowest_rank__range=(max(0,rank - i), rank + i), 
                student_type=request.session['student_type']
                )
            # if len(schools) > 30:
            #     break
    
    schools = sorted(schools)
    paginator = Paginator(schools, 25)
    schools = paginator.get_page(page)

    # school_form = forms.school_form(initial={
    #     'school_name': request.session['school_name'], 'province': request.session['province'],
    #     'student_type': request.session['student_type'], 'epoch': request.session['epoch']
    # })
    school_form = forms.school_form(initial={
        'province': request.session['province'],
        'student_type': request.session['student_type'], 
        'epoch': request.session['epoch'],
        'rank': rank
    })
    school_form.student_type = None
    return render(request, 'recommend_school.html', locals())
