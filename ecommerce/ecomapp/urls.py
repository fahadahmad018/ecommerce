from django.urls import path
from ecomapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('checkout/', views.checkout, name="Checkout"),
    # path('handlerequest/', views.handlerequest, name="HandleRequest"),
    
]
