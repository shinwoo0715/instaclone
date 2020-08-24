from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login # authenticate : 로그인 인증관련 기능,
from django.contrib.auth import logout as django_logout
from .forms import SignupForm , LoginForm



def signup(request):
    if request.method == 'POST' : 
        form = SignupForm(request.POST , request.FILES) # 뒤에 request.FILE을 받은 이유는 우리가 회원가입을 할때
        # 프로필도 받을 것이기 때문에 받은 것이다. 
        if form.is_valid():
            user = form.save()
            
            return redirect('accounts:login')
    else : # request.POST로 들어오지 않았다는 것은 오류사항이다. 
        form = SignupForm()
    
    return render(request, 'accounts/signup.html' , {
        'form'  : form ,
    })
    

def login_check(request ):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        name = request.POST.get('username') # username으로 보내진 값을 변수에 저장
        pwd = request.POST.get("password")

        user = authenticate(username=name , password=pwd) 

        if user is not None:
            login(request , user)
            return redirect("/")
        else: 
            return render(request , 'accounts/login_fail_info.html')
    else:
        form = LoginForm()
        return render(request , 'accounts/login.html' , {'form' : form})

def logout(request): # logout은 매우 간단하다 우리가 아까 import한 auth 이다. 
    django_logout(request)
    return redirect('/')
