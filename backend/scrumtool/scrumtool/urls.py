"""scrumtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from api import views

router = DefaultRouter()

router.register(r'steplist', views.SteplistViewSet)
router.register(
    r'steplist/(?P<steplist_pk>[^/.]+)/step',
    views.StepViewSet)
router.register(r'epic', views.EpicViewSet)
router.register(r'feature', views.FeatureViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'board', views.BoardViewSet)
router.register(r'lane', views.LaneViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'file', views.FileViewSet)


schema_view = get_schema_view(
    title='Scrumtool API',
    description='An API to book matches or update odds.')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Scrumtool API')),
    path('rest-auth/', include('rest_auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
