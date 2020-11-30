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
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

import oauth2_provider.views as oauth2_views

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from rest_framework_nested import routers

from api import views
from scrmtl_statistics import views as statistic_views

router = routers.SimpleRouter()

router.register(r'projects', views.ProjectViewSet)
router.register(r'project_users', views.ProjectUserViewSet)
router.register(r'project_roles', views.ProjectRoleViewSet)
router.register(r'boards', views.BoardViewSet)
router.register(r'lanes', views.LaneViewSet)
router.register(r'epics', views.EpicViewSet)
router.register(r'features', views.FeatureViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'steplists', views.SteplistViewSet)
router.register(r'steps', views.StepViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'labels', views.LabelViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'sprints', views.SprintViewSet)
router.register(r'users', views.PlatformUserViewSet)

router.register(r'sprint_statistics', statistic_views.SprintStatisticViewSet)


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/',
             oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/',
             oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/',
             oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/',
             oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(),
             name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
             name="authorized-token-delete"),
    ]


schema_view = get_schema_view(
    title='Scrumtool API',
    description='An API to book matches or update odds.')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api-auth/', include('rest_framework.urls')),
    path('schema/', schema_view),
    path(r'api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Scrumtool API')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
