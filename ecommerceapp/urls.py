from django.urls import path
from .views import *
urlpatterns=[
    path('firsturl/',first),
    path('shopreg/',shopreg),
    path('shoplog/',shoplogin),
    path('productupload/',productupload),
    path('productprofile/',productprofile),
    path('productdisplay/',productdisplay),
    path('allproductdisplay/',allproductdisplay),
    path('delete/<int:id>', productdelete),
    path('editproduct/<int:id>',productedit),
    path('userregister/',uregis),
    path('verify/<auth_token>',verify),
    path('index/',index),
    path('userlogin/',userlogin),
    path('userprofile/',userprofile),
    path('userallproducts/',userallproducts),
    path('addtocart/<int:id>',addtocart),
    path('cartdisplay/',displaycart),
    path('wishlist/<int:id>',wishlist),
    path('displaywishlist/',wishlistdisplay),
    path('cartremove/<int:id>',cartremove),
    path('wishremove/<int:id>',wishlistremove),
    path('buyproduct/<int:id>',productbuycart),
    path('wishtocart/<int:id>',wishtocart),
    path('placeorder/',cardpay),
    path('shopnot/', shopnotification),
    path('usernot/', usernotification)


]