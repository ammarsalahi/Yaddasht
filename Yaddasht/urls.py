from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from YadApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('signup/',signup.as_view(),name='signup'),
    path('signin/',signin,name='signin'),
    path('update/',update.as_view(),name='update'),
    path('logout/',logout,name='logout'),
    path('add-yadd/',add_yadd.as_view(),name='add-yadd'),
    path('edit-yadd/',edit_yadd.as_view(),name='edit-yadd'),
    path('del-yadd/',delete_yadd,name='del-yadd'),
    path('search',search,name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
