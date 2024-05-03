from django.shortcuts import render,redirect
import random , string , datetime
from .models import *
from django.contrib import messages
import logging
from django.views.decorators.cache import never_cache

logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@never_cache
def home(request):
    if request.session.has_key('session_key'):
        if request.method=="POST":
            srch = request.POST.get("search")
            # print(type(srch))
            if srch=="":
                return redirect("home")
            else:
            
                std2 = Student.objects.filter(name__icontains=srch).values()
                if std2:
                    return render(request,'home.html',context={"std":std2,"srch":srch})
                else:
                    return redirect("home")
        else:    
            # std2 = Student.objects.all().values()
            std2 = Student.objects.all().order_by('-id').values()
            
            return render(request,'home.html',context={"std":std2})
    else:
        return redirect("login")

def delete_student(request,pk):
    if request.session.has_key('session_key'):
        del_std = Student.objects.get(id=pk)
        logger.info(f'Request[delete_student]: student_detail = {del_std}')
        del_std.delete()
        response = {"status":True,"message":"student deleted successfully"}
        logger.info(f'Response[delete_student]: {response}')
        return redirect('home')
    else:
        return redirect("login")

def add_student(request):
    if request.session.has_key('session_key'):
        if request.method=="POST":
            nam = request.POST.get("name")
            ag = request.POST.get("age")
            emal = request.POST.get("email")
            gndr = request.POST.get("gender")
            stts = request.POST.get("status")
            user_name=request.session.get('user_name')
            user_time=datetime.datetime.now()
            logger.info(f'Request[add_student]: name={nam} , age={ag}, email ={emal}, gender={gndr}, status = {stts}, login_username = {user_name}')
            print(nam,ag,emal,gndr,stts,user_name,user_time)
            std=Student.objects.create(name=nam.capitalize(),age=ag,email=emal,gender=gndr,created_by=user_name,created_at=user_time,status=stts)
            std.save()
            response = {"status":True,"message":"student added successfully"}
            logger.info(f'Response[add_student]: {response}')
            return redirect("home")
    
        else:
            return render(request,'index2.html')
    else:
        response = {"status":False,"message":"User not have session key"}
        logger.exception(f'Response[add_student]: {response}')
        return redirect("login")
    
def update_student(request,pk):
    if request.session.has_key('session_key'):
        updt = Student.objects.get(id=pk)
        logger.info(f'Request[update_student]: {updt}')
        if request.method=="POST":
            nam = request.POST.get("name")
            ag = request.POST.get("age")
            emal = request.POST.get("email")
            gndr = request.POST.get("gender")
            stts = request.POST.get("status")
            editor_name=request.session.get('user_name')
            edit_time=datetime.datetime.now()


            updt.name = nam
            updt.age = ag
            updt.email = emal
            updt.gender = gndr
            updt.updated_by=editor_name
            updt.updated_at=edit_time
            updt.status = stts

            updt.save()
            response = {"status":True,"message":"student updated successfully"}
            logger.info(f'Response[update_student]: {response}')
            return redirect("home")
        else:
            return render (request,'index2.html')
        
    else:
        response = {"status":False,"message":"User not have session key"}
        logger.exception(f'Response[update_student]: {response}')
        return redirect("login")
    

def login(request):
    char_set=string.ascii_uppercase + string.digits
    session_key=''.join(random.sample(char_set * 20, 20))
    
    if request.method=="POST":
        uname = request.POST.get('username')
        pswrd = request.POST.get('password')
        logger.info(f'Request[login]: username = {uname} , password = {pswrd}')
        # print(uname , pswrd)
        obj = LoginUser.objects.get(username=uname)
        if obj.password==pswrd:
            
            request.session['user_name']=obj.username
            request.session['user_id']=obj.id
            request.session['session_key']=session_key
            
            obj.save()
            # print('===========>')
            response = {"status":True,"message":"student logged in  successfully"}
            logger.info(f'Response[login]: {response}')
            return redirect('home')
        else:
            messages.error(request,"wrong password")
            response = {"status":False,"message":"student entered wrong password"}
            logger.info(f'Response[login]: {response}')
            return redirect('login')

    return render(request,'login2.html')

def logout(request):
    if request.session.has_key('session_key'):
        del request.session['session_key']
        # print("=================>  logout" )
        response = {"status":True,"message":"student logged out successfully"}
        logger.info(f'Response[logout]: {response}')
        return redirect('login')
    else:
        # print("=================>  logout" )
        response = {"status":False,"message":"User not have session key"}
        logger.exception(f'Response[logout]: {response}')
        return redirect('login')
    

@never_cache
def add_data_template(request):
    if request.session.has_key('session_key'):
        if request.method=="POST":
            nam = request.POST.get("name")
            ag = request.POST.get("age")
            emal = request.POST.get("email")
            gndr = request.POST.get("gender")
            stts = request.POST.get("status")
            user_name=request.session.get('user_name')
            user_time=datetime.datetime.now()
            logger.info(f'Request[add_data_template]: name={nam} , age={ag}, email ={emal}, gender={gndr}, status = {stts}, login_username = {user_name}')
            # print(nam,ag,emal,gndr,stts,user_name,user_time)
            std=Student.objects.create(name=nam.capitalize(),age=ag,email=emal,gender=gndr,created_by=user_name,created_at=user_time,status=stts)
            std.save()
            response = {"status":True,"message":"student added successfully"}
            logger.info(f'Response[add_data_template]: {response}')
            return redirect("home")
    
        else:
            return render(request,'add_student.html')
    else:
        response = {"status":False,"message":"User not have session key"}
        logger.exception(f'Response[add_data_template]: {response}')
        return redirect("login")
    