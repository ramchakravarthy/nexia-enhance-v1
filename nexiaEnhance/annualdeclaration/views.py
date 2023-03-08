# import requests
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms as f

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Apps files:

# from risk_register import forms
# from risk_register.models import TrialModel, Genre, RiskRegister, CustomRiskRegister, AnnualDeclaration
# from risk_database.models import Model_01_QualityObjectiveCategory, Model_02_QualityObjective, Model_03_QualityRisk, \
#     Model_04_RiskResponse

# from risk_database.views import CreateRiskLibraryTable

from copy import deepcopy

from annualdeclaration.models import OLD_AnnualDeclaration, AnnualDeclaration
from annualdeclaration.forms import AnnualDeclarationForm
# from annualdeclaration.forms import AnnualDeclarationForm

# from risk_register.models import AnnualDeclaration as AD

from nexiaEnhance.views import UserRightsContext

import pandas as pd
import numpy as np
from collections import OrderedDict, defaultdict

from json import dumps
import os, io
import xlsxwriter
import datetime


# ---------------------- Annual declaration ----------------------
# class MakeDeclarationView(TemplateView):
#     template_name = 'risk_register/05_01_make_declaration.html'


class MakeDeclarationView(LoginRequiredMixin, CreateView):
    model = AnnualDeclaration
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        template_name = 'annual_declaration/01_annualdeclaration_form.html'
        context = UserRightsContext(request)
        context['today'] = datetime.datetime.today().strftime("%d-%m-%y")
        context['form'] = AnnualDeclarationForm()
        return render(request, template_name=template_name, context=context)


class ViewDeclarations(LoginRequiredMixin, ListView):
    model = AnnualDeclaration
    template_name = 'annual_declaration/9_1_viewDeclarations.html'
    context_object_name = 'declarations'

class ViewDeclarationsDetail(LoginRequiredMixin, DetailView):
    model = AnnualDeclaration
    template_name = 'annual_declaration/9_2_viewDecDetail.html'
    context_object_name = 'declaration'

class EditDeclaration(LoginRequiredMixin, UpdateView):
    model = AnnualDeclaration
    template_name = 'annual_declaration/9_3_edit_declaration.html'
    fields = (
        'evaluation_year',
        'evaluation_1',
        'evaluation_2',
        'evaluation_3',
        'conclusion_1',
        'conclusion_2',
        'conclusion_3',
        'actions_and_communications_1',
        'actions_and_communications_1_b',
        'actions_and_communications_2',
        'actions_and_communications_3',
        'individual',
    )

class DeleteDeclaration(LoginRequiredMixin, DeleteView):
    model = AnnualDeclaration
    template_name = 'annual_declaration/9_4_delete_declaration.html'
    context_object_name = 'declaration'


# # ---------------------- 5.1. Make annual declaration ----------------------
# class MakeDeclarationView(CreateView):
#     template_name = 'annual_declaration/01_annualdeclaration_form.html'
#     # specify the model for create view
#     model = AnnualDeclaration
#     form_class = AnnualDeclarationForm
#
#     # specify the fields to be displayed
#     # fields = ['evaluation_year', 'previous_evaluation_date', 'evaluation_1']
#
#     def get_context_data(self, **kwargs):
#         context = super(MakeDeclarationView, self).get_context_data(**kwargs)
#         date_now = datetime.datetime.now()
#         context['today']=str(date_now.strftime('%d-%m-%Y'))
#
#
#         # print("Make dec")
#         #
#         # field_name = 'year'
#         # obj = AD.objects.values_list('year',flat=True)
#         # print("Obj is: ", obj,"\n")
#         # print("Obj 2 is: ", list(obj), "\n")
#         # print("Obj 3 is: ", list(set(obj)), "\n")
#         # # field_value = getattr(obj, field_name)
#         # # print(field_value)
#         #
#         # print("AD ey: ",len(AnnualDeclaration.objects.values('evaluation_year')))
#
#
#         prev_eval_dates_choices = [
#             (date_now, date_now)
#             # (date_now, date_now.strftime('%d-%m-%Y'))
#         ]
#
#         print("In AD FORM")
#
#         print("Length of annual dec dates: ", len(AnnualDeclaration.objects.values('evaluation_date')),"\n")
#
#         if len(AnnualDeclaration.objects.values('evaluation_date'))>0:
#             prev_eval_dates = list(set(AnnualDeclaration.objects.values('evaluation_date', flat=True)))
#             for date in prev_eval_dates:
#                 prev_eval_dates_choices.append(
#                     (date, date.strftime('%d-%m-%Y'))
#                 )
#         else:
#             pass
#
#         print("AD Form var: ", prev_eval_dates_choices)
#
#         return context



# ---------------------- 5.1. END OF Make annual declaration ----------------------

# ---------------------- 5.2. View annual declarations ----------------------
class ViewDeclarationView(LoginRequiredMixin, TemplateView):
    template_name = 'annual_declaration/DO_NOT_USE_02_view_declarations.html'

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    def get_context_data(self, **kwargs):
        context = super(ViewDeclarationView, self).get_context_data(**kwargs)
        df_temp = pd.DataFrame(OLD_AnnualDeclaration.objects.values())
        print(df_temp)
        print("\nAnnual declatation column names: ",df_temp.columns.values)
        # to_dict('records', into=defaultdict(list))

        # context["cat_obj_matrix"], context["obj_risk_matrix"], context[
        #     "risk_rr_matrix"] = self.create_risk_library_table()
        context['annual_declaration'] = df_temp.to_dict('records', into=defaultdict(list))
        return context
# ---------------------- 5.2. END OF View annual declarations ----------------------