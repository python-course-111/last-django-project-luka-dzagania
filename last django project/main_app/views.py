from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm
from .models import Contact
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import asyncio
from django.http import JsonResponse
import httpx
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail.message import EmailMessage
from django.core import mail
from django.conf import settings


def index(request):
    return render(request, './index.html')


def about(request):
    if not request.user.is_authenticated:
        messages.error(request, 'please log in and try again')
        return redirect('/login.html')
    return render(request, './about.html',)



def contact(request):
    if not request.user.is_authenticated:
        messages.error(request, 'please log in and try again')
        return redirect('/login.html')
    if request.method == "POST":
        name = request.POST.get('firstName')
        surname = request.POST.get('LastName')
        email = request.POST.get('email')
        phone = request.POST.get('num')
        description = request.POST.get('description')
        fullname = f'{name} {surname}'
        contact_query = Contact(
            name=name, surname=surname, email=email, number=phone, message=description)
        contact_query.save()
        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        email_mesge = mail.EmailMessage(f'Website Email from {fullname}', f'Email from : {email}\nUser Query :{description}\nPhone No : {phone}', from_email, ['lukadzagaia@gmail.com'], connection=connection)
        email_user = mail.EmailMessage('A+ Company', f'Hello {fullname}\nThanks fo Contacting Us Will Resolve Your Query Asap\nThank You', from_email, [email], connection=connection)
        connection.send_messages([email_mesge, email_user])
        connection.close()
        messages.info(request, "Thanks for Contacting Us ")
        return redirect('/contact.html')
    return render(request, './contactPage.html')


def blog(request):
    contacts = Contact.objects.all()
    return render(request, './blog.html', {'contacts': contacts})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration success!")
            return redirect("/login.html")
        messages.error(
            request, "Registration unsuccessful, invaild information!")
    form = NewUserForm()

    return render(request=request, template_name="./auth/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()

    return render(request=request, template_name="./auth/login.html", context={"login_form": form})


def catalog(request):
    a=['mmorpg', 'shooter', 'strategy', 'moba', 'racing', 'sports', 'social', 'sandbox', 'open-world', 'survival', 'pvp', 'pve', 'pixel', 'voxel', 'zombie', 'turn-based', 'first-person', 'third-Person', 'top-down', 'tank', 'space', 'sailing', 'side-scroller', 'superhero', 'permadeath', 'card', 'battle-royale', 'mmo', 'mmofps', 'mmotps', '3d', '2d', 'anime', 'fantasy', 'sci-fi', 'fighting', 'action-rpg', 'action', 'military',' martial-arts', 'flight', 'low-spec', 'tower-defense', 'horror', 'mmorts']
    if 'search' in request.GET:
        requested_game=request.GET.get('search')
        game = httpx.get(f"https://www.cheapshark.com/api/1.0/games?title={requested_game}")
        game = game.json()
        len_games=len(game)
        if len_games>9:
            game=game[0:9]
            len_games=9
        price=[]
        name=[]
        images=[]
        steam_name=[]
        for i in game:
            price.append(i['cheapest'])
        for i in game:
            name.append(i['external'])
        for i in game:
            images.append(i['thumb'])
        for i in name:
            j=i.replace(' ','+')
            steam_name.append(j)
        return render(request, "./catalog.html", {'result': game,'price':price,'name':name,'image':images,'len_games':len_games,'steam_name':steam_name})
    return render(request, "./catalog.html")