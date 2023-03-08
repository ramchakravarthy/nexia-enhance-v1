from django.shortcuts import render

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.models import User, UserAttributes, Firm

from riskdatabase.forms import ImportRiskDatabaseForm
from riskdatabase.models import (
    RiskDatabase_01_QualityObjectiveCategory,
    RiskDatabase_02_QualityObjective,
    RiskDatabase_03_QualityRisk,
    RiskDatabase_04_RiskResponse,
)

from nexiaEnhance.views import UserRightsContext

from collections import OrderedDict, defaultdict
import io
import xlsxwriter

import numpy as np
import pandas as pd

# Create your views here.

# 01. View Risk Database
class ViewRiskDatabaseTableView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        template_name = 'riskdatabase/01_view_risk_database.html'
        context = UserRightsContext(request)
        # print("\nContext:\n",context)

        if context['is_viewer']==True:
            df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
            df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
            df_cat_obj = pd.merge(
                left=df_cat,
                left_on='quality_objective_category_id',
                right=df_obj,
                right_on='quality_objective_category_id',
                how='inner'
            )
            del df_cat, df_obj

            df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
            df_cat_obj_risk = pd.merge(
                left=df_cat_obj,
                left_on='quality_objective_id',
                right=df_risk,
                right_on='quality_objective_id',
                how='inner',
            )
            del df_risk, df_cat_obj

            df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
            df_cat_obj_risk_rr = pd.merge(
                left=df_cat_obj_risk,
                left_on='quality_risk_id',
                right=df_rr,
                right_on='quality_risk_id',
                how='inner',
            )
            del df_cat_obj_risk, df_rr

            context['risk_database_combined'] = df_cat_obj_risk_rr.to_dict('records', into=defaultdict(list))

            print("\nDf combined:\n", df_cat_obj_risk_rr.head(1).T)

            print("\nDf combined columns:\n", df_cat_obj_risk_rr.columns.values)

            del df_cat_obj_risk_rr
        else:
            print("\nUser is not a viewer and hence cannot view Risk Library\n")
            pass

        return render(request=request, template_name=template_name, context=context)

# 02. Add risk

# NOT SURE IF WE NEED THIS - WE WILL IMPORT A DATABASE AND THEN EDIT IT

# 03. Import risk database

class ImportRiskDatabaseView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        context['import_file_form'] = ImportRiskDatabaseForm
        return render(request, template_name = 'riskdatabase/03_import_risk_database.html', context=context)

    def post(self, request, *args, **kwargs):
        print("In post")

        print("In Risk library import Post view - a Form has been posted")

        form = ImportRiskDatabaseForm(request.POST, request.FILES)
        if form.is_valid():
            print("File found")

            print(request.POST)
            print(request.FILES)

            try:
                df = pd.read_excel(request.FILES['risk_database'])
                print("\nRisk Database to upload:\n", df)

                print(df.columns.values)

                # 1. Category table:

                cat_dict = pd.DataFrame(
                    df['Quality objective category'].drop_duplicates().values,
                    columns=['Quality objective category']
                ).to_dict('records', into=defaultdict(list))

                # print("\nCat dict:\n", cat_dict)

                # code to create records
                # -----------------

                for cat in cat_dict:
                    RiskDatabase_01_QualityObjectiveCategory.objects.get_or_create(
                        quality_objective_category=cat['Quality objective category']
                    )

                # 2. Objectives:

                obj_dict = df[
                    ['Quality objective category', 'Quality objective', 'Quality objective ref']
                ].drop_duplicates().to_dict('records', into=defaultdict(list))
                # print('\nObj\n',obj_dict[0])

                # code to create records
                # -----------------
                for obj in obj_dict:
                    RiskDatabase_02_QualityObjective.objects.get_or_create(
                        quality_objective_category=RiskDatabase_01_QualityObjectiveCategory.objects.get(
                            quality_objective_category=obj['Quality objective category']),
                        quality_objective=obj['Quality objective'],
                        quality_objective_ref=obj['Quality objective ref'],
                    )

                    # print("\nCat: ", cat, "\n")

                # 3. Risk:

                risk_dict = df[
                    ['Quality objective', 'Quality Risk', 'Quality risk firm size', 'Quality Risk ref']
                ].drop_duplicates().to_dict('records', into=defaultdict(list))
                print('\nRisk\n', risk_dict[0])

                # code to create records
                # -----------------
                for risk in risk_dict:
                    RiskDatabase_03_QualityRisk.objects.get_or_create(
                        quality_objective=RiskDatabase_02_QualityObjective.objects.get(
                            quality_objective=risk['Quality objective']),
                        quality_risk=risk['Quality Risk'],
                        quality_risk_firm_size=risk['Quality risk firm size'],
                        quality_risk_ref=risk['Quality Risk ref'],
                    )

                # 4. Risk response:

                rr_dict = df[
                    ['Quality Risk', 'Responses to address the quality risks', 'Risk response firm size',
                     'Risk response ref', 'Additional Mercia guidance', 'Mandatory?']
                ].drop_duplicates().to_dict('records', into=defaultdict(list))
                print('\nRR\n', rr_dict[0])

                # code to create records
                # -----------------
                for rr in rr_dict:
                    RiskDatabase_04_RiskResponse.objects.get_or_create(
                        quality_risk=RiskDatabase_03_QualityRisk.objects.get(quality_risk=rr['Quality Risk']),
                        risk_response=rr['Responses to address the quality risks'],
                        risk_response_firm_size=rr['Risk response firm size'],
                        risk_response_ref=rr['Risk response ref'],
                        response_mandatory=rr['Mandatory?'],
                        additional_mercia_guidance=rr['Additional Mercia guidance'],
                    )
            except:
                print("Import didnt work")


        else:
            print("File not found")



        return HttpResponseRedirect(reverse('risk_database:view-risk-database'))

# 04. Update Category, Objective, Risk and Risk Response entries

class RiskDatabaseCatUpdateView(LoginRequiredMixin, UpdateView):
    model = RiskDatabase_01_QualityObjectiveCategory
    success_url = reverse_lazy('risk_database:view-risk-database')
    fields = ['quality_objective_category']
    template_name = 'riskdatabase/04_a_update_category.html'

class RiskDatabaseObjectiveUpdateView(LoginRequiredMixin, UpdateView):
    model = RiskDatabase_02_QualityObjective
    success_url = reverse_lazy('risk_database:view-risk-database')
    fields = ['quality_objective_category', 'quality_objective', 'quality_objective_ref']
    template_name = 'riskdatabase/04_b_update_objective.html'

class RiskDatabaseRiskUpdateView(LoginRequiredMixin, UpdateView):
    model = RiskDatabase_03_QualityRisk
    success_url = reverse_lazy('risk_database:view-risk-database')
    fields = ['quality_objective', 'quality_risk', 'quality_risk_ref', 'quality_risk_firm_size']
    template_name = 'riskdatabase/04_c_update_risk.html'

class RiskDatabaseRiskResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = RiskDatabase_04_RiskResponse
    success_url = reverse_lazy('risk_database:view-risk-database')
    fields = ['quality_risk', 'risk_response', 'risk_response_ref','response_mandatory','risk_response_firm_size', 'additional_mercia_guidance']
    template_name = 'riskdatabase/04_d_update_rr.html'

# 05. Delete Category, Objective, Risk and Risk Response entries

class RiskDatabaseCatDeleteView(LoginRequiredMixin, DeleteView):
    model = RiskDatabase_01_QualityObjectiveCategory
    template_name = 'riskdatabase/05_a_delete_cat.html'
    success_url = reverse_lazy('risk_database:view-risk-database')

class RiskDatabaseObjDeleteView(LoginRequiredMixin, DeleteView):
    model = RiskDatabase_02_QualityObjective
    template_name = 'riskdatabase/05_b_delete_obj.html'
    success_url = reverse_lazy('risk_database:view-risk-database')

class RiskDatabaseRiskDeleteView(LoginRequiredMixin, DeleteView):
    model = RiskDatabase_03_QualityRisk
    template_name = 'riskdatabase/05_c_delete_risk.html'
    success_url = reverse_lazy('risk_database:view-risk-database')

class RiskDatabaseRRDeleteView(LoginRequiredMixin, DeleteView):
    model = RiskDatabase_04_RiskResponse
    template_name = 'riskdatabase/05_d_delete_rr.html'
    success_url = reverse_lazy('risk_database:view-risk-database')

# 06. Export to excel

@login_required
def RiskDatabaseExportToExcelView(request):
    print("In Export View")

    # TODO: Consider deleteing user rights if not needed
    # Get the user rights
    context = UserRightsContext(request)

    # context={}
    #
    # context['is_nexia_superuser'] = False
    # context['is_user_manager'] = False
    # is_nexia_superuser = False
    # is_user_manager = False
    #
    # try:
    #     print("In try")
    #     is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = UserAttributes.objects.filter(
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

    # Create the risk library as a dataframe:
    df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
    df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
    df_cat_obj = pd.merge(
        left=df_cat,
        left_on='quality_objective_category_id',
        right=df_obj,
        right_on='quality_objective_category_id',
        how='inner'
    )
    del df_cat, df_obj

    df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
    df_cat_obj_risk = pd.merge(
        left=df_cat_obj,
        left_on='quality_objective_id',
        right=df_risk,
        right_on='quality_objective_id',
        how='inner',
    )
    del df_risk, df_cat_obj

    df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
    df_cat_obj_risk_rr = pd.merge(
        left=df_cat_obj_risk,
        left_on='quality_risk_id',
        right=df_rr,
        right_on='quality_risk_id',
        how='inner',
    )
    del df_cat_obj_risk, df_rr

    df_cat_obj_risk_rr.drop(
        columns=['quality_objective_category_id','quality_objective_id', 'quality_risk_id', 'risk_response_id'],
        inplace=True
    )

    df_cat_obj_risk_rr = df_cat_obj_risk_rr.replace("nan"," ")

    # df_risk_reg = pd.DataFrame(Risk.objects.values()).drop(columns='id')
    print("\n Risk library: \n", df_cat_obj_risk_rr)

    # Create an excel file:
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Risk_Library")

    # General formats:

    text_bold_format = workbook.add_format({'bold': True})
    text_normal_format = workbook.add_format({'bold': False})
    text_bold_red_format = workbook.add_format({'bold': True, 'font_color': 'red'})

    worksheet.hide_gridlines(2)

    # Create table in file:

    data_to_add = np.array(df_cat_obj_risk_rr)

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

    df_cols = df_cat_obj_risk_rr.columns.values

    for col_num, data in enumerate(df_cols):
        worksheet.write(start_row, start_col + col_num, data)

    # Header for table
    worksheet.write(start_row - 2, start_col, "Risk Library:", text_bold_format)

    # END OF CREATE TABLE

    # CLOSE FILE:
    workbook.close()
    output.seek(0)

    # DOWNLOAD FILE:
    # Set up the Http response.

    filename = 'risk_database.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    print(response)
    return response



# # 01.2 View database - button view - DO NOT USE
#
# class ViewRiskDatabaseButtonView(TemplateView):
#     template_name = 'riskdatabase/02_view_risk_database_buttons.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ViewRiskDatabaseButtonView, self).get_context_data(**kwargs)
#
#         context['risk_database'] = [
#             {
#                 "cat":"Cat 1",
#                 "objs":[
#                     {
#                         "obj": "Obj 1",
#                         'risks':[
#                             {
#                                 "risk": "Risk 1",
#                                 "rrs":[
#                                     {"rr":"RR 1"},
#                                     {"rr": "RR 2"},
#                                 ]
#                             },
#                             {"risk": "Risk 2"},
#                         ]
#                     },
#                     {
#                         "obj": "Obj 2",
#                         "risk": "Risk 3",
#                     },
#                 ]
#             }
#         ]
#
#         # cat_list = RiskDatabase_01_QualityObjectiveCategory.objects.values_list('quality_objective_category',flat=True)
#         # print("\nCat list:\n", cat_list)
#         #
#         # obj_list = RiskDatabase_02_QualityObjective.objects.values('quality_objective_category', 'quality_objective')
#         # print("\nCat list:\n", obj_list)
#         #
#         # obj_list_2 = np.array(RiskDatabase_02_QualityObjective.objects.values_list('quality_objective_category', 'quality_objective'))
#         # print("\nCat list 2:\n", obj_list_2)
#
#         df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
#         print("\nDf cat\n",df_cat)
#
#         print("\nCol names from model\n",
#               RiskDatabase_01_QualityObjectiveCategory.objects.values()
#               )
#
#         risk_database_combined = []
#         cat_list = RiskDatabase_01_QualityObjectiveCategory.objects.values()
#         for i in range(len(cat_list)):
#             print(i)
#             cat_dict_temp = {}
#             cat_dict_temp['quality_objective_category_id'] = cat_list[i]['quality_objective_category_id']
#             cat_dict_temp['quality_objective_category'] = cat_list[i]['quality_objective_category']
#
#             obj_list_temp = []
#             obj_list_from_db = RiskDatabase_02_QualityObjective.objects.filter(
#                 quality_objective_category=cat_dict_temp['quality_objective_category_id']
#             ).values()
#
#             for j in range(len(obj_list_from_db)):
#                 obj_dict_temp = {}
#                 obj_dict_temp['quality_objective'] = obj_list_from_db[j]['quality_objective']
#                 obj_dict_temp['quality_objective_id'] = obj_list_from_db[j]['quality_objective_id']
#
#                 risk_list_temp = []
#                 risk_list_from_db = RiskDatabase_03_QualityRisk.objects.filter(
#                     quality_objective=obj_dict_temp['quality_objective_id']
#                 ).values()
#
#                 for k in range(len(risk_list_from_db)):
#                     risk_dict_temp={}
#                     risk_dict_temp['quality_risk'] = risk_list_from_db[k]['quality_risk']
#                     risk_dict_temp['quality_risk_id'] = risk_list_from_db[k]['quality_risk_id']
#                     risk_dict_temp['quality_risk_firm_size'] = risk_list_from_db[k]['quality_risk_firm_size']
#
#                     rr_list_temp = []
#                     rr_list_from_db = RiskDatabase_04_RiskResponse.objects.filter(
#                         quality_risk=risk_dict_temp['quality_risk_id']
#                     ).values()
#
#                     for l in range(len(rr_list_from_db)):
#                         rr_dict_temp = {}
#                         rr_dict_temp['risk_response'] = rr_list_from_db[l]['risk_response']
#
#                     risk_list_temp.append(risk_dict_temp)
#
#                 obj_dict_temp['risks'] = risk_list_temp
#                 obj_list_temp.append((obj_dict_temp))
#
#             cat_dict_temp['objectives'] = obj_list_temp
#
#
#             risk_database_combined.append(cat_dict_temp)
#
#         print("\nRisk database combined\n", risk_database_combined)
#
#
#
#         df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
#         df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
#         df_cat_obj = pd.merge(
#             left=df_cat,
#             left_on='quality_objective_category_id',
#             right=df_obj,
#             right_on='quality_objective_category_id',
#             how='inner'
#         )
#         del df_cat, df_obj
#
#         df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
#         df_cat_obj_risk = pd.merge(
#             left=df_cat_obj,
#             left_on='quality_objective_id',
#             right=df_risk,
#             right_on='quality_objective_id',
#             how='inner',
#         )
#         del df_risk, df_cat_obj
#
#         df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
#         df_cat_obj_risk_rr = pd.merge(
#             left=df_cat_obj_risk,
#             left_on='quality_risk_id',
#             right=df_rr,
#             right_on='quality_risk_id',
#             how='inner',
#         )
#         del df_cat_obj_risk, df_rr
#
#         # context['risk_database_combined'] = df_cat_obj_risk_rr[:10].to_dict()
#         context['risk_database_combined'] = df_cat_obj_risk_rr.to_dict('records', into=defaultdict(list))
#         # del df_cat_obj_risk_rr
#
#         df_combined = df_cat_obj_risk_rr.__deepcopy__()
#
#         # print("\nDf combined:\n", df_combined.head(1))
#         #
#         # print("\nDf combined columns:\n", df_combined.columns.values)
#         #
#         # df_cat = df_combined[['quality_objective_category_id', 'quality_objective_category']]
#         # print("\nDf cat from combined\n", df_cat)
#         # print("\nRisk database combined:\n", context['risk_database_combined'])
#
#         return context