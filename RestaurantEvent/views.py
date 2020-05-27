from django.shortcuts import render, HttpResponse, redirect
from .models import Restaurant, RestaurantManager, Event
from Location.models import *
from django.contrib import messages
import datetime

#Used for debugging, turn to true to turn off check if a restaurant is logged in
debug = True

def index(request):

    # Sort by most recent day
    context = {
        'events' : Event.objects.all()
    }
    return render(request,'events.html',context)

#Route is /event/new/create
def createEvent(request):
    #Make sure a restaurant is logged in
    if "restaurantID" in request.session or debug:
        errors = Event.objects.validator(request.POST)
        print(f"Date: {request.POST['date']}")
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/event/new")
        else:
            #Get restaurant object that is currently logged in
            restaurant = Restaurant.objects.get(id=request.session['restaurantID'])
            #Create the location for the event
            location = Location.objects.create(
                address = request.POST["address"],
                city = request.POST["city"],
                state = request.POST["state"],
                zip_code = request.POST["zip_code"]
            )
            #Create the event
            Event.objects.create(
                restaurant_id = restaurant,
                menu = restaurant.menus.first(),
                location= location,
                date_time = request.POST['date'],
                notes = request.POST["notes"],
                status = "In Progress",
                minimum_orders = request.POST["min_orders"],
                maximum_orders = 10000, #value is currently a placeholder to say lots of orders
                minimum_amount_per_order = request.POST["min_per_order"]
            )
            return redirect('/event')
    else:
        return redirect('/')

#Route is /event/new
def newEvent(request):
    return render(request, "newEvent.html")

#Route is /event/<int:eventID>/edit
def editEvent(request, eventID):
    if "restaurantID" in request.session or debug:
        event = Event.objects.get(id=eventID)
        date = event.date_time.strftime("%Y-%m-%dT%H:%M")
        print(f"{event.date_time}")
        context = {
            "event": event, 
            "date": date
        }
        return render(request, "editevent.html", context)
    else:
        return redirect("/")
    

#Route is /event/<int:eventID>/update
def updateEvent(request, eventID):
    if "restaurantID" in request.session or debug:
        errors = Event.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
                return redirect(f"/event/{eventID}/edit")
        else:
            #Update event in db
            event = Event.objects.get(id=eventID)
            location = Location.objects.create(
                address = request.POST["address"],
                city = request.POST["city"],
                state = request.POST["state"],
                zip_code = request.POST["zip_code"]
            )
            event.location = location
            event.date_time = request.POST["date"]
            event.notes = request.POST["notes"]
            event.minimum_orders = request.POST["min_orders"]
            event.minimum_amount_per_order = request.POST["min_per_order"]
            event.save()
        return redirect(f"/event/{eventID}/edit")
    else:
        return redirect("/")

#Route is /event/<int:eventID>
def viewEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    context = {
        "event": event,
        "orders": event.orders.all()
    }
    return render(request, "viewEvent.html", context)

#Route is /event/<int:eventID>/complete
def completeEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    event.status = "Completed"
    event.save()
    return redirect(f"/event/{event.id}")