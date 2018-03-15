from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import openpyxl
import os

from manager.forms import UserInfoForm
from account.models import UserInfo, ProApply, ProMiddle, ProConclude, UserProInfo


@permission_required('account.add_userproinfo',login_url="/account/login/")
def manager_home(request):
    return render(request, "manager/home.html")

@permission_required('account.add_userproinfo',login_url="/account/login/")
@csrf_exempt
def userlist(request):
    print("jinliale")
    if request.method == "GET":
        userinfo = UserInfo.objects.all()
        userinfo_form = UserInfoForm()
        return render(request,'manager/userlist.html',{'userinfo':userinfo,'userinfo_form':userinfo_form})

    if request.method == "POST":
        user = request.POST['user']
        password = 'szu'+str(user)[-6:]
        print(password)
        name = request.POST['name']
        sex = request.POST['sex']
        classID = request.POST['classID']
        major = request.POST['major']
        institute = request.POST['institute']
        user_obj = User.objects.filter(username=user)
        if user_obj:
            pass
        else:
            user = User.objects.create_user(username=user, password=password)
            user.save()
        user_instance = User.objects.get(username=user)
        userinfo_obj = UserInfo.objects.filter(user=user_instance)
        if userinfo_obj:
            return HttpResponse('2')
        else:
            UserInfo.objects.create(user=user_instance, name=name, sex=sex, classID=classID, major=major,
                                    institute=institute)
            return HttpResponse('1')


@permission_required('account.add_userproinfo',login_url="/account/login/")
@require_POST
@csrf_exempt
def del_userlist(request):
    user = request.POST['user_id']
    print(user)
    try:
        print("step1")
        user_obj = User.objects.get(username=user)
        if UserInfo.objects.filter(user=user_obj):
            print("step2")
            userinfo_obj = UserInfo.objects.get(user=user_obj)
            print("step3")

            if ProApply.objects.filter(pro_id=userinfo_obj.id):
                print("有申请")
                ProApply.objects.get(pro_id=userinfo_obj.id).delete()
                print("删申请")
            if ProMiddle.objects.filter(pro_id=userinfo_obj.id):
                print("有中期")
                ProMiddle.objects.get(pro_id=userinfo_obj.id).delete()
                print("删中期")
            if ProConclude.objects.filter(pro_id=userinfo_obj.id):
                print("有结题")
                ProConclude.objects.get(pro_id=userinfo_obj.id).delete()
                print("删结题")

            print("step4")
            userinfo_obj.delete()
            print("step5")
            user_obj.delete()
            print("step6")
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@permission_required('account.add_userproinfo',login_url="/account/login/")
def apply_infolist(request):
    infolist = []
    prolist = ProApply.objects.filter(status=2)
    print(prolist)
    for i in prolist:
        print(i.pro_id_id)
        pro_id = i.pro_id_id
        records = UserProInfo.objects.filter(id=pro_id)
        for k in records:
            dict = model_to_dict(k)
            user = k.user
            userinfo = UserInfo.objects.filter(user=user)
            for j in userinfo:
                name = j.name
            dict['user'] = user
            dict['name'] = name
            infolist.append(dict)
    return render(request, 'manager/infolist_apply.html',{'infolist': infolist})

