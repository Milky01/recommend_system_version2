from django import forms
from django.core.exceptions import ValidationError
from . import models



class RegisterForm(forms.Form):
    # 校验两次密码是否相同等
    def clean(self):
        username = self.cleaned_data.get('username')
        user = models.User.objects.filter(username=username).first()
        if user:
            raise ValidationError('用户名已存在')
        user_email = self.cleaned_data.get('email')
        email = models.User.objects.filter(email=user_email).first()
        if email:
            raise ValidationError('该邮箱已经被注册')
        pwd = self.cleaned_data.get('password1')
        re_pwd = self.cleaned_data.get('password2')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')

    username = forms.CharField(label="用户名", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入用户名小于30个字符"}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="电子邮箱", max_length=256,
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入电子邮箱"}))                            

class ForgetForm(forms.Form):
    # 校验两次密码是否相同等
    def clean(self):
        email = self.cleaned_data.get('email')
        user = models.User.objects.filter(email=email)
        if not user:
            raise ValidationError('该邮箱不存在')
        pwd = self.cleaned_data.get('password1')
        re_pwd = self.cleaned_data.get('password2')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')
    email = forms.CharField(label="邮箱账号", max_length=256,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入邮箱号"}))
    
    
class ChangeForm(forms.Form):
    # 校验两次密码是否相同等
    def clean(self):
        pwd = self.cleaned_data.get('password1')
        re_pwd = self.cleaned_data.get('password2')
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')
    password1 = forms.CharField(label="新密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    


class LoginForm(forms.Form):
    # 校验账号密码
    def clean(self):
        username = self.cleaned_data.get('username')
        user = models.User.objects.filter(username=username).first()
        if not user:
            raise ValidationError('该用户名尚未注册')
        else:
            if user.password != self.cleaned_data.get('password'):
                raise ValidationError('密码输入错误')
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class StudentInfoForm(forms.Form):
    sex_gender = (
        ('男', "男"),
        ('女', "女"),
    )
    province_gender = (
        ('广东', '广东'),
    )
    subject_gender = (
        ('物理类', '物理类'),
        ('历史类', '历史类'),
    )
    # sex = forms.ChoiceField(label='', choices=sex_gender)
    # province = forms.ChoiceField(label='省份', choices=province_gender)
    # subject = forms.ChoiceField(label='科别', choices=subject_gender)
    sex = forms.ChoiceField(label='性别',choices=sex_gender, widget=forms.Select(attrs={'class':'form-control input-lg'}))
    province = forms.ChoiceField(label='省份',choices=province_gender, widget=forms.Select(attrs={'class':'form-control input-lg'}))
    subject = forms.ChoiceField(label='考生类型',choices=subject_gender, widget=forms.Select(attrs={'class':'form-control input-lg'}))
    score = forms.IntegerField(label='高考分数', max_value=800, min_value=0, widget=forms.NumberInput(attrs={'class':'form-control input-lg'}))
    rank = forms.IntegerField(label='高考排位',max_value=800000,min_value=1,widget=forms.NumberInput(attrs={'class':'form-control input-lg'}))
