from django.urls import path
from Users import views
urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('create/', views.CreateUserView.as_view(), name="create"),
    path('logout', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name="profile"),
    path('update/', views.UpdateUser.as_view(), name="update"),
    path('delete/', views.DeleteAccountView.as_view(), name="delete")
]
