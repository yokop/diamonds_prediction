"""jb_project_diamonds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import re_path
from diamonds import views
from diamonds import data_loader
from diamonds import predictor
from django.db.utils import OperationalError

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup_user, name='signup_user'),

    # diamonds
    path('', views.home, name='home'),
    path('fit/', views.fit, name='fit'),
    path('dataset/', views.dataset, name='dataset'),
    path('predict/', views.predict, name='predict'),
    path('predict_result/', views.predict_result, name='predict_result'),
    path('my_admin/', views.my_admin, name='my_admin'),
    path('my_admin_predicted_items/', views.my_admin_predicted_items, name='my_admin_predicted_items'),
    path('my_admin_log/', views.my_admin_log, name='my_admin_log'),
    
    path('predict/feedback', views.predict_result_feedback, name='predict_result_feedback'),
    path(r'predict/addtodataset/(?P<prediction>\d+)(?P<values>\d+)', views.predict_result_add_to_dataset, name='predict_result_add_to_dataset'),

    path('ajax_fit/', views.ajax_fit, name='ajax_fit'),
    path('ajax_load_new_dataset/', views.ajax_load_new_dataset, name='ajax_load_new_dataset'),
]

## remember to remove it when doing makemigrations or migrate
try:
    data_loader.init_dataset()
    predictor.load_model()
except OperationalError:
    pass # happens when db doesn't exist yet, views.py should be
         # importable without this side effect