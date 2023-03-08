from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views


app_name = 'accounts'

urlpatterns = [

    # Firms
    path('view-firms/', views.FirmsListView.as_view(), name='view-firms'),
    path('create-firm/', views.CreateFirmView.as_view(), name='create-firm'),
    path('import-firms/', views.ImportFirmView.as_view(), name='import-firms'),
    path('edit-firm/<pk>', views.EditFirm.as_view(), name='edit-firm'),
    path('delete-firm/<pk>', views.DeleteFirm.as_view(), name='delete-firm'),

    path('view-firm-details/<pk>', views.FirmsDetailedView.as_view(), name='view-firm-detail'),

    # Users
    path('user-administration/', views.AdminView.as_view(), name='user-administration'),
    path('create-user/', views.CreateUserView.as_view(), name='create-user'),
    path('import-users/', views.ImportUserView.as_view(), name='import-users'),
    path('view-users/',views.ViewUsersView.as_view(),name='view-users'),
    path('edit-user/<pk>',views.EditUserView.as_view(),name='edit-user'),
    path('delete-user/<pk>',views.DeleteUserView.as_view(),name='delete-user'),
    # path('view-users/',views.ViewUsersView.as_view(),name='view-users'),

    # path('accounts/', include('django.contrib.auth.urls')),


    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/09_password_change.html'), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/10_password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/11_password_reset.html',
        email_template_name='accounts/16_password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
    ), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/12_password_reset_sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'accounts/13_password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/15_password_reset_complete.html'
    ), name='password_reset_complete'),



    path("login/", auth_views.LoginView.as_view(template_name="accounts/08_b_login_video.html"), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),


    # path("signup/", views.SignUp.as_view(), name="signup"),
    # path("create-it-admin/", views.CreateITAdmin.as_view(), name="create-it-admin"),

]
