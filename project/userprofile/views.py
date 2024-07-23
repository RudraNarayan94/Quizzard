from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,authenticate,login,logout
#from django.contrib.auth.decorators import login_required
from .models import UserProfileModel,UserAchievementModel

# Create your views here.
def home_view(request):
    if request.method == 'POST':
        if get_user_model().objects.filter(username=request.POST.get('username')).exists():
            return redirect('profile_view', request.POST.get('username'))
    if request.user.is_authenticated:
        quiz_data = QuizModel.objects.exclude(user__pk=request.user.pk)
        return render(request, 'home.html',context={"request":request,"user":request.user,"quizzes":quiz_data})
    else:
        return redirect('login_view')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_instance = authenticate(username=username, password=password)
        if user_instance is not None:
            login(request,user_instance)
            return redirect('home_view')
        else:
            print("Invalid username or password")
            return redirect('login_view')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user_instance = get_user_model().objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        user_instance.set_password(password)
        user_instance.save()
        UserProfileModel.objects.create(user=user_instance) 
        UserAchievementModel.objects.create(user=user_instance) 
        return redirect('login_view')
    return render(request, 'signup.html')
  
def logout_view(request):
  logout(request)
  return redirect('login_view')

def profile_view(request,username):
    user_instance = get_user_model().objects.get(username=username)
    data = {
        "is_user_profile": True if request.user.username == username else False,
        "quizzes_created_count":user_instance.QuizModel_user.all().count(),
        "quizzes_participated_count":user_instance.ParticipateModel_user.quiz.all().count(),
        "correct_answers_count":user_instance.UserAchievementModel_user.correct_answers,
        "achievement":user_instance.UserAchievementModel_user.all(),
        "user_created":user_instance.QuizModel_user.all(),
        "user_participated":user_instance.ParticipateModel_user.quiz.all()
    }
    print(data['is_user_profile'])
    return render(request, 'profile.html',context={"request":request,"user":user_instance,"data":data})

def update_user_profile(request):
    user_instance= request.user
    if request.method == 'POST':
        user_instance.first_name = request.POST.get('first_name')
        user_instance.last_name = request.POST.get('last_name')
        if request.POST.get('username') != request.user.username:
            if get_user_model().objects.filter(username=request.POST.get('username')).exists():
                print("Username already taken")
            else:
                user_instance.username = request.POST.get('username')
        user_profile_instance = user_instance.UserProfileModel_user
        user_profile_instance.bio = request.POST.get('bio')
        if len(request.FILES) != 0:
            user_profile_instance.profile_picture = request.FILES['profile_picture']
        user_profile_instance.save()
        user_instance.save()
        return redirect('profile_view',username=request.user.username)
    return render(request, 'update_user_profile.html',context={"request":request,"user":request.user})

def update_password_view(request):
    user_instance = request.user
    if request.method == 'POST':
        user_check = authenticate(username=user_instance.username,password=request.POST.get('password'))
        if user_check is not None:
            if request.POST.get('new_password') == request.POST.get('new_password_check'):
                user_instance.set_password(request.POST.get('new_password'))
                user_instance.save()
        return redirect('profile_view',request.user.username)
    return render(request, 'update_password.html',context={"request":request,"user":request.user})

def delete_profile_view(request):
    request.user.delete()
    return redirect('login_view')