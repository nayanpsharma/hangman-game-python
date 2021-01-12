from django.urls import path
from django.urls.resolvers import URLPattern
from . import views as view
from rest_framework.authtoken import views


urlpatterns = [
    path("account/api/register/", view.register),
    path("account/api/login/", view.login),
    path("account/api/users_list/", view.users_list),
    path("account/api/delete_logout/", view.delete_authtokens_logout),
    path("account/api/add_or_update_contacts/", view.update_contacts),
    path("account/api/get_contacts/", view.view_contacts),
    #path("update_contacts/", view.update_contacts)



    #path('get_token/', views.obtain_auth_token)

]
