from django.shortcuts import render
from EpochGrail.models import Grail, GrailItem, EpochItem
import json

# Create your views here.
def index(request):
    return render(request, "index.html")

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
             
