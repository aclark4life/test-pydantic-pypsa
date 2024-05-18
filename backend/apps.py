from django.contrib.admin.apps import AdminConfig


class BackendAdminConfig(AdminConfig):
    default_site = "backend.admin.BackendAdminSite"
