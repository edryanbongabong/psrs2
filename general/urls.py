from django.urls import path
from . import views

urlpatterns = [
  path('dashboard/', views.home, name="home"),
  path('', views.loginPage, name="default"),
  path('login/', views.loginPage, name="login"),
  path('logout/', views.logoutUser, name="logout"),
  path('profile/', views.profile, name="profile"),
  path('settings/', views.settings, name="settings"),
  path('ranks/', views.ranks, name="ranks"),
  path('ranks/all/', views.RankAjaxDatatableView.as_view(), name="view-ranks"),
  path('ranks/create/', views.RankCreateView.as_view(), name="create-rank"),
  path('ranks/update/<int:pk>/', views.RankUpdateView.as_view(), name="update-rank"),
  path('ranks/delete/<int:pk>/', views.RankDeleteView.as_view(), name="delete-rank"),
  path('offices/', views.offices, name="offices"),
  path('offices/all/', views.OfficeAjaxDatatableView.as_view(), name="view-offices"),
  path('offices/create/', views.OfficeCreateView.as_view(), name="create-office"),
  path('offices/update/<int:pk>/', views.OfficeUpdateView.as_view(), name="update-office"),
  path('offices/delete/<int:pk>/', views.OfficeDeleteView.as_view(), name="delete-office"),
  path('bos/', views.bos, name="bos"),
  path('bos/all/', views.BOSAjaxDatatableView.as_view(), name="view-bos"),
  path('bos/create/', views.BOSCreateView.as_view(), name="create-bos"),
  path('bos/update/<int:pk>/', views.BOSUpdateView.as_view(), name="update-bos"),
  path('bos/delete/<int:pk>/', views.BOSDeleteView.as_view(), name="delete-bos"),
  
  path('users/', views.users_view, name="users"),
  path('users/all/', views.UserAjaxDatatableView.as_view(), name="view-user"),
  path('users/create/', views.create_user, name="create-user"),
  path('users/update/<int:id>/', views.update_user, name="update-user"),
  path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name="delete-user"),
  path('users/change-password/<int:id>/', views.change_password_user, name="change-password-user"),
  
  path('dashboard/donut-ajax-category/<str:cat>/', views.donut_chart, name="donut-ajax-category"),
  
]