from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('post/<slug:slug>/',views.post_detail,name='post_detail'),
    path('articles/',views.article,name='article'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-post/', views.add_post, name='add_post'),
    path('edit-post/<int:id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:id>/', views.delete_post, name='delete_post'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]