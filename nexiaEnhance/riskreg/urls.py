"""isqm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from riskreg import views, views_dashboard, views_monitoring

# TEMPLATE TAGGING
app_name = 'risk_register_2'

urlpatterns = [

    path('create_quill/', views.CreateQuill.as_view(), name="create_quill"),
    path('view_quill/', views.ViewQuillPosts.as_view(), name="view_quill"),
    path('import_quill/', views.ImportQuillPost, name="import_quill"),


    # # 0.0 Home - Dashboards
    path('', views_dashboard.RiskRegHomeView.as_view(), name="risk_reg_home_view"),
    path('risk-profile/', views_dashboard.RiskRegHomeViewRiskProfile.as_view(), name="risk_reg_home_view_risk_profile"),
    path('risk-response-profile/', views_dashboard.RiskRegHomeViewRiskResponseProfile.as_view(),
         name="risk_reg_home_view_risk_response_profile"),
    path('data-quality-summary/', views_dashboard.RiskRegHomeViewDataQualityProfile.as_view(),
         name="risk_reg_home_view_data_quality_summary"),
    path('deficiencies-action-plan-view/', views_dashboard.RiskRegHomeViewDeficiencyActionPlanView.as_view(),
         name="risk_reg_home_view_deficiencies_action_plan_view"),
    #
    # # 0.0.0 Dev
    # path('risk-register-dev/', views.RiskRegDevView.as_view(), name="risk_reg_dev_view"),
    # path('charts-dev/', views.ChartsDevView.as_view(), name="charts_dev_view"),
    #
    # 0.1 Instructions
    path('instructions/', views.RiskRegInstructions.as_view(), name="instructions"),
    path('instructions/isqm-system', views.RiskRegInstructionsISQMSystem.as_view(),
         name="instructions-isqm-system"),
    path('instructions/risk-assessment', views.RiskRegInstructionsRiskAssessment.as_view(),
         name="instructions-risk-assessment"),

    # 1. View risk register and update entries
    path('view-risk-register/', views.ViewRiskRegisterView.as_view(), name="view-risk-register"),

    # 2. Create entries
    # 2.0. Choice of entry view:
    path('create-risk-reg-entry', views.CreateRiskRegEntry.as_view(), name='create-risk-reg-entry'),

    # 2.1.1. Create from risk library
    path('create-risk-library-entry', views.CreateRiskRegTabView.as_view(), name='create-risk-library-entry'),

    # 2.1.2. Custom RR
    path('custom-rr-entry', views.CustomRREntryView.as_view(), name='custom-rr-entry'),

    # 2.1.3. Custom R, RR
    path('custom-r-rr-entry', views.CustomRisk_RREntryView.as_view(), name='custom-r-rr-entry'),

    # 2.1.4. Custom O, R, RR
    path('custom-o-r-rr-entry', views.CustomObjRiskRREntryView.as_view(), name='custom-o-r-rr-entry'),

    # 2.1.5 Create custom entry:
    path('create-custom-entry/', views.CustomEntryView.as_view(), name='create-custom-entry'),

    # 2.1.6 Edit Risk Library entry:
    path('edit-risk-library-entry/<pk>/', views.UpdateRLEntry.as_view(), name='edit-risk-library-entry'),

    # 2.1.7 Delete Risk Library entry:
    path('delete-risk-library-entry/<pk>/', views.DeleteRiskRegEntry.as_view(), name='delete-risk-library-entry'),
    #
    # 2.1.8 Export Risk Register:
    path('export-risk-register/', views.RiskRegisterExportToExcelView, name='export-risk-register'),
    # 2.1.9 Import Risk Register:
    path('import-risk-register/', views.RiskRegisterImportView.as_view(), name='import-risk-register'),
    # 2.1.10 Delete Risk Register:
    path('delete-risk-register/', views.DeleteRiskRegister, name='delete-risk-register'),
    path('delete-risk-register-complete/', views.DeleteRegComplete.as_view(), name='delete-risk-register-complete'),
    #
    # # 2.3. Success and error urls:

    #
    # # 2.4. Update entry:
    # path('update-library-risk/<int:pk>/', views.UpdateCustomRiskRegEntry.as_view(), name="update-library-risk"),
    #
    # 3. RCA:
    # 3.1 Create deficiency:
    path('create-deficiency/<int:rr_id>/', views_monitoring.CreateDeficiencyView.as_view(), name='create-deficiency'),

    # 3.2 View deficiency:
    path('view-deficiencies/', views_monitoring.ViewDeficiencies.as_view(), name='view-deficiencies'),

    # 3.3 Edit deficiency:
    path('edit-deficiency/<int:pk>/', views_monitoring.EditRCAEntryView.as_view(), name='edit-deficiency'),

    # 3.4 Delete deficiency:
    path('delete-deficiency/<int:pk>/', views_monitoring.DeleteDeficiencyView.as_view(), name='delete-deficiency'),

    # 3.5 Delete deficiency:
    path('export-deficiency/', views_monitoring.DeficienciesExportToExcelView, name='export-deficiency'),

    # path('create-deficiency/<int:rr_id>/', views.RiskRegMonitoringView.as_view(), name='risk-reg-monitoring'),
    # path('identified-deficiencies/', views.ViewDeficienciesView.as_view(), name='identified-deficiencies'),

    # # 3.3. Success and error urls:
    path('deficiency-success/', views_monitoring.DeficiencySuccessView.as_view(), name='deficiency-success'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('error/', views.ErrorView.as_view(), name='error'),
    path('update-rr-success/', views.UpdateRRSuccessView.as_view(), name='update-rr-success'),
    path('deficiency-error/', views_monitoring.DeficiencyErrorView.as_view(), name='deficiency-error'),

    #
    # # 4. Export to excel:
    # path('risk-reg-export-to-excel/', views.ExportToExcelView.as_view(), name='risk-reg-export-to-excel'),
    # path('risk-reg-export-to-excel-2/', views.ExportToExcelView2),
    #
    # # 5. Annual declaration:
    # # 4.1. Make declaration:
    # path('make-declaration/', views.MakeDeclarationView.as_view(), name='make-declaration'),
    # # 4.2. View declaration:
    # path('view-declaration/', views.ViewDeclarationView.as_view(), name='view-declaration'),

]
