from attr import fields
from django.db import models
from django import forms

# Create your models here.
class File(models.Model):
    file=models.FileField(upload_to='media/')

class FileForms(forms.ModelForm):
    class Meta:
        model=File
        fields="__all__"