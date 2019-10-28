from __future__ import unicode_literals
from django.db import models
import re
    

# Create your models here.
class PWmanager(models.Manager):
    def Pass_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # email from registration
        if not EMAIL_REGEX.match(postData['reg_email']):
            errors['email'] = "Invalid email address"
        # this needs to be the phone number in the reg page 
        if len(postData['reg_phone']) > 10:
            errors['number'] = "your number is "
        # password from the registration
        if len(postData['reg_pass']) < 8:
            errors['password'] = "your password is too short"
        # first name from registration
        if len(postData['reg_first_name']) < 3:
            errors['firs_name']= "your first name must be entered and at least 3 letters long."
        # last name from the registration
        if len(postData['reg_last_name']) < 3:
            errors['last_name'] = "your last name must be entered and at least 3 letters long"
        # email from the registration page this tests for weather the email exists this is how I prevent duplicate users
        for user in Users.objects.all():
            if user.email == postData['reg_email']:
                errors['existance'] = "this email is already in use."
        return errors

class Users(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = PWmanager()
    def __repr__(self):
        return f"\n{100*'*'}\nID: {self.id}\n{self.email} : {self.password}\nfirst_name : {self.first_name}\nlast_name : {self.last_name}\n{100*'*'}"

class prospectManager(models.Manager):
    def pros_validator(self, postData):
        # this is for the prospects name
        errors = {}
        if len(postData['pros_name'])< 3:
            errors['name'] = "must have at least 3 characters in the name field"
        if len(postData['pros_address']) < 3:
            errors['address'] = "must have at least 3 characters in the address field"
        if len(postData['pros_phone']) < 3:
            errors['phone'] = "must have at least 3 characters in the phone field"
        if len(postData['pros_email']) < 3:
            errors['email'] = "must have at least 3 characters in the email field"
        if len(postData['pros_step'])< 3:
            errors['step'] = "must have at least 3 characters in the step field"
        if len(postData['pros_notes'])< 3:
            errors['notes'] = "must have at least 3 characters in the notes field"
        return errors

class Prospects(models.Model):
    name = models.CharField(max_length=255)
    followup = models.DateField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    step = models.CharField(max_length=255)
    users = models.ManyToManyField(Users, related_name="Prospects")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects=prospectManager()

class Notes(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    notes = models.TextField()
    Prospect = models.ForeignKey(Prospects, related_name="notes")

