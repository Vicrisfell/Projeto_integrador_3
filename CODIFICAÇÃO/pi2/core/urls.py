from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    # path('cadastro/', admin.site.urls),
    # path('listar/', include('blog.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/register/', views.register, name='register'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('accounts/profile/edit/', views.profile_edit, name='profile_edit'),
]
