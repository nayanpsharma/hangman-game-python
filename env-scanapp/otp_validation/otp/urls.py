from django.urls import path
from django.urls.resolvers import URLPattern
from . import views as view
from rest_framework.authtoken import views


urlpatterns = [
    path("register/", view.register),
    path("login/", view.login),
    path("users/", view.users_list),
    path("delete_logout/", view.delete_authtokens_logout),
    path("add_or_update_contacts/", view.update_contacts),
    path("get_contacts/", view.view_contacts),
    #path("update_contacts/", view.update_contacts)



    #path('get_token/', views.obtain_auth_token)

]
