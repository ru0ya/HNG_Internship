from django.urls import path

from kampuni.views import (
        RegisterView,
        LoginView,
        UserDetailView,
        OrganizationListView,
        OrganizationDetailView
        )


urlpatterns = [
        path(
            'auth/register',
            RegisterView.as_view(),
            name='register'
            ),
        path(
            'auth/login',
            LoginView.as_view(),
            name='login'
            ),
        path(
            'api/users/<uuid:user_id>',
            UserDetailView.as_view(),
            name='user-detail'
            ),
        path(
            'api/organizations',
            OrganizationListView.as_view(),
            name='organization-list'
            ),
        path(
            'api/organizations/<uuid:org_id>',
            OrganizationDetailView.as_view(),
            name='organization-detail'
            ),
        ]

