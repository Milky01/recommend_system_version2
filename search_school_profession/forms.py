from django import forms


class school_form(forms.Form):
    province_gender = (
        ('', "全部"),
        ('广东', "广东"),
        ('安徽', "安徽"),
        ('澳门', "澳门"),
        ('北京', "北京"),
        ('福建', "福建"),
        ('甘肃', "甘肃"),
        ('广西', "广西"),
        ('贵州', "贵州"),
        ('海南', "海南"),
        ('河北', "河北"),
        ('江西', "江西"),
        ('河南', "河南"),
        ('黑龙江', "黑龙江"),
        ('湖北', "湖北"),
        ('湖南', "湖南"),
        ('吉林', "吉林"),
        ('江苏', "江苏"),
        ('辽宁', "辽宁"),
        ('内蒙古', "内蒙古"),
        ('宁夏', "宁夏"),
        ('青海', "青海"),
        ('山东', "山东"),
        ('山西', "山西"),
        ('陕西', "陕西"),
        ('上海', "上海"),
        ('四川', "四川"),
        ('天津', "天津"),
        ('西藏', "西藏"),
        ('香港', "香港"),
        ('新疆', "新疆"),
        ('云南', "云南"),
        ('浙江', "浙江"),
        ('重庆', "重庆"),
    )
    student_gender = (
        ('物理类', '物理类'),
        ('历史类', '历史类'),
    )
    epoch_gender = (
        ('本科批', '本科批'),
        ('专科批', '专科批'),
        ('本科提前批', '本科提前批'),
        ('专科提前批', '专科提前批'),
    )

    # school_name = forms.CharField(label="院校名称", empty_value='',max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profession_name = forms.CharField(label="专业名称", empty_value='',max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    province = forms.ChoiceField(label='省份', choices=province_gender, widget=forms.Select(attrs={'class':'form-control'}))
    epoch = forms.ChoiceField(label='录取批次', choices=epoch_gender, widget=forms.Select(attrs={'class':'form-control'}))
    student_type = forms.ChoiceField(label='考生类型', choices=student_gender, widget=forms.Select(attrs={'class':'form-control'}))
    rank = forms.CharField(label="排位", max_length=256,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
