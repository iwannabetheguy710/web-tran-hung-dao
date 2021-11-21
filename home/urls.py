from django.urls import path

from . import views

urlpatterns = [
	path('', views.index_page, name='index'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('register/', views.register_page, name='register'),

	# time table management
	path('tkb/', views.tkb_page, name='tkb'),
	path('tkb/<str:class_name>/', views.tkb_detail_page, name='tkb detail'),
	path('tkb/<str:class_name>/edit/', views.tkb_edit_page, name='tkb edit'),
]