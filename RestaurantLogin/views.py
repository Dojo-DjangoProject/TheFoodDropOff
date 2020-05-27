from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from RestaurantEvent.models import Event

def index(request):
    # render login form
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        return redirect('/userlogin')
    return render(request,'restaurant-login.html')

def register(request):
    # render registration form
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        return redirect('/userlogin')
    return render(request,'restaurant-registration.html')
    
def login(request):
    # process POST request to log in restaurant
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        return redirect('/userlogin')
    elif request.method == 'POST':
        errors = Restaurant.objects.pw_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/restaurantlogin')
        restaurant = Restaurant.objects.filter(email=request.POST['logemail']) 
        logged_in = restaurant[0]   
        request.session['restaurantID'] = logged_in.id
        return redirect('/restaurantlogin/welcome')
    return redirect('/')

def create(request):
    # process POST request to create new restaurant account
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            return redirect('/restaurantlogin/welcome')
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        return redirect('/userlogin')
    elif request.method == 'POST':
        errors = Restaurant.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/restaurantlogin/register')
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        newlocation=Location.objects.create(
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code']
        )
        newrestaurant = Restaurant.objects.create(
            restaurant_name=request.POST['restaurant_name'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            cuisine=request.POST['cuisine'],
            phone_number=request.POST['phone_number'],
            email_address=request.POST['email'],
            password=pw_hash,
            location_id=newlocation.id
        )        
        request.session['restaurantID'] = newrestaurant.id
        return redirect('/restaurantlogin/welcome')
    return redirect('/')

def welcome(request):
    # render welcome page
    if 'restaurantID' in request.session:
        restaurant = Restaurant.objects.filter(id=request.session['restaurantID'])
        if restaurant:
            restaurant = Restaurant.objects.get(id=request.session['restaurantID'])
            context = {
                'one_restaurant': restaurant,
            }
            return render(request,'restaurant-welcome.html',context)
        else:
            request.session.flush()
            return redirect('/')
    elif 'userID' in request.session:
        return redirect('/userlogin')
    return redirect('/')

def testunique(request):
    # check email uniqueness and return result to ajax
    email = request.GET.get("email", None)
    print(email)
    if Restaurant.objects.filter(email_address__iexact=email).exists():
        return JsonResponse({"used":True}, status = 200)
    else:
        return JsonResponse({"used":False}, status = 200)

def testlogin(request):
    # check login credentials and return result to ajax
    errors = Restaurant.objects.pw_validator(request.POST)
    print(errors)
    if len(errors)>0:
        return JsonResponse({"match":False}, status = 200)
    else:
        return JsonResponse({"match":True}, status = 200)

def logout(request):
    request.session.flush()
    return redirect('/')