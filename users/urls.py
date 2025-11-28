from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("activate/<int:user_id>/", views.activate_account, name="activate"),

    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("profile/edit/", views.UserEditView.as_view(), name="edit_profile"),

    path("list/", views.UserListView.as_view(), name="user_list"),
    path("detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),

    path("password/reset/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        views.ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path("dashboard/", views.UserDashboardView.as_view(), name="dashboard"),
]

