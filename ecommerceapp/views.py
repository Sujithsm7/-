from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import os
import datetime
from django.contrib.auth.models import User
from django.contrib import messages
import uuid

# Create your views here.
def first(request):
    return HttpResponse("hello world")

def index(request):
    return render(request,'index.html')


def shopreg(request):
    if request.method=='POST':
        a=shopregform(request.POST)
        if a.is_valid():
            sn=a.cleaned_data["shopname"]
            sa=a.cleaned_data["address"]
            si=a.cleaned_data["shopid"]
            se=a.cleaned_data["email"]
            sph=a.cleaned_data["phone"]
            spass=a.cleaned_data["password"]
            scpass=a.cleaned_data["cpass"]
            if spass==scpass:
                b=shopregmodel(shopname=sn,address=sa,shopid=si,email=se,phone=sph,password=spass)
                b.save()
                return redirect(shoplogin)
            else:
                return HttpResponse("Password Incorrect")
        else:
            return HttpResponse("Registration failed")
    return (render(request,'shopregister.html'))


def shoplogin(request):
    if request.method=='POST':
        a=shoploginform(request.POST)
        if a.is_valid():
            sname=a.cleaned_data["shopname"]
            spassword=a.cleaned_data["password"]
            request.session['shopname']=sname

            b=shopregmodel.objects.all()
            for i in b:
                if sname==i.shopname and spassword==i.password:
                    request.session['id']=i.id
                    return redirect(productprofile)
            else:
                return HttpResponse("Login Failed")
    return render(request,'shoplogin.html')

def productprofile(request):
    shopname=request.session['shopname']
    return render(request,'productprofile.html',{'shopname':shopname})

def productupload(request):
    if request.method=='POST':
        a=productuploadform(request.POST,request.FILES)
        id=request.session['id']
        if a.is_valid():
            name=a.cleaned_data["pname"]
            p=a.cleaned_data["price"]
            d=a.cleaned_data["des"]
            im=a.cleaned_data["pimage"]
            b=productuploadmodel(shopid=id,pname=name,price=p,des=d,pimage=im)
            b.save()
            return redirect(productdisplay)
        else:
            return HttpResponse("Upload failed")


    return render(request,'productupload.html')


def productdisplay(request):
    shpid=request.session['id']
    a=productuploadmodel.objects.all()
    n=[]
    p=[]
    d=[]
    im=[]
    id=[]
    shopid=[]
    for i in a:
        sid=i.shopid
        shopid.append(sid)

        ide=i.id
        id.append(ide)

        nm=i.pname
        n.append(nm)

        pr=i.price
        p.append(pr)

        de=i.des
        d.append(de)

        ime=i.pimage
        im.append(str(ime).split('/')[-1])
    thelist=zip(n,p,d,im,id,shopid)
    return render(request,'productdisplay.html',{'thelist':thelist,'shopid':shpid})

def allproductdisplay(request):
    a=productuploadmodel.objects.all()
    n=[]
    p=[]
    d=[]
    im=[]
    id=[]

    for i in a:


        ide=i.id
        id.append(ide)

        nm=i.pname
        n.append(nm)

        pr=i.price
        p.append(pr)

        de=i.des
        d.append(de)

        ime=i.pimage
        im.append(str(ime).split('/')[-1])
    thelist=zip(n,p,d,im,id)

    return render(request,'allproductdisplay.html',{'thelist':thelist})



#models.objects.get(id=id)
def productdelete(request,id):
    a=productuploadmodel.objects.get(id=id)
    a.delete()
    return redirect(productdisplay)


def productedit(request,id):
    a=productuploadmodel.objects.get(id=id)
    img=str(a.pimage).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES):
            if len(a.pimage)>0:#check old file
                os.remove(a.pimage.path)
            a.pimage=request.FILES["edimage"]
        a.pname=request.POST.get("edname")
        a.price=request.POST.get("edprice")
        a.des=request.POST.get("eddes")
        a.save()
        return redirect(productdisplay)

    return render(request,'editproduct.html',{'a':a,'img':img})



def uregis(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        password=request.POST.get('password')

        if User.objects.filter(username=username).first():
            messages.success(request,'Username already taken')
            return redirect(uregis)
        if User.objects.filter(email=email).first():
            messages.success(request,'Email already taken')
            return redirect(uregis)
        user_obj=User(username=username,email=email,first_name=firstname,last_name=lastname)
        user_obj.set_password(password)
        user_obj.save()

        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()

        send_mail_regis(email,auth_token)#user def fn
        return render(request,'success.html')
    return render(request,'userregister.html')


def send_mail_regis(email,auth_token): #django sending mail config
    subject="your account has been verified"
    message=f'click the link to verify your account http://127.0.0.1:8000/ecommerceapp/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    #inbuilt fn
    send_mail(subject,message,email_from,recipient)



def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,"Your account is already verified")
            return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,"Your account has been verified")
        return redirect(userlogin)
    else:
        messages.success(request,"USER NOT FOUND")
        return redirect(userlogin)

def userlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        request.session['username']=username
        userobj=User.objects.filter(username=username).first()
        if userobj is None:
            messages.success(request,'user not found')
            return redirect(userlogin)
        profile_obj=profile.objects.filter(user=userobj).first()
        request.session['id']=userobj.id
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check mail')
            return redirect(userlogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'Wrong password or Username')
            return redirect(userlogin)
        return redirect(userprofile)
    return render(request,'userlogin.html')

def userprofile(request):
    un=request.session['username']
    return render(request,'userprofile.html',{'username':un})


def userallproducts(request):

    a=productuploadmodel.objects.all()
    n=[]
    p=[]
    d=[]
    im=[]
    id=[]
    for i in a:

        ide=i.id
        id.append(ide)

        nm=i.pname
        n.append(nm)

        pr=i.price
        p.append(pr)

        de=i.des
        d.append(de)

        ime=i.pimage
        im.append(str(ime).split('/')[-1])
    thelist=zip(n,p,d,im,id)
    return render(request,'userallproducts.html',{'thelist':thelist})



def addtocart(request,id):

    a=productuploadmodel.objects.get(id=id)
    usd = request.session['id']
    if cartm.objects.filter(pname=a.pname,userid=usd):
        return HttpResponse('item already in cart')
    b=cartm(userid=usd,pname=a.pname,price=a.price,des=a.des,pimage=a.pimage)
    b.save()
    return redirect(displaycart)

def displaycart(request):
    uid=request.session['id']
    a=cartm.objects.all()
    userid=[]
    n=[]
    p=[]
    d=[]
    im=[]
    id=[]
    for i in a:
        ui=i.userid
        userid.append(ui)

        nm=i.pname
        n.append(nm)

        pr=i.price
        p.append(pr)

        dr=i.des
        d.append(dr)

        imge=i.pimage
        im.append(str(imge).split('/')[-1])

        ide=i.id
        id.append(ide)

    li=zip(n,p,d,im,id,userid)
    return render(request,'cartdisplay.html',{'li':li,'userid':uid})



def wishlist(request,id):

    a=productuploadmodel.objects.get(id=id)
    usd = request.session['id']
    if wishlistm.objects.filter(pname=a.pname,userid=usd):
        return HttpResponse('ITEM ALREADY IN WISHLIST')
    b=wishlistm(userid=usd,pname=a.pname,price=a.price,des=a.des,pimage=a.pimage)
    b.save()
    return redirect(wishlistdisplay)

def wishlistdisplay(request):
    usid = request.session['id']
    a=wishlistm.objects.all()
    userid=[]
    name=[]
    price=[]
    description=[]
    image=[]
    id=[]
    for i in a:
        us=i.userid
        userid.append(us)

        nm=i.pname
        name.append(nm)

        pr=i.price
        price.append(pr)

        d=i.des
        description.append(d)

        image.append(str(i.pimage).split('/')[-1])

        idi=i.id
        id.append(idi)
    lis=zip(name,price,description,image,id,userid)
    return render(request,'wishdisplay.html',{'lis':lis,'userid':usid})

def cartremove(request,id):
    a=cartm.objects.get(id=id)
    a.delete()
    return redirect(displaycart)
def wishlistremove(request,id):
    a=wishlistm.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)

def productbuycart(request,id):
    a=cartm.objects.get(id=id)
    img = a.pimage
    x = str(img).split('/')[-1]
    if request.method=='POST':

        nm = request.POST.get('name')
        pr = request.POST.get('price')
        des=request.POST.get('description')
        quan = request.POST.get('quantity')
        b=buymodel(pname=nm,price=pr,des=des,quantity=quan)
        b.save()
        total=int(pr)*int(quan)
        return render(request,'finalbill.html',{'b':b,'t':total,'x':x})
    return render(request,'buyproduct.html',{'a':a,'x':x})

def wishtocart(request,id):
    ide=request.session['id']
    a=wishlistm.objects.get(id=id)
    if cartm.objects.filter(pname=a.pname):
        return HttpResponse('iTEM ALREADY IN CART')
    b=cartm(userid=ide,pname=a.pname,des=a.des,price=a.price,pimage=a.pimage)
    b.save()
    return redirect(displaycart)



def cardpay(request):
    if request.method=='POST':
        cardname=request.POST.get('cname')
        cardnumber=request.POST.get('cnumber')
        cardexpiry=request.POST.get('expiry')
        securitycode=request.POST.get('security')
        b=customerdetailsmodel(name=cardname,cardno=cardnumber,cardexpiry=cardexpiry,security=securitycode)
        b.save()

        from datetime import timedelta
        a=datetime.date.today()
        d=a+timedelta(15)
        return render(request,'ordersuccess.html',{'date':d})
    return render(request,'placeorder.html')



def shopnotification(request):
    c = []
    t = []
    a=shop_notification.objects.all()
    for i in a:
        ct=i.content
        c.append(ct)
        ti=i.datetimeshop
        t.append(ti)
    x=zip(c,t)
    return render(request,'shopnot.html',{'x':x})

def usernotification(request):
    a=user_notification.objects.all()
    uc=[]
    ut=[]
    for i in a:
        cnt=i.content
        uc.append(cnt)
        usd=i.datetimeuser
        ut.append(usd)
    x=zip(uc,ut)
    return render(request,'usernot.html',{'x':x})