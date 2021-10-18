from django.conf import settings
from django.db import models


class Country(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    
class Division(models.Model):
    name=models.CharField(max_length=100)
    country=models.ForeignKey(Country,on_delete=models.CASCADE, related_name='divisions')
    def __str__(self):
        return self.name
    
    
   
class District(models.Model):
    name=models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    division=models.ForeignKey(Division,on_delete=models.CASCADE, related_name='districts')
    def __str__(self):
        return self.name
    
    
class SubDistrict(models.Model):
    name=models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    district=models.ForeignKey(District,on_delete=models.CASCADE, related_name='subdistricts')
    def __str__(self):
        return self.name
    
    

class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    phone=models.CharField(max_length=100,blank=True, null= True)
    country=models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='cntry')
    division=models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True, related_name='dvsn')
    district=models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True, related_name='dstrct')
    subdistrict=models.ForeignKey(SubDistrict, on_delete=models.SET_NULL, blank=True, null=True, related_name='sbdstrct')
    addressOf=models.CharField(max_length=225)
    
    def __str__(self):
        return self.addressOf
    
    

class Contact(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=17)
    email=models.EmailField()
    text=models.TextField()
    def __str__(self):
        return self.name
    
    


