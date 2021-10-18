
from django.urls import path,include
from django.contrib.auth import views as auth_views



from . import views



urlpatterns = [
    
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/',views.account_activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/', views.account_update, name='account'),
    path('profile/', views.userprofile, name='userprofile'),
    path("registergmail", views.registergmail, name="registergmail"),
    #path('accounts/', include('allauth.urls')),
    
    
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  
  
   
] 







