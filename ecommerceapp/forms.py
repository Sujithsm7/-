from django import forms

class shopregform(forms.Form):
    shopname=forms.CharField(max_length=30)
    address=forms.CharField(max_length=90)
    shopid=forms.IntegerField()
    email=forms.EmailField()
    phone=forms.IntegerField()
    password=forms.IntegerField()
    cpass=forms.IntegerField()

class shoploginform(forms.Form):
    shopname=forms.CharField(max_length=30)
    password=forms.IntegerField()

class productuploadform(forms.Form):
    pname=forms.CharField(max_length=30)
    price=forms.IntegerField()
    des=forms.CharField(max_length=500)
    pimage=forms.ImageField()