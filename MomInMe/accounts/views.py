# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import SignupFirstForm, SignupSecondForm, LoginForm
from .models import UserProfile

def signup_first(request):
    if request.method == 'POST':
        form = SignupFirstForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            request.session['username'] = username  # 세션에 username 저장
            request.session['password'] = password  # 세션에 password 저장
            return redirect('accounts:setup')  # 두 번째 단계로 리다이렉트
    else:
        form = SignupFirstForm()

    return render(request, 'signup.html', {'form': form})

def signup_second(request):
    username = request.session.get('username')
    password = request.session.get('password')

    if request.method == 'POST':
        form = SignupSecondForm(request.POST, request.FILES)
        if form.is_valid():
            # User 생성
            user = User.objects.create_user(username=username, password=password)

            # UserProfile 생성
            user_profile = form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            # 세션 데이터 삭제
            del request.session['username']
            del request.session['password']

            return redirect('accounts:login')  # 회원 가입 성공 후 로그인 페이지로 리다이렉트
    else:
        form = SignupSecondForm()

    return render(request, 'setup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # 사용자 인증
            user = authenticate(username=username, password=password)
            if user is not None:
                # 로그인 처리
                login(request, user)
                return redirect('mainpage:home')  # 로그인 성공 후 대시보드 페이지로 리다이렉트
            else:
                # 인증 실패 처리
                return render(request, 'login.html', {'form': form, 'error_message': '아이디 또는 비밀번호가 올바르지 않습니다.'})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})