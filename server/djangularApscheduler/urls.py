"""djangularApscheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$',views.loginSignup),
    url(r'^signup-user/$',views.signupUser),
    url(r'^signin-user/$',views.signinUser),
    url(r'^dashboard/$',views.dashboard),
    url(r'^instant-email-send/$',views.instantEmailSend),
    url(r'^save-email-report/$',views.saveEmailReport),
    url(r'^fetch-all-email-reports/$',views.fetchAllEmailReports),
    url(r'^delete-current-email-report/$',views.deleteCurrentEmailReport),
    url(r'^schedule-current-email-report/$',views.scheduleCurrentEmailReport),
    url(r'^get-all-schedule-email/$',views.getAllScheduleEmail),
    url(r'^pause-delete-schedule-email/$',views.pauseDeleteScheduleEmail),
]
