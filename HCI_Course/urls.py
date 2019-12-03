"""HCI_Course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from HCI.views import views
from HCI.urls import university_url_patterns, course_url_patterns, charts_url_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'account'))),
    path('university/', include((university_url_patterns, 'HCI'), namespace='university')),
    path('course/', include((course_url_patterns, 'HCI'), namespace='course')),
    path('charts/', include((charts_url_patterns, 'HCI'), namespace='charts')),
    path('report/', include(('report.urls', 'report'))),
    path('message/', include(('message.urls', 'message'))),
    path('', views.homepage, name='homepage'),
]
