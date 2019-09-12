from django.db import models
import uuid
from django.utils import timezone
from jsonfield import JSONField


class SessionLevel(models.Model):
    """
    Table to Keeping track of sessions
    """
    session_id = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=13)
    level = models.IntegerField(default=0)
    session_data = JSONField(blank=True)

    def __str__(self):
        return self.phone_number + "  at Level  " + str(self.level)

class SaguraUsers(models.Model):
    """
    Table of sagura users
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, unique=True)
    national_id = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=30)
    registered_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Sagura Users"

    def __str__(self):
        return self.name

class Subscribers(models.Model):
    """
    Table of users who subscribed
    to sagura notifications(sells,requests,...) 
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(SaguraUsers, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = " Subscribers"
    
    def __str__(self):
        return self.user.name


class Crops(models.Model):
    """
    Table of fruits
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    CROP_CHOICES = {
        ('FRUITS','FRUITS'),
        ('VEGETABLES','VEGETABLES')
    }  
    crop_type = models.CharField(max_length=20, choices = CROP_CHOICES,default= 'FRUITS')
    prefered_climate = models.CharField(max_length=1000)
    land_preparation = models.CharField(max_length=1000)
    maturity_process = models.CharField(max_length=1000)


    class Meta:
        verbose_name_plural = "Crops"

    def __str__(self):
        return self.name + " " + self.crop_type

class Harvest(models.Model):
    """
    Table of harvests for sale
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    crop_name = models.CharField(max_length=30)
    crop_quantity = models.CharField(max_length=30)
    crop_price = models.CharField(max_length=30)
    farmer = models.ForeignKey(SaguraUsers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Harvest for Sale"
    
    def __str__(self):
        return self.crop_name + " " + self.crop_quantity +" Kg"

class Orders(models.Model):
    """
    Table of buyers orders
    """
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    harvest = models.ForeignKey(Harvest,on_delete=models.CASCADE)
    buyer = models.ForeignKey(SaguraUsers,on_delete= models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Buyer's Orders"
    
    def __str__(self):
        return self.harvest
