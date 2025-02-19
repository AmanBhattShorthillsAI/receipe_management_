"""
URL configuration for storefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from home.views import about, home, success, contact
from vege.views import receipes, delete_receipe, update_receipe, login_page, register_page, logout_page, get_students, see_marks
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home, name="home"),
    path("receipes/", receipes, name="receipes"),
    path("success/", success, name="success"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("admin/", admin.site.urls),
    path("delete_receipes/<id>/", delete_receipe, name="delete_receipe"),
    path("update_receipes/<id>/", update_receipe, name="update_receipe"),
    path("login/", login_page, name="login"),
    path("register/", register_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path('students/', get_students, name='students'),
    path('marks/<student_id>/', see_marks, name='marks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
