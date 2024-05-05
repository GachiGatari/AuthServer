from django.urls import path
import users.views as v

urlpatterns = [
    path("register/", v.register_user, name="register"),
    path("login/", v.login_user, name="login"),
    path("logout/", v.logout_user, name="logout"),
    path("me/", v.get_user_info, name="get_user_info")
]
