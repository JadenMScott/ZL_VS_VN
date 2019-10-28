from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return redirect('/login')
def logout(request):
    request.session.clear()
    return redirect('/login')
def login(request):
    if request.method == "GET":
        return render(request, 'main/log_and_reg.html')
    elif request.method == "POST":
        # this is the email of the user that is put into the login page
        user = Users.objects.filter(email=request.POST['log_email'])
        if len(user) > 0:
            testpass = user.first().password
            # password field from the login page
            if bcrypt.checkpw((request.POST['log_pass']).encode(), testpass.encode()):
                # this is the user put in the login username field 
                request.session['user'] = Users.objects.get(email=request.POST['log_email']).id
                return redirect('/dashboard')
            else:
                messages.error(request, 'Incorrect Credentials')
                return redirect('/login')
        else:
            messages.error(request, 'Incorrect Credentials')
            return redirect('/login')
def register(request):
    errors = Users.objects.Pass_validator(request.POST)
    if len(errors) > 0:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        # password for the registration page
        print(request.POST['reg_pass'])
        passw = request.POST['reg_pass']
        pw_hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt())
        print(pw_hash)
        # this is creating the user so pretty much just read the tag its creating and put in the info needed
        Users.objects.create(
            username=request.POST['reg_username'],
            email=request.POST['reg_email'],
            phone=str(request.POST['reg_phone']),
            password=pw_hash,
            first_name=request.POST['reg_first_name'],
            last_name=request.POST['reg_last_name']
        ) 
        return redirect("/login")
def createpros(request):
    errors = Prospects.objects.pros_validator(request.POST)
    if len(errors) > 0:
        for (key,value) in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        # creates a prospect from the page once you are logged in
        Prospects.objects.create(
            # name of the prospect
            name = request.POST['pros_name'],
            # followup in the propects submission
            followup = request.POST['pros_followup'],
            # address in the prospects submission page
            address = request.POST['pros_address'],
            # phone number in the submissions page
            phone = request.POST['pros_phone'],
            # email from submissions page
            email = request.POST['pros_email'],
            # step in the sales proccess
            step = request.POST['pros_step'],
            # add a s to the end of user
        )
        Prospects.objects.last().users.add(Users.objects.get(id=request.session['user']))
        if 'pros_notes' in request.POST:
            Notes.objects.create(
                notes=request.POST['pros_notes'],
                Prospect=Prospects.objects.last()
            )
        return redirect('/dashboard')

def dashboard(request):
    if 'user' in request.session:
        currentUser = Users.objects.get(id=request.session['user'])
        context = {
            # youll need these to pass the info from the back end to the front end on the dashboard
            'user' : currentUser,
            'prospects' : Prospects.objects.filter(users = currentUser),
        }
        return render(request, 'main/dashboard.htm', context)
    else:
        return redirect('/login')

def prospect(request, id):
    if 'user' in request.session:
        currentUser = Users.objects.get(id=id)
        if currentUser in Prospects.objects.get(id=id).users.all():
            context = {
                'user' : currentUser,
                'prospect' : Prospects.objects.get(id=id),
            }
            return render(request, 'main/single.htm', context)
        else:
            return redirect('/dashboard')
    else:
        return redirect("/login")

def note(request,id):
    if 'user' in request.session:
        if request.method=="POST":
            Notes.objects.create(notes=request.POST['more_pros_note'],Prospect=Prospects.objects.get(id=id))
            return redirect(f"/prospects/{id}")
        else:
            return render(request,"main/single.htm")
    else:
        return redirect('/login')