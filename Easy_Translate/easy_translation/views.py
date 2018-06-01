from django.shortcuts import render,redirect
from easy_translation.models import user_info,diary
from translate import Translator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import FileResponse
# Create your views here.
language = {"中文":"zh","英语":"en","日语":"ja","韩语":"ko","法语":"fr","德语":"de","意大利语":"it","俄语":"ru","西班牙语":"es","葡萄牙语":"pt"}
list = ["中文","英语","日语","韩语","法语","德语","意大利语","俄语","西班牙语","葡萄牙语"]
diarys = {}
flag = False
username = ''

def register(req):
    userinfo = {}
    msg = ''
    if req.method=='POST':
        userinfo['name'] = req.POST['name']
        userinfo['password'] = req.POST['password']
        user = user_info.objects.filter(name=userinfo['name']).count()
        if user:
            msg = '该用户名已存在'
            return redirect('/register/',{'msg':msg})
        user_info.objects.create(**userinfo)
        return redirect('/login/')
    return render(req,'register.html')

def login(req):
    msg = ''
    if req.method == 'POST':
        username = req.POST['name']
        password = req.POST['password']
        try:
            user = user_info.objects.get(name=username,password=password) #通过数据库验证
            if user:
                #设置session内部字典内容
                req.session['is_login'] = 'True'
                req.session['username'] = username
                return redirect('/user_home/')
        except Exception as e:
            msg = '账号或密码错误'

    return render(req,'login.html',{'msg':msg})

def logout(req):
    try:
        del req.session['is_login']
    except KeyError:
        pass
    return redirect('/login/')

#登录验证装饰器
def auth(func):
    def warrper(req,*args,**kwargs):
        try:
            is_login = req.session.get('is_login',False)
            print(is_login)
            if not is_login:
                return redirect('/login/')
            return func(req,*args,**kwargs)
        except Exception as e:
            return redirect('/login/')
    return warrper


def home(req):
    return render(req,'home.html')

@auth
def changepwd(req):
    username = req.session['username']
    user = user_info.objects.get(name=username)
    if req.method == 'POST':
        oldpwd = req.POST['oldpwd']
        if oldpwd != user.password:
            return redirect('/changepwd/')
        newpwd = req.POST['newpwd']
        user.password = newpwd
        user.save()
        return render(req,'changepwd_done.html')
    return render(req,'changepwd.html')

@auth
def user_home(req):
    username = req.session['username']
    users = user_info.objects.filter(name=username).values('id')
    users_info = users[0]
    user_id = users_info['id']
    a_diary = diary.objects.filter(User_info_id=user_id).last()
    title = a_diary.title
    text = a_diary.text
    time = a_diary.dtime
    return render(req,'user_home.html',{'username':username,'title':title,'text':text,'time':time})


@auth
def translate(req):
    username = req.session['username']
    if req.method=='POST':
        from_lang=req.POST.get('from_language')
        to_lang=req.POST.get('to_language')
        texts = req.POST.get('texts')
        translator = Translator(from_lang=language[from_lang],to_lang=language[to_lang])
        translation = translator.translate(texts)
        return render(req,'translate.html',{'translation':translation,'username':username,'list':list})
    return render(req,'translate.html',{'username':username,'list':list})


@auth
def Diary(req):
    username = req.session['username']
    if req.method == 'POST':
        users = user_info.objects.filter(name=username).values('id')
        user_id = users[0]
        title = req.POST.get('title')
        text = req.POST.get('text')
        diarys['title']=title
        diarys['text']=text
        diarys['User_info_id']=user_id['id']
        diary.objects.create(**diarys)
    return render(req,'diary.html',{'username':username})

@auth
def showdiary(req):
    username = req.session['username']
    users = user_info.objects.filter(name=username).values('id')
    user_id = users[0] #得到{'id':id}
    user_id = user_id['id']
    all_diary = diary.objects.filter(User_info_id=user_id).values('title')
    current_page = req.GET.get('p')
    paginator = Paginator(all_diary,5)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(req, 'showdiary.html', {'posts':posts})

@auth
def diarytext(req):
    username = req.session['username']
    titles = req.GET.get('title')
    a_diary = diary.objects.get(title=titles)
    text = a_diary.text
    time = a_diary.dtime
    return render(req, 'diarytext.html', {'username':username,'title':titles, 'text':text, 'time':time})


@auth
def deleteit(req):
    titles = req.GET.get('title')
    a_diary = diary.objects.get(title=titles)
    a_diary.delete()
    return redirect('/showdiary.html')




def file_down(request):
    file=open('static/Quick词典.zip','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="Quick词典.zip"'
    return response