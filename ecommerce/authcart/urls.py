from django.urls import path
from authcart import views

urlpatterns = [
path('login/', views.handellogin, name = 'login'),
path('signup/', views.signup, name = 'signup'),
path('logout/', views.handellogout, name ='logout'),
path('activate/ <uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate')
# path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#     views.activate, name='activate'),
    
]
