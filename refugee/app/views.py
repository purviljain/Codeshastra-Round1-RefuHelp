from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event
from .models import Refugee, NGO, NgoPetition, NgoPetitionVote, Help, Notification, RefugeePetition, RefugeePetitionVote
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail


def login(request):
    if request.user.is_authenticated:
        return render(request, 'app/profile.html', {})
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return render(request, 'app/profile.html', {})
                else:
                    error = 'Your Rango account is disabled.'
                    return render(request, 'app/login.html', {'error': error})
            else:
                error = 'Incorrect Username or Password'
                return render(request, 'app/login.html', {'error': error})
        else:
            return render(request, 'app/login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('app:login'))


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        FirstName = request.POST.get('fname', '')
        LastName = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        name = FirstName + " " + LastName
        user = User.objects.create_user(username=username, email=email, first_name=FirstName, last_name=LastName)
        user.set_password(password)
        user.save()
        country = request.POST.get('country', '')
        bio = request.POST.get('bio', '')
        age = request.POST.get('age', '')
        mobileNo = request.POST.get('mobileNo', '')
        gender = request.POST.get('gender', '')
        passport = request.FILES.get('passport', None)
        photo = request.FILES.get('photo', None)
        refugee = Refugee.objects.create(refugee=user, country=country, bio=bio, age=age, mobileNo=mobileNo,
                                         gender=gender, passport=passport, photo=photo, name=name)
        refugee.save()
        return HttpResponse("avh")
    else:
        return render(request, 'app/registration.html', {})


def ngo_register(request):
    if request.user.is_authenticated:
        return render(request, 'app/test.html', {})
    if request.method == 'GET':
        return render(request, "app/ngo_register.html", {})
    name = request.POST.get("name")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if User.objects.filter(username=name).exists():
        error = 'The NGO is already registered.'
        return render(request, 'app/ngo_register.html', {'error': error})
    user = User.objects.create_user(username=name, email=email)
    user.set_password(password)
    user.save()
    country = request.POST.get("country", "")
    ngo_id = request.POST.get("ngo_id", "")
    ngo = NGO.objects.create(user=user, name=name, country=country, ngo_id=ngo_id)
    ngo.save()
    auth_login(request, user)
    return redirect('app:ngo_profile', pk=user.id)


@login_required(login_url="app:ngo_login")
def ngo_profile(request, pk):
    ngo = get_object_or_404(NGO, id=pk)
    return render(request, 'app/ngo_profile.html', {'ngo': ngo})


def ngo_login(request):
    if request.user.is_authenticated:
        return redirect('app:ngo_profile', pk=request.user.ngo.id)
    if request.method == 'GET':
        return render(request, 'app/ngo_login.html', {})
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return redirect('app:ngo_profile', pk=user.ngo.id)
    else:
        error = 'The NGO does not exist.'
        return render(request, 'app/ngo_login.html', {'error': error})


def ngo_logout(request):
    auth_logout(request)
    return redirect(reverse('app:ngo_login'))


@login_required(login_url='/login/')
def profile(request, idx):
    client = get_object_or_404(Refugee, pk=idx)
    return render(request, 'app/refugee_profile.html', {'client': client})


def askforhelp(request):
    if request.method == 'POST':
        name = request.user.get_username()
        idd = request.user.id
        ngo_name = request.POST.get("askto", "")
        print(ngo_name)
        helpof = request.POST.get("helpof", "")
        urgency = request.POST.get("urgency", "")
        description = request.POST.get("description", "")
        myhelp = Help()
        current_refugee = Refugee.objects.get(refugee__username=name)
        myhelp.asker = current_refugee
        myhelp.askto = NGO.objects.get(name=ngo_name)
        myhelp.helpof = helpof
        myhelp.urgency = urgency
        myhelp.description = description
        return redirect('app:profile', idx=idd)
    else:
        name = request.user.get_username()
        current_refugee = Refugee.objects.get(refugee__username=name)
        name = request.user.get_username()
        country = current_refugee.country
        return render(request, 'app/askforhelp.html', {'all_ngo': NGO.objects.filter(country=country)})


def view_ngo_petition(request, pk):
    petition = get_object_or_404(NgoPetition, id=pk)
    return render(request, 'app/petition.html', {'petition': petition})


def vote_ngo_petition(request, pk):
    if request.method == 'GET':
        return redirect('app:view_ngo_petition', pk=pk)
    email = request.POST.get('email')
    petition = NgoPetition.objects.get(id=pk)
    if NgoPetitionVote.objects.filter(petition=petition, voter=email).exists():
        return redirect('app:view_ngo_petition', pk=pk)
    petition = NgoPetition.objects.get(id=pk)
    vote = NgoPetitionVote.objects.create(petition=petition, voter=email)
    vote.save()
    send_mail(
        'Verify your vote',
        'http://127.0.0.1:8000/petition/ngo/vote/{0}/success/'.format(vote.id),
        'from@example.com',
        ['test@example.com'],
        fail_silently=False,
    )
    return redirect('app:vote_message')


def vote_message(request):
    return render(request, 'app/vote_message.html', {})


def confirm_email(request, pk):
    vote = NgoPetitionVote.objects.get(id=pk)
    vote.email_confirmed = True
    vote.save()
    return HttpResponse('Your vote has been confirmed.')


@login_required(login_url='app:ngo_login')
def create_ngo_petition(request):
    if request.method == 'GET':
        return render(request, 'app/create_ngo_petition.html', {})
    title = request.POST.get('title')
    description = request.POST.get('description')
    petition = NgoPetition.objects.create(title=title, description=description, ngo=request.user.ngo)
    petition.save()
    return redirect('app:view_ngo_petition', pk=petition.id)


def search_ngo(request):
    if request.GET.get('search_ngo'):
        param = request.GET.get('search_ngo')
        ngo = NGO.objects.filter(name__icontains=param)
        if not ngo.exists():
            return render(request, 'app/search_ngo.html', {'error': 'NO MATCHING QUESTIONS FOUND'})
        return render(request, 'app/search_ngo.html', {'ngo': ngo})
    return render(request, 'app/search_ngo.html', {})


@login_required(login_url="app:ngo_login")
def search_refugee(request):
    if request.GET.get('search_refugee'):
        param = request.GET.get('search_refugee')
        r = Refugee.objects.filter(name__icontains=param)
        if not r.exists():
            return render(request, 'app/search_refugee.html', {'error': 'NO MATCHING QUESTIONS FOUND'})
        return render(request, 'app/search_refugee.html', {'r': r})
    return render(request, 'app/search_refugee.html', {})


@login_required(login_url="app:ngo_login")
def add_notif(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        r = NGO.objects.get(user=request.user)
        n = Notification(message=message, askedBy=r)
        n.save()
        return HttpResponse("avh")
    else:
        return render(request, 'app/addnotif.html', {})


@login_required(login_url="app:ngo_login")
def allnotifs(request):
    notif = Notification.objects.all()
    return render(request, 'app/allnotifs.html', {'notif': notif})


@login_required(login_url="app:ngo_login")
def add_event(request):
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        date = request.POST.get('date', '')
        location = request.POST.get('location', '')
        r = NGO.objects.get(user=request.user)
        n = Event(reason=reason, startedBy=r, date=date, location=location)
        n.save()
        return HttpResponse("avh")
    else:
        return render(request, 'app/addevent.html', {})


def all_event(request):
    event = Event.objects.all()
    return render(request, 'app/allevents.html', {'event': event})


def view_refugee_petition(request, pk):
    petition = get_object_or_404(RefugeePetition, id=pk)
    return render(request, 'app/refugee_petition.html', {'petition': petition})


def vote_refugee_petition(request, pk):
    if request.method == 'GET':
        return redirect('app:view_refugee_petition', pk=pk)
    email = request.POST.get('email')
    petition = RefugeePetition.objects.get(id=pk)
    if RefugeePetitionVote.objects.filter(petition=petition, voter=email).exists():
        return redirect('app:view_refugee_petition', pk=pk)
    petition = RefugeePetition.objects.get(id=pk)
    vote = RefugeePetitionVote.objects.create(petition=petition, voter=email)
    vote.save()
    send_mail(
        'Verify your vote',
        'http://127.0.0.1:8000/petition/refugee/vote/{0}/success/'.format(vote.id),
        'from@example.com',
        ['test@example.com'],
        fail_silently=False,
    )
    return redirect('app:vote_message')


def refugee_confirm_email(request, pk):
    vote = RefugeePetitionVote.objects.get(id=pk)
    vote.email_confirmed = True
    vote.save()
    return HttpResponse('Your vote has been confirmed.')


@login_required(login_url='app:login')
def create_refugee_petition(request):
    if request.method == 'GET':
        return render(request, 'app/create_refugee_petition.html', {})
    title = request.POST.get('title')
    description = request.POST.get('description')
    petition = RefugeePetition.objects.create(title=title, description=description, refugee=request.user.refugee)
    petition.save()
    return redirect('app:view_refugee_petition', pk=petition.id)
