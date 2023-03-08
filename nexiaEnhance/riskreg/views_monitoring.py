# import requests
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms as f
from riskreg.forms import RiskRegEntryForm, CustomRiskForm, CreateDeficiencyForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags
import re
import html2text

from nexiaEnhance.views import UserRightsContext

# Apps files:

from nexiaEnhance.views import UserRightsContext

from accounts.models import Firm

from riskdatabase.models import (
    RiskDatabase_01_QualityObjectiveCategory,
    RiskDatabase_02_QualityObjective,
    RiskDatabase_03_QualityRisk,
    RiskDatabase_04_RiskResponse,
)

from riskreg.models import RiskRegister, RCA

from nexiaEnhance.views import UserRightsContext

from copy import deepcopy

import pandas as pd
import numpy as np
from collections import OrderedDict, defaultdict

from json import dumps
import os, io
import xlsxwriter


# Create your views here.


# ---------------------- 3. RCA ----------------------

# ---------------------- 3.1 Create RCA Entry ----------------------

class CreateDeficiencyView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = "riskreg/03_01_create_deficiency.html"
        context=UserRightsContext(request)
        context['does_form_data_exist'] = False
        try:
            context['cat'],context['obj'], context['risk'], context['rr'] = RiskRegister.objects.filter(id=self.kwargs['rr_id']).values_list('quality_objective_category','quality_objective','quality_risk','risk_response')[0]
            context['rr_id'] = self.kwargs['rr_id']
            print("\nSuccess, cat is: ", context['cat'])

            context['create_deficiency_form'] = CreateDeficiencyForm()
            context['does_form_data_exist'] = True

        except:
            print('Try Fail')

        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        print("\nRequest.post: ", request.POST)

        try:
            # print("New risk response: ", request.POST['new_risk_response'])

            is_severe = False
            try:
                if request.POST['is_severe']=="on":
                    is_severe=True
                    print("\nIt is severe")
                else:
                    print("\nIt is not severe")
            except:
                pass

            is_pervasive = False
            try:
                if request.POST['is_pervasive']=='on':
                    is_pervasive = True
                    print("\nIt is pervasive")
                else:
                    print("\nIt is NOT pervasive")
                    # pass
            except:
                pass

            # print("\nNumber trial: ", int('89'))
            # print("\nRisk response id is: ", request.POST['risk_response_id'])

            # risk_response_id = RiskRegister.objects.get(id=int(request.POST['risk_response_id']))
            # print("Obtained risk response object")

            # old_risk_response = RiskRegister.objects.filter(id=int(request.POST['risk_response_id'])).values('risk_response')
            # print("Obtained risk response")
            # print("\nRisk response id is: ", risk_response_id,"\n and old risk response is: ", old_risk_response)

            # defForm = CreateDeficiencyForm(request.POST)
            # print("\nForm created from request.post")
            # # defForm.save(commit=False)
            #
            # defForm.risk_response=risk_response_id
            # print("\nGot risk resp id for form")
            # defForm.old_risk_response=old_risk_response
            # print("\nGot risk resp for form")
            #
            # print("\nErrors in Def form:",defForm.errors)

            # defForm.save()
            # print("Form saved")
            # if defForm.is_valid():
            #     defForm.save()
            #     print("Form valid and saved")
            # else:
            #     print("Form not valid and not saved")

            RCA.objects.get_or_create(
                identified_deficiency=request.POST['identified_deficiency'],
                immediate_cause=request.POST['immediate_cause'],
                immediate_cause_reviewer_comments=request.POST['immediate_cause_reviewer_comments'],
                contributory_cause_1=request.POST['contributory_cause_1'],
                contributory_cause_1_reviewer_comments=request.POST['contributory_cause_1_reviewer_comments'],
                contributory_cause_2=request.POST['contributory_cause_2'],
                contributory_cause_2_reviewer_comments=request.POST['contributory_cause_2_reviewer_comments'],
                contributory_cause_3=request.POST['contributory_cause_3'],
                contributory_cause_3_reviewer_comments=request.POST['contributory_cause_3_reviewer_comments'],
                root_cause=request.POST['root_cause'],
                root_cause_reviewer_comments=request.POST['root_cause_reviewer_comments'],
                is_severe=is_severe,
                is_severe_comments=request.POST['is_severe_comments'],
                is_pervasive=is_pervasive,
                is_pervasive_comments=request.POST['is_pervasive_comments'],
                proposed_remedial_action=request.POST['proposed_remedial_action'],
                proposed_remedial_action_reviewer_comments=request.POST['proposed_remedial_action_reviewer_comments'],
                # proposed_remedial_action_status_choices=request.POST['proposed_remedial_action_status_choices'],
                proposed_remedial_action_status=request.POST['proposed_remedial_action_status'],
                remedial_action_conclusion=request.POST['remedial_action_conclusion'],
                remedial_action_change=request.POST['remedial_action_change'],
                preparer_signature=request.POST['preparer_signature'],
                # preparer_signature_date=request.POST['preparer_signature_date'],
                quality_management_head_signature=request.POST['quality_management_head_signature'],
                # quality_management_head_signature_date=request.POST['quality_management_head_signature_date'],
                old_risk_response=RiskRegister.objects.filter(id=self.kwargs['rr_id']).values_list('risk_response')[0][0],
                new_risk_response=request.POST['new_risk_response'],
                risk_response=RiskRegister.objects.get(id=request.POST['risk_response_id']),

            )
            print("Entry created")
            return HttpResponseRedirect(reverse('risk_register_2:deficiency-success'))
        except:
            print("Entry not created")
            return HttpResponseRedirect(reverse('risk_register_2:deficiency-error'))

        # return HttpResponseRedirect(reverse('risk_register:success'))

# ---------------------- 3.1 End of Create RCA Entry ----------------------

# ---------------------- 3.2 View all RCA Entries ----------------------

class ViewDeficiencies(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context=UserRightsContext(request)

        print("\nDef objects:", RCA.objects.all())

        rca_objs = RCA.objects.all()
        for rca in rca_objs:
            print("\nRca is : ", rca)

        df_risk_reg = pd.DataFrame(RiskRegister.objects.values())
        df_deficiencies = pd.DataFrame(RCA.objects.values())

        print("Def cols: ",df_deficiencies.columns.values)
        print("Def df isnull? : ",len(df_deficiencies))
        print("Time for error!")
        context['is_deficiency_exists'] = False

        rca_dict_list = []
        if len(df_deficiencies)>0 and len(df_risk_reg)>0:
            for rca in RCA.objects.filter(risk_response__firm_name_id=context['current_firm']):
                rca_dict={}

                print("\nRisk response of rca is: ",rca.risk_response_id)
                rca_dict['quality_objective_category'], rca_dict['quality_objective'], rca_dict['quality_risk'], \
                rca_dict['risk_response'] = \
                RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective_category',
                                                                                 'quality_objective', 'quality_risk',
                                                                                 'risk_response')[0]
                rca_dict['identified_deficiency'] = rca.identified_deficiency.html


                # immediate_cause '] = rca.  # immediate_cause .html
                rca_dict['immediate_cause'] = rca.immediate_cause.html
                rca_dict['immediate_cause_reviewer_comments'] = rca.immediate_cause_reviewer_comments.html


                # contributory_cause_1 '] = rca.  # contributory_cause_1 .html
                rca_dict['contributory_cause_1'] = rca.contributory_cause_1.html
                rca_dict['contributory_cause_1_reviewer_comments'] = rca.contributory_cause_1_reviewer_comments.html
                rca_dict['contributory_cause_2'] = rca.contributory_cause_2.html
                rca_dict['contributory_cause_2_reviewer_comments'] = rca.contributory_cause_2_reviewer_comments.html
                rca_dict['contributory_cause_3'] = rca.contributory_cause_3.html
                rca_dict['contributory_cause_3_reviewer_comments'] = rca.contributory_cause_3_reviewer_comments.html

                rca_dict['root_cause'] = rca.root_cause.html
                rca_dict['root_cause_reviewer_comments'] = rca.root_cause_reviewer_comments.html

                rca_dict['is_severe'] = "Yes" if rca.is_severe==True else "No"
                rca_dict['is_severe_comments'] = rca.is_severe_comments.html

                rca_dict['is_pervasive'] = "Yes" if rca.is_pervasive==True else "No"
                rca_dict['is_pervasive_comments'] = rca.is_pervasive_comments.html

                rca_dict['proposed_remedial_action'] = rca.proposed_remedial_action.html
                rca_dict['proposed_remedial_action_reviewer_comments'] = rca.proposed_remedial_action_reviewer_comments.html
                rca_dict['proposed_remedial_action_status'] = "Not started" if \
                    rca.proposed_remedial_action_status=="not_started" else \
                    "In progress" if rca.proposed_remedial_action_status == "in_progress" else "implemented"

                rca_dict['remedial_action_conclusion'] = rca.remedial_action_conclusion.html
                rca_dict['remedial_action_change'] = rca.remedial_action_change.html

                rca_dict['preparer_signature'] = rca.preparer_signature
                rca_dict['preparer_signature_date'] = rca.preparer_signature_date
                rca_dict['quality_management_head_signature'] = rca.quality_management_head_signature
                rca_dict['quality_management_head_signature_date'] = rca.quality_management_head_signature_date

                rca_dict['new_risk_response'] = rca.new_risk_response

                rca_dict['identified_deficiency_id'] = rca.identified_deficiency_id
                # rca_dict['identified_deficiency'] = rca.identified_deficiency.html

                rca_dict_list.append(rca_dict)

            # df_combined = pd.merge(
            #     left=df_risk_reg,
            #     left_on='id',
            #     right=df_deficiencies,
            #     right_on='risk_response_id',
            #     how='inner',
            # )
            # print("\nDf to print cols: \n", df_combined.columns.values)
            # print("\nDf to print: \n", df_combined)
            # context['deficiencies_dict'] = df_combined.to_dict('records', into=defaultdict(list))
            context['deficiencies_dict'] = rca_dict_list
            context['is_deficiency_exists'] = True
            print("To print def.s")
        else:
            context['deficiencies_dict'] = {}

        print("\nRCA dict list: ", rca_dict_list)

        template_name = "riskreg/03_02_view_deficiencies.html"
        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        print("\nRequest.post: ", request.POST)

        key_index = 0
        i=0

        try:
            while key_index==0 and i<len(request.POST):
                for key in request.POST:
                    print("Key is: ", key)
                    print("\nValue of the key is: ", request.POST[key])
                    if request.POST[key] == 'Update existing risk response':
                        print("\n Found key")
                        key_index = i
                    else:
                        pass
                    i=i+1
            # print("\nKey found and index is: ", key_index)

            identified_deficiency_id = list(request.POST)[key_index]
            print("\nIdentified deficiency id is: ", identified_deficiency_id)
            # print("\nRCA rr id: ", RCA.objects.filter(identified_deficiency_id=identified_deficiency_id).values() ,"\n")
            # print("\nValues: ",RCA.objects.filter(identified_deficiency_id=identified_deficiency_id).values_list('risk_response','new_risk_response')[0],"\n")

            rca_rr_id, rca_new_rr = RCA.objects.filter(identified_deficiency_id=identified_deficiency_id).values_list('risk_response','new_risk_response')[0]
            print("\nRCA new rr is: ", rca_new_rr)
            # print("\nRR entry: ", RiskRegister.objects.filter(id=rca_rr_id).values(), "\n")

            RiskRegister.objects.filter(id=rca_rr_id).update(risk_response=rca_new_rr)
            print("\nRR entry updated from RCA rr\n")
            return HttpResponseRedirect(reverse('risk_register_2:update-rr-success'))
        except:
            print("\nRR entry NOT updated from RCA rr\n")
            return HttpResponseRedirect(reverse('risk_register_2:deficiency-error'))

# ---------------------- 3.2 End of View all RCA Entries ----------------------

# ---------------------- 3.3 Edit RCA Entry ----------------------

class EditRCAEntryView(LoginRequiredMixin, UpdateView):
    template_name = 'riskreg/03_03_update_deficiency.html'
    fields = '__all__'
    model = RCA
    success_url = reverse_lazy('risk_register_2:view-deficiencies')

# ---------------------- 3.3 End of Edit RCA Entry ----------------------


# ---------------------- 3.4 Delete Deficiency View ----------------------

class DeleteDeficiencyView(LoginRequiredMixin, DeleteView):
    model = RCA
    template_name = 'riskreg/03_04_delete_deficiency.html'
    context_object_name = 'deficiency'
    success_url = reverse_lazy('risk_register_2:view-deficiencies')

# ---------------------- 3.4 End of Delete Deficiency View ----------------------

# ---------------------- 3.5 Deficiency Success View ----------------------
class DeficiencySuccessView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)

        # context['is_nexia_superuser'] = False
        # context['is_user_manager'] = False
        # is_nexia_superuser = False
        # is_user_manager = False
        #
        # try:
        #     print("In try")
        #     is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = \
        #     UserAttributes.objects.filter(
        #         user_id=request.user.id
        #     ).values_list('is_preparer', 'is_reviewer', 'is_ult_authority', 'is_user_manager', 'is_nexia_superuser')[0]
        #     context['is_preparer'] = is_preparer
        #     context['is_reviewer'] = is_reviewer
        #     context['is_ult_authority'] = is_ult_authority
        #     context['is_nexia_superuser'] = is_nexia_superuser
        #     context['is_user_manager'] = is_user_manager
        #     print("try succesful")
        # except:
        #     if request.user == "nexiaenhancesuperuser":
        #         is_nexia_superuser = True
        #         is_user_manager = True
        #         context['is_nexia_superuser'] = True
        #         context['is_user_manager'] = True
        #     else:
        #         is_nexia_superuser = False
        #         is_user_manager = False
        #
        # print("\nUser rights: NSU, UM\n", context['is_nexia_superuser'], context['is_user_manager'])

        template_name = 'riskreg/03_04_create_deficiency_success.html'

        return render(request, template_name=template_name, context=context)

# ---------------------- 3.5 Deficiency Success View ----------------------

# ---------------------- 3.6 Deficiency Error View ----------------------

class DeficiencyErrorView(LoginRequiredMixin, TemplateView):
    template_name = 'riskreg/03_06_deficiency_error.html'


# ---------------------- 3.6 End of Deficiency Error View ----------------------

# Export deficiencies
def textify(html):
    h = html2text.HTML2Text()

    # Don't Ignore links, they are useful inside emails
    h.ignore_links = False
    return h.handle(html)

def textify2(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()


@login_required()
def DeficienciesExportToExcelView(request):
    print("In Def Export View")

    # TODO: Consider deleteing user rights if not needed
    # Get the user rights
    context = UserRightsContext(request)


    rr_df = pd.DataFrame(
        RCA.objects.values()
    )

    print("\nDf: ", rr_df)


    def_list = []

    # for deficiency in RCA.objects.all():
    #     def_list.append(
    #         deficiency.identified_deficiency
    #     )

    for rca in RCA.objects.filter(risk_response__firm_name_id=context['current_firm']):
        rca_dict = {}
        temp_list = []

        print("\nRisk response of rca is: ", rca.risk_response_id)

        print("\nTextify: ", textify(rca.identified_deficiency.html))

        print("\nTextify 2: ", textify2(rca.identified_deficiency.html))

        print("\nRR values:\n", list(RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective_category',
                                                                                 'quality_objective', 'quality_risk',
                                                                                 'risk_response')[0]))

        temp_list.append(
            RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective_category',
                                                                             'quality_objective', 'quality_risk',
                                                                             'risk_response')[0],
        )

        def_list.append(
            [
                RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective_category')[0][0],
                RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective')[0][0],
                RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_risk')[0][0],
                RiskRegister.objects.filter(id=rca.risk_response_id).values_list('risk_response')[0][0],

                textify2(rca.identified_deficiency.html),

                textify2(rca.immediate_cause.html),
                textify2(rca.immediate_cause_reviewer_comments.html),

                textify2(rca.contributory_cause_1.html),
                textify2(rca.contributory_cause_1_reviewer_comments.html),
                textify2(rca.contributory_cause_2.html),
                textify2(rca.contributory_cause_2_reviewer_comments.html),
                textify2(rca.contributory_cause_3.html),
                textify2(rca.contributory_cause_3_reviewer_comments.html),

                textify2(rca.root_cause.html),
                textify2(rca.root_cause_reviewer_comments.html),

                "Yes" if rca.is_severe else "No",
                textify2(rca.is_severe_comments.html),
                "Yes" if rca.is_pervasive else "No",
                textify2(rca.is_pervasive_comments.html),

                textify2(rca.proposed_remedial_action.html),
                textify2(rca.proposed_remedial_action_reviewer_comments.html),
                "Not started" if \
                    rca.proposed_remedial_action_status == "not_started" else \
                    "In progress" if rca.proposed_remedial_action_status == "in_progress" else "implemented",

                textify2(rca.remedial_action_conclusion.html),
                textify2(rca.remedial_action_change.html),

                rca.preparer_signature,
                rca.preparer_signature_date,
                rca.quality_management_head_signature,
                rca.quality_management_head_signature_date,

                rca.new_risk_response,
            ]
        )

        print("\nDef list: ", def_list)

    rr_df = pd.DataFrame(def_list, columns=[
        'Quality objective Category',
        'Quality objective',
        'Quality risk',
        'Risk response',

        'Identified deficiency',

        'Immediate cause',
        'Reviewer comments',

        'First contributory cause',
        'Reviewer comments',
        'Second contributory cause',
        'Reviewer comments',
        'Third contributory cause',
        'Reviewer comments',

        'Root cause',
        'Reviewer comments',

        'Severe?',
        'Comments',
        'Pervasive?',
        'Comments',

        'Proposed remedial action',
        'Reviewer comments',
        'Remedial action status',
        'Remedial action conclusion',
        'Change as a result of the remedial action',
        'Preparer',
        'Sign off date',
        'Quality management head',
        'Sign off date',
        'New risk response'
    ])

    rr_df.to_excel("Deficiency_export.xlsx")

    print("\nDf RCA: ", rr_df)



    # # Create the risk library as a dataframe:


    # Create the risk register as a dataframe:
    #
    # rr_df = pd.DataFrame(
    #     RiskRegister.objects.values(
    #         'quality_objective_category', 'quality_objective',
    #          'quality_risk', 'risk_response', 'owner', 'response_type',
    #          'risk_response_source', 'response_status', 'comments', 'frequency_of_review',
    #          'created_by', 'sign_off_owner', 'sign_off_reviewer'
    #     )
    # )
    # print("Risk reg database: ","\n",rr_df)
    # print("Risk reg database columns: ", "\n", rr_df.columns.values)


    # Unmark from here

    # Create an excel file:
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Deficiencies")

    # General formats:

    text_bold_format = workbook.add_format({'bold': True})
    text_normal_format = workbook.add_format({'bold': False})
    text_bold_red_format = workbook.add_format({'bold': True, 'font_color': 'red'})

    worksheet.hide_gridlines(2)

    # Create table in file:

    # data_to_add = np.array(df_cat_obj_risk_rr)
    data_to_add = np.array(rr_df)


    start_row = 0
    start_col = 0
    end_row = start_row + data_to_add.shape[0]
    end_col = start_col + data_to_add.shape[1] - 1

    worksheet.add_table(start_row, start_col, end_row, end_col, {
        'data': data_to_add,
        'header_row': True,
        'style': 'Table Style Medium 6',
        'first_column': True,
    })

    # df_cols = df_cat_obj_risk_rr.columns.values
    df_cols = rr_df.columns.values


    for col_num, data in enumerate(df_cols):
        worksheet.write(start_row, start_col + col_num, data)

    # Header for table
    worksheet.write(start_row - 2, start_col, "Deficiencies:", text_bold_format)

    # END OF CREATE TABLE

    # CLOSE FILE:
    workbook.close()
    output.seek(0)

    # DOWNLOAD FILE:
    # Set up the Http response.

    filename = 'deficiencies.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    print(response)

    return response

    # return HttpResponse("Export completed")