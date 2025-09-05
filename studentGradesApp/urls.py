from django.urls import path
from . import views
# from django.contrib.auth import views as auth

from django.contrib import admin  # Django admin module
from django.conf import settings   # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('courses/', views.courses, name='courses'),
    path('course/', views.course, name='course'),
    path('students/', views.students, name='students'),
   path("students/remove_s/", views.remove_student, name="remove_student"),
   path("students/remove_c/", views.remove_course, name="remove_course"),
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
] 

#  Serve media files if DEBUG is True (development mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()