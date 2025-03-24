
from django.db import models
from django.conf import settings
from django.utils import timezone

class Grail(models.Model):
    date_created = models.DateField(auto_now_add= True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def items(self):
        return GrailItem.objects.filter(grail=self)

class EpochItem(models.Model):
    name = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50, null = True) #Unique/Set

class GrailItem(models.Model):
    grail = models.ForeignKey(Grail, on_delete=models.CASCADE, null = True)
    item = models.ForeignKey(EpochItem, on_delete=models.CASCADE)
    has_found = models.BooleanField(default= False)
    date_found = models.DateField(null = True)

    def update_item(self):
        #Simply flip whether the item was found, if we flip has_found to True then set the date_found
        self.has_found = not self.has_found
        if(self.has_found == True):
            self.date_found = timezone.now()
        self.save()