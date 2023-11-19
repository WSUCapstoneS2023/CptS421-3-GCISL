"""projectGCISL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from appGCISL import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_view, name='landing'),
    path('registration/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('get_involved/', views.getinvolved_view, name='get_involved'),
    path('survey/', views.survey_view, name='survey'),
    path('logout/', view=views.logout_view, name='logout'),
    path('survey/editor/builder/', view=views.survey_faculty_view, name='custom_survey'),
    path('survey/editor/<int:survey_id>/', view=views.survey_manager_view, name='survey_manager'),
    path('survey/editor/', view=views.survey_landing_view, name='survey_landing'),
    path('survey/editor/<int:survey_id>/response/', view=views.response_view, name='response')
]

# 
admin.site.site_header  =  "gciConnect Admin"  
admin.site.site_title  =  "gciConnect Admin Site"
admin.site.index_title  =  "gciConnect Admin"