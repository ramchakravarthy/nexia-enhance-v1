from django.urls import path, include

from riskregister import views

app_name = 'risk_register'

urlpatterns = [

    # 0.1 Instructions
    path('instructions/', views.RiskRegInstructions.as_view(), name="instructions"),
    path('instructions/risk-assessment', views.RiskRegInstructionsRiskAssessment.as_view(),
         name="instructions-risk-assessment"),


    # 01. Create an entry

    # 01_a_create a risk library entry
    path('create-rd-entry/', views.CreateRiskLibraryEntryView.as_view(), name='create-rd-entry'),
    # path('confirm-create-entry/', views.ConfirmCreateEntryView, name='confirm-create-entry'),

    # 2. View Risk register:
    path('view-risk-register/',views.ViewRiskRegisterView.as_view(), name='view-risk-register'),

    # 09: Success and error urls:
    path('success/', views.SuccessView.as_view(), name='success'),
    path('error/', views.ErrorView.as_view(), name='error'),

    path('view1/', views.View1.as_view(), name='view1'),
    path('view2/', views.View2, name='view2'),


    path('cat-list-view/', views.CategoryListView.as_view(), name='cat-list-view'),
    path('cat-detailed-view/<pk>', views.CategoryDetailedView.as_view(), name='cat-detail-view'),
    path('create-cat/', views.CreateCategoryView.as_view(), name='create-cat'),
    path('create-obj/', views.CreateObjectiveView.as_view(), name='create-obj'),
]
