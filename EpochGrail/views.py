from django.shortcuts import render, redirect
from EpochGrail.models import Grail, GrailItem, EpochItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
import json
from django.http import JsonResponse
from .forms import RegisterForm

# Create your views here.
def index(request):
    return render(request, "index.html")

#View a stranger (or friend's) grail 
def view_grail(request, pk):
    grail = Grail.objects.get(owner = pk)
    item_list = grail.items()
    return render(request, 'grail/item_list.html', {'item_list':item_list, 'pk':pk})

#User registration
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("EpochGrail:create_grail")
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form":form})

#Creates a new grail if the user has none.
@login_required
def create_grail(request):
    #Make sure the user has no grail associated with their account
    grail = Grail.objects.filter(owner = request.user)
    #Create the new grail with the user as the owner.
    if not grail:
        new_grail = Grail(owner = request.user)
        new_grail.save()
        items = EpochItem.objects.all()
        for item in items:
            new_item = GrailItem(grail = new_grail, item = item)
            new_item.save()
    return redirect("/")

#Displays the editable grail for a user. If the user somehow has not created a grail (should not happen, but you can never be too careful) creates one.
@login_required
def edit_grail(request):
    try:
        grail = Grail.objects.get(owner = request.user)
        item_list = grail.items()
        return render(request, 'grail/edit_grail.html', {'item_list':item_list, 'user_id':request.user})
    except Grail.DoesNotExist:
        return redirect("EpochGrail:create_grail")

@login_required
def update_grail(request):
    #Get the item name to query
    item_id = json.loads(request.body)['item']
    #Get the Grail object that the user owns
    grail_id = Grail.objects.get(owner = request.user)
    #get the the grail owned by the user and its list of GrailItems
    selection = GrailItem.objects.filter(grail = grail_id).filter(item__name__contains = item_id)

    for entry in selection:
        entry.update_item()
        state = entry.has_found
    return JsonResponse({"response": state})


    
#TODO: create an admin option to update the list.
def update_item_list():
    with open("EpochGrail/json/item_list.json") as f:
        result = json.loads(f.read())
    for item in result:
        #Check if an item already exists. While unique/set items thus far all have unique names, all fields are checked for thoroughness
        if not(EpochItem.objects.filter(name = item['Name'], base = item['Base'])):
            entry = EpochItem(base = item['Base'], name = item['Name'], rarity= item['Rarity'])
            entry.save()
            print("Added "+ entry.name + " to item list.")
        else:
            print("Entry exists in master list. Skipping...")
             
