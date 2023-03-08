# import requests
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms as f

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags
import re
import html2text

from riskreg.forms import RiskRegEntryForm, CustomRiskForm, CreateDeficiencyForm, UploadFileForm, QuillFieldForm, QuillModelForm

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

from riskreg.models import RiskRegister, RCA, NonQuillPost, QuillPost


from copy import deepcopy

import pandas as pd
import numpy as np
from collections import OrderedDict, defaultdict

from json import dumps
import os, io
import xlsxwriter


# Create your views here.

class CreateQuill(TemplateView):
    template_name = 'riskreg/99_1_create_quill.html'
    def get_context_data(self, **kwargs):
        context=super(CreateQuill, self).get_context_data()
        context['form']=QuillModelForm()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)

        quillPostForm = QuillModelForm(request.POST)

        if quillPostForm.is_valid():
            print("\nQuill form is valid")
            quillPostForm.save()
        else:
            print("\nQuill form is NOT valid")

        # print("\nContent: ", request.POST['content'])
        #
        # a = request.POST['content']
        #
        # print("\n Find html in a ", a.find('html'))
        #
        # b = a.find('html')
        #
        # c = a[b+7:]
        #
        # print("\n c is: ", c)
        #
        # d = c.find('"')
        # print("\nd is : ", d)
        #
        # e = c[:d]
        #
        # print("\ne is: ", e)
        #
        # QuillPost.objects.get_or_create(
        #     content=e,
        #     text=request.POST['text']
        # )


        return HttpResponseRedirect(reverse('risk_register_2:view_quill'))

class ViewQuillPosts(TemplateView):
    template_name = 'riskreg/99_2_view_quill_posts.html'
    def get_context_data(self, **kwargs):
        context=super(ViewQuillPosts, self).get_context_data()
        context['quillposts'] = QuillPost.objects.all()


        return context

def ImportQuillPost(request):
    print("\n\nIn import quill post")

    df = pd.read_excel("riskreg/Book3.xlsx")
    print("\nDf: \n", df)
    print("\nFirst cell is: ",df.iloc[0,1])

    print("\n",df.to_dict('records', into=defaultdict(list)))

    x = df.to_dict('records', into=defaultdict(list))

    print("\nContent line 1: ",x[0]['Content'])

    x1 = x[0]['Content']

    print("\nX1 is : ", x1)

    print("\nX1 replaced",x1.replace("\n","</p><p>"))
    print("\nX1 replaced",x1.replace("\n","\\\\n"))

    # df_2 = df.to_html()
    # print("\nDf 2: \n", df_2)

    # a = "Others, including the network, network firms, individuals in the network or network firms, or service providers, who are subject to the relevant ethical requirements to which the firm and the firm's engagements are subject:\\\\ni) Understand the relevant ethical requirements that apply to them; and\\\\nii) Fulfil their responsibilities in relation to the relevant ethical requirements that apply to them."
    #
    # print("\nA is: ",a)
    #
    # print("\nA in html is: ",a.replace("\\\\n\\\\n","</p><p><br></p><p>"))

    # QuillPost.objects.get_or_create(
    #     content= '{"delta":"{\\"ops\\":[{\\"insert\\":\\"Para 1.\\\\n\\\\nPara 2.\\\\n\\"}]}","html":"<p>Para 3.</p><p><br></p><p>Para 4.</p>"}',
    #     text= "text"
    # )

    return HttpResponse("import complete")

# ---------------------- 0.2. INSTRUCTIONS ----------------------

class RiskRegInstructions(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/00_02_a_risk_register_instructions.html'
        context = UserRightsContext(request)
        return render(request, template_name=template_name, context=context)


class RiskRegInstructionsISQMSystem(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/00_02_b_isqm_system.html'
        context = UserRightsContext(request)
        return render(request, template_name=template_name, context=context)


class RiskRegInstructionsRiskAssessment(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/00_02_c_risk_assessment.html'
        context = UserRightsContext(request)
        return render(request, template_name=template_name, context=context)

# ---------------------- 1. VIEW RISK REGISTER ----------------------

def textify(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace('\n ', '\n').strip()

def textify2(html):
    h = html2text.HTML2Text()

    # Don't Ignore links, they are useful inside emails
    h.ignore_links = False
    return h.handle(html)



class ViewRiskRegisterView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        print("\nIn view risk reg view\n")

        template_name = 'riskreg/01_view_risk_register.html'
        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr)==0:
            context['is_risk_reg_empty']=True
        else:
            print("\nDf risk register:\n",df_rr.head(3).T)

        # context['form'] = QuillFieldForm()
        #
        # # Read:
        # # https://django-quill-editor.readthedocs.io/en/latest/pages/migrating-to-quillfield.html
        #
        # quill_obj = NonQuillPost.objects.values()
        # print("\nQuill obj: ",quill_obj)
        # print("\nQuill obj len: ", len(quill_obj))
        # print("\nFirst quill obj: ",quill_obj[0],"\n\n")
        #
        # for key in quill_obj[0]:
        #     print("\nKey is: ", key)
        #     print("\nQuil obj for this key is: ",quill_obj[0][key])
        #
        # # print("\nFirst quill obj: ", quill_obj[0]['content'].html, "\n\n")
        #
        #
        # quill_obj2 = NonQuillPost.objects.all()
        #
        # print(
        #     "\nLen of quill obj 2 is: ", len(quill_obj2),"\n",
        #     ""
        #       )
        #
        # for obj in quill_obj2:
        #     print("Content: ", obj.content.html)
        #     print("Text: ", obj.text)
        #     # print("\nQuil obj for this key is: ",quill_obj[0][key])
        #
        # print("\nQuil obj for this key is: ", quill_obj2[0].content.html)
        #
        # context['quill_obj'] = quill_obj2[0].content.html
        #
        # df_data = []
        #
        # for row in NonQuillPost.objects.all():
        #     df_data.append([
        #         row.content.html,
        #         row.text
        #     ])
        #
        # print("\nDf data: \n", df_data)
        #
        # df_q = pd.DataFrame(df_data, columns=[['Content','Text']])
        #
        # print("\nDf_q:\n", df_q)
        #
        # #
        # # for key in quill_obj[0]['content']:
        # #     print("\nKey is: ", key)
        # #     # print("\nQuil obj for this key is: ",quill_obj[0][key])
        #
        # # quill_item_list = []
        # # quill_item_list2 = []
        # # for item in quill_obj:
        # #     print("\nItem is: ",item.content.html)
        # #     quill_item_list.append(textify(item.content.html))
        # #     quill_item_list2.append(textify2(item.content.html).replace("*","").replace("_",""))
        # #
        # #     # new_parser = HtmlToDocx()
        # #     # new_parser.parse_html_file(item.content.html, "docx_filename")
        # #
        # # print("\nQuill item list: ", quill_item_list)
        # # print("\nQuill item list 2: ", quill_item_list2)
        # #
        # # df_quill = pd.DataFrame(quill_item_list)
        # # df_quill.to_excel("quill_list_df.xlsx")
        # #
        # # df_quill2 = pd.DataFrame(quill_item_list2)
        # # df_quill2.to_excel("quill_list_df_2.xlsx")

        if context['does_firm_exist'] == True:
            print("\nFirm exists and is: ",context['current_firm'],"\n")
            rr_df = pd.DataFrame(
                RiskRegister.objects.filter(firm_name_id=context['current_firm']).values()
            )
            print("\nDone.")
            print("\nRR df\n", rr_df)

            rr_def = pd.DataFrame(
                RCA.objects.filter(risk_response__firm_name_id=context['current_firm']).values('identified_deficiency_id','risk_response_id')
                # RCA.objects.filter(risk_response__firm_name_id=context['current_firm'])
            )

            print("\nRR def:\n", rr_def)

            rr_def_combined = pd.DataFrame()

            if len(rr_def>0):

                rr_def_pivot = rr_def.pivot_table(
                    index=['risk_response_id'],
                    values=['identified_deficiency_id'],
                    aggfunc='count'
                )

                print("\nRR def pivot:\n",rr_def_pivot)

                rr_def_combined = pd.merge(
                    left=rr_df,
                    left_on='id',
                    right=rr_def_pivot,
                    right_on='risk_response_id',
                    how='left'
                )
            else:
                rr_def_combined = rr_df.__deepcopy__()
                print("\nIn else , rr ref combined is: ", rr_def_combined)

            rr_def_combined['identified_deficiency_id'] = rr_def_combined['id'].apply(lambda x: 0)


            rr_def_combined['identified_deficiency_id']=rr_def_combined['identified_deficiency_id'].fillna(0)
            print("\nRR def dtypes\n", rr_def_combined.dtypes)
            rr_def_combined['identified_deficiency_id'] = rr_def_combined['identified_deficiency_id'].astype('int')
            print("\nRR def dtypes\n", rr_def_combined.dtypes)
            print("\nRR df combined: \n", rr_def_combined[rr_def_combined['identified_deficiency_id']!=0])

            context['rr_dict'] = rr_def_combined.to_dict('records', into=defaultdict(list))

            # context['rr_dict'] = pd.DataFrame(
            #     RiskRegister.objects.filter(firm_name_id=context['current_firm']).values()
            # ).to_dict('records', into=defaultdict(list))
        else:
            pass
        return render(request, template_name=template_name, context=context)

# ---------------------- 2. CREATE RISK REGISTER ENTRY ----------------------

class CreateRiskRegEntry(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/02_00_create_risk_reg_entry.html'
        context = UserRightsContext(request)
        return render(request, template_name=template_name, context=context)

# ---------------------- 2.0.1 Model Matrices (Risk library tables relationships) ----------------------

class ModelMatrices:
    def create_risk_library_table(self):
        # ------------------------------ Cat - Objective Matrix --------------------

        # df_rd_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
        # df_rr_in_rr = pd.DataFrame(
        #     RiskRegister.objects.filter(firm_name_id=current_firm).values('rd_risk_response_id'))

        df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())

        df_cat_obj = pd.merge(
            left=df_cat,
            right=df_obj,
            left_on="quality_objective_category_id",
            right_on="quality_objective_category_id",
            how="inner"
        )
        del df_obj

        df_cat_dict = df_cat.to_dict('records', into=defaultdict(list))
        del df_cat
        cat_obj_matrix = []

        for cat in df_cat_dict:
            # print("Cat: ",cat,"\n")
            temp_dict = {}
            temp_dict['category'] = cat['quality_objective_category']
            temp_dict['category_id'] = "cat_"+str(cat['quality_objective_category_id'])

            df_cat_obj_dict = df_cat_obj[
                df_cat_obj['quality_objective_category'] == cat['quality_objective_category']].to_dict('records',
                                                                                                       into=defaultdict(
                                                                                                           list))

            # print("\nCat obj dict is:", df_cat_obj_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_risk = []
            for obj in df_cat_obj_dict:
                temp_dict_risk = {}
                temp_dict_risk['objective'] = obj['quality_objective']
                temp_dict_risk['objective_id'] = 'obj_'+str(obj['quality_objective_id'])
                temp_list_risk.append(temp_dict_risk)
                del temp_dict_risk
            temp_dict['objectives'] = temp_list_risk

            cat_obj_matrix.append(temp_dict)

            del temp_dict, df_cat_obj_dict

        # print("Cat obj matrix is: \n", cat_obj_matrix)
        # ------------------------------ END OF Cat - Objective Matrix --------------------

        # ------------------------------ Objective - Risk Matrix --------------------

        # print("\n OBJECTIVE RISK MATRIX \n")

        df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
        df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())

        # print(df_obj.columns.values)
        # print("\n",df_risk.columns.values)

        df_obj_risk = pd.merge(
            left=df_obj,
            right=df_risk,
            left_on="quality_objective_id",
            right_on="quality_objective_id",
            how="inner"
        )
        del df_risk
        # print(df_obj_risk.head())
        # print("Obj risk columns: ",df_obj_risk.columns.values,"\n")

        df_obj_dict = df_obj.to_dict('records', into=defaultdict(list))
        obj_risk_matrix = []
        #
        for obj in df_obj_dict:
            # print("Obj: ", obj, "\n")
            temp_dict = {}
            temp_dict['objective'] = obj['quality_objective']
            temp_dict['objective_id'] = 'obj_'+str(obj['quality_objective_id'])

            df_obj_risk_dict = df_obj_risk[
                df_obj_risk['quality_objective'] == obj['quality_objective']].to_dict('records', into=defaultdict(list))
            # print("\nCat obj dict is:", df_obj_risk_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_risk = []
            for risk in df_obj_risk_dict:
                temp_dict_risk = {}
                temp_dict_risk['quality_risk'] = risk['quality_risk']
                temp_dict_risk['quality_risk_id'] = 'risk_'+str(risk['quality_risk_id'])
                temp_list_risk.append(temp_dict_risk)
                del temp_dict_risk
            temp_dict['risks'] = temp_list_risk

            obj_risk_matrix.append(temp_dict)

            del temp_dict, df_obj_risk_dict

        # print(obj_risk_matrix)

        # -------------- END OF OBJ RISK MATRIX --------------------

        # ------------------------------ RISK - RISK RESPONSE Matrix --------------------

        # print("\n RISK - RISK RESPONSE MATRIX \n")

        df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
        df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())

        # print(df_obj.columns.values)
        # print("\n",df_risk.columns.values)

        df_risk_rr = pd.merge(
            left=df_risk,
            right=df_rr,
            left_on="quality_risk_id",
            right_on="quality_risk_id",
            how="inner"
        )
        del df_rr
        # print(df_risk_rr.head())

        df_risk_dict = df_risk.to_dict('records', into=defaultdict(list))
        risk_rr_matrix = []
        #
        for risk in df_risk_dict:
            # print("Obj: ", obj, "\n")
            temp_dict = {}
            temp_dict['quality_risk'] = risk['quality_risk']
            temp_dict['quality_risk_id'] = 'risk_'+str(risk['quality_risk_id'])

            df_risk_rr_dict = df_risk_rr[
                df_risk_rr['quality_risk'] == risk['quality_risk']].to_dict('records', into=defaultdict(list))
            # print("\nCat obj dict is:", df_obj_risk_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_rr = []
            for rr in df_risk_rr_dict:
                temp_dict_rr = {}
                temp_dict_rr['risk_response'] = rr['risk_response']
                temp_dict_rr['risk_response_id'] = 'rr_'+str(rr['risk_response_id'])
                temp_list_rr.append(temp_dict_rr)
                del temp_dict_rr
            temp_dict['rr'] = temp_list_rr

            risk_rr_matrix.append(temp_dict)

            del temp_dict, df_risk_rr_dict

        return cat_obj_matrix, obj_risk_matrix, risk_rr_matrix

    def merge_risk_library_tables(self, df_for_input, entry_type):
        # Obtain the values stored in the risk library models
        df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
        df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
        df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())

        print("\nObtained risk library matrices\n")
        # Starting from the risk response model, merge each model to the dataframe created from response.post
        print("\nTo start merging with risk library. Entry type at start is: ",entry_type)
        if entry_type=="rd_entry":
            df_for_input = pd.merge(
                left=df_rr,
                left_on='risk_response_id',
                right=df_for_input,
                right_on='risk_response_id',
                how="inner",
            )
            entry_type = "custom_rr"
            print('\nlevel 0 done and entry type changed to: ',entry_type)
        else:
            pass
        if entry_type=="custom_rr":
            df_for_input = pd.merge(
                left=df_risk,
                left_on='quality_risk_id',
                right=df_for_input,
                right_on='quality_risk_id',
                how='inner'
            )
            entry_type = "custom_r_rr"
            print('\nlevel 1 done and entry type changed to: ', entry_type)
        else:
            pass
        if entry_type=="custom_r_rr":
            df_for_input = pd.merge(
                left=df_obj,
                left_on='quality_objective_id',
                right=df_for_input,
                right_on='quality_objective_id',
                how='inner'
            )
            entry_type = "custom_o_r_rr"
            print('\nlevel 2 done and entry type changed to: ', entry_type)
        else:
            pass
        if entry_type=='custom_o_r_rr':
            df_for_input = pd.merge(
                left=df_cat,
                left_on='quality_objective_category_id',
                right=df_for_input,
                right_on='quality_objective_category_id',
                how='inner'
            )
            print('\nlevel 3 done')
        else:
            pass

        return df_for_input

# ---------------------- 2.0.1 End of Model Matrices ----------------------

# ---------------------- 2.0.2 Get user selection from request.post ----------------------

def GetSelection(request, entry_type):
    # print(request.POST)

    print("Current user: ", request.user.id)
    print("Current user: ", request.user)
    print("Current user: ", request.user.first_name)

    # Obtain a list of risk response ids from "requst.POST" that have been selected:
    rr_selection_list = [x.replace("_selection", "") for x in list(request.POST) if "_selection" in x]
    # ONLY FOR DEV:

    temp_list = []
    response_post_list = list(request.POST)
    print("\nLength of Response post list is: ", len(response_post_list), "\n")
    for rr in rr_selection_list:
        print("\nrr is ", rr)
        temp_dict = {}
        i = 0
        while i < len(response_post_list):
            key = response_post_list[i]
            if rr in key:
                # print("key is: ", key)
                # print('RR found: ', rr, ' Dict is empty? :', not bool(temp_dict))
                if "_selection" in key:
                    temp_dict[entry_type + '_id'] = rr
                    # print("Selection added")
                else:
                    temp_dict[key.replace(rr + "_", "")] = request.POST[key]
                    # print("Other key added")

                # print("Key to be removed is: ",key)
                response_post_list.remove(key)
                # print("Removed and Length of Response post list is: ", len(temp_response_post_list))
            else:
                i = i + 1
            del key
            # print("\ni after the loop is: ", i, " and length of request post list is: ", len(response_post_list))

        if bool(temp_dict):
            temp_list.append(temp_dict)
        else:
            pass
        del temp_dict

        df_selection_values = pd.DataFrame(temp_list)
        del temp_list

        print("\n Dataframe selection: \n", df_selection_values)
        print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))



        # Use an if statement to determine the abbreviation of the entry type for below
        entry_type_abbrev = "rr_"
        if entry_type == "risk_response":
            pass
        elif entry_type == "quality_risk":
            entry_type_abbrev = "risk_"
        elif entry_type == "quality_objective":
            entry_type_abbrev = "obj_"
        elif entry_type == "quality_objective_category":
            entry_type_abbrev = "cat_"
        else:
            pass

        print("\nEntry type abbrev is: ",entry_type_abbrev)

        def return_rr(x):
            return int(x.replace(entry_type_abbrev, ""))

        df_selection_values[entry_type + '_id'] = df_selection_values[entry_type + '_id'].apply(
            lambda x: return_rr(x))

        print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))

        return df_selection_values

# ---------------------- 2.0.2 End of get user selection from request.post ----------------------

# ---------------------- 2.1 Five entry choices ----------------------

# ---------------------- 2.1.1 Risk Library Entries ----------------------

class CreateRiskRegTabView(LoginRequiredMixin, TemplateView, ModelMatrices):

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        print("\nIn Create Risk reg tab view\n")
        template_name = 'riskreg/02_01_risk_library_entry.html'
        context = UserRightsContext(request)
        context["cat_obj_matrix"], context["obj_risk_matrix"], context[
            "risk_rr_matrix"] = self.create_risk_library_table()
        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted in create risk reg 2 view\n")
            # # Obtain a list of risk response ids from "requst.POST" that have been selected:
            # rr_selection_list = [x.replace("_selection", "") for x in list(request.POST) if "_selection" in x]
            # # ONLY FOR DEV:
            #
            # temp_list = []
            # response_post_list = list(request.POST)
            # print("\nLength of Response post list is: ",len(response_post_list),"\n")
            # for rr in rr_selection_list:
            #     print("\nrr is ", rr)
            #     temp_dict = {}
            #     i = 0
            #     while i < len(response_post_list):
            #         key = response_post_list[i]
            #         if rr in key:
            #             print("key is: ",key)
            #             print('RR found: ',rr, ' Dict is empty? :', not bool(temp_dict))
            #             if "_selection" in key:
            #                 temp_dict['risk_response_id'] = rr
            #                 print("Selection added")
            #             else:
            #                 temp_dict[key.replace(rr + "_", "")] = request.POST[key]
            #                 print("Other key added")
            #             # if not bool(temp_dict):
            #             #     # print("Dict is empty and adding id")
            #             #     temp_dict['risk_response_id'] = rr
            #             # else:
            #             #     # print("dict is NOT empty")
            #             #     pass
            #             # temp_dict[key.replace(rr + "_", "")] = request.POST[key]
            #             # print("Key to be removed is: ",key)
            #             response_post_list.remove(key)
            #             # print("Removed and Length of Response post list is: ", len(temp_response_post_list))
            #             # print("temp req post list is: ",temp_response_post_list, "\n and other is: ",response_post_list)
            #         else:
            #             i = i + 1
            #         del key
            #         print("\ni after the loop is: ",i, " and length of request post list is: ", len(response_post_list))
            #     # print("After first RR loop, temp rep.post list is: ", temp_response_post_list, "\n")
            #
            #     if bool(temp_dict):
            #         temp_list.append(temp_dict)
            #     else:
            #         pass
            #     del temp_dict
            #
            # df_selection_values = pd.DataFrame(temp_list)


            # del temp_list
            # print("\n Dataframe selection: \n", df_selection_values)
            # print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))
            #
            # def return_rr(x):
            #     return int(x.replace("rr_", ""))
            #
            # df_selection_values['risk_response_id'] = df_selection_values['risk_response_id'].apply(
            #     lambda x: return_rr(x))
            #
            # print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))

            # Obtain the values posted for the risk register entry from request.post where a tick box was selected:
            df_selection_values = GetSelection(request, entry_type='risk_response')
            print("\nDf selection values:\n",df_selection_values)

            df_for_input = self.merge_risk_library_tables(df_for_input=df_selection_values, entry_type='rd_entry')
            print("\nDf for input:\n", df_for_input)

            # Convert the dataframe into a dictionary for input into the Risk Register model
            df_for_input_dict = df_for_input.to_dict('records', into=defaultdict(list))
            print("\nDf for input dict: \n", df_for_input_dict)

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[
                    0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # # Pass the variable to a view to show the data to be input and confirm its right:
                # return ConfirmCreateEntryView(request, df_for_input_dict)
                #
                # # This was used to input data here. Now being passed to another function:

                # Input each row of the above dictionary into the Risk Register model
                for row in df_for_input_dict:
                    print("\nIn row to input into RRs:\n")

                    RiskRegister.objects.get_or_create(
                        firm_name=Firm.objects.get(firm_id=current_firm),

                        quality_objective_category=row['quality_objective_category'],
                        quality_objective=row['quality_objective'],
                        quality_risk=row['quality_risk'],
                        quality_risk_firm_size=row['quality_risk_firm_size'],
                        risk_response=row['risk_response'],
                        owner=row['owner'],
                        response_mandatory=row['response_mandatory'],
                        risk_response_firm_size=row['risk_response_firm_size'],
                        response_type=row['risk_response_type'],
                        risk_response_source='Risk library',
                        response_status=row['risk_response_status'],
                        comments=row['comments'],
                        frequency_of_review=row['review_frequency'],
                        created_by=request.user.first_name + " " + request.user.last_name,
                        sign_off_owner=row['sign_off_owner'],
                        sign_off_reviewer=row['sign_off_reviewer'],
                        entry_type='rd_entry',
                        rd_risk_response_id=row['risk_response_id'],
                    )

                    print("\nCreated Risk entry")

                print("\nDONE")
            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register_2:"))

            # Input each row of the above dictionary into the Risk Register model
            # for row in df_for_input_dict:
            #     RiskRegister.objects.get_or_create(
            #         quality_objective_category=row['quality_objective_category'],
            #         quality_objective=row['quality_objective'],
            #         quality_risk=row['quality_risk'],
            #         quality_risk_mandatory=row['quality_risk_mandatory'],
            #         quality_risk_firm_size=row['quality_risk_firm_size'],
            #         owner=row['owner'],
            #         risk_response=row['risk_response'],
            #         response_mandatory=row['response_mandatory'],
            #         risk_response_firm_size=row['risk_response_firm_size'],
            #         response_type=row['risk_response_type'],
            #         risk_response_source='Risk library',
            #         response_status=row['risk_response_status'],
            #         comments=row['comments'],
            #         frequency_of_review=row['review_frequency'],
            #         created_by=request.user,
            #         sign_off_owner=row['sign_off_owner'],
            #         sign_off_reviewer=row['sign_off_reviewer'],
            #         # upload_files='',
            #     )

            print("\nDONE")

            return HttpResponseRedirect(reverse("risk_register_2:success"))
        except:
            # Todo: Need to print an error message here instead of redirecting
            return HttpResponse("ERROR: Please retry the previous operation.")

# ---------------------- 2.1.1 End of Risk Library Entries ----------------------

# ---------------------- 2.1.2 Custom Risk Response Entries ----------------------

class CustomRREntryView(LoginRequiredMixin, TemplateView, ModelMatrices):

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/02_02_custom_rr_entry.html'
        context = UserRightsContext(request)
        context["cat_obj_matrix"], context["obj_risk_matrix"], context[
            "risk_rr_matrix"] = self.create_risk_library_table()
        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted in Custom RR view\n")
            # print("\nRequest.post is:\n", request.POST)

            # Obtain the values posted for the risk register entry from request.post where a tick box was selected:
            df_selection_values = GetSelection(request, entry_type='quality_risk')
            print("\nGet selection successful!\n")
            print("\nDf selection values:\n",df_selection_values)

            df_for_input = self.merge_risk_library_tables(df_for_input=df_selection_values, entry_type='custom_rr')
            print("\nDf for input:\n", df_for_input)

            # Convert the dataframe into a dictionary for input into the Risk Register model
            df_for_input_dict = df_for_input.to_dict('records', into=defaultdict(list))
            print("\nDf for input dict: \n", df_for_input_dict)
            print("\nDf for input columns: \n", df_for_input.columns.values)

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # Input each row of the above dictionary into the Risk Register model
                for row in df_for_input_dict:
                    print("\nIn row to input into RRs:\n")

                    RiskRegister.objects.create(
                        firm_name=Firm.objects.get(firm_id=current_firm),

                        quality_objective_category=row['quality_objective_category'],
                        quality_objective=row['quality_objective'],
                        quality_risk=row['quality_risk'],
                        quality_risk_firm_size=row['quality_risk_firm_size'],
                        risk_response=row['risk_response'],
                        owner=row['owner'],
                        response_mandatory=row['response_mandatory'],
                        risk_response_firm_size=row['risk_response_firm_size'],
                        response_type=row['risk_response_type'],
                        risk_response_source='Risk library',
                        response_status=row['risk_response_status'],
                        comments=row['comments'],
                        frequency_of_review=row['review_frequency'],
                        created_by=request.user.first_name + " " + request.user.last_name,
                        sign_off_owner=row['sign_off_owner'],
                        sign_off_reviewer=row['sign_off_reviewer'],
                        entry_type='custom_rr',
                        rd_risk_response_id=0,
                    )

                    print("\nCreated Custom Risk Response entry")
                print("\nDONE")
            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register_2:error"))
            print("\nDONE")
            return HttpResponseRedirect(reverse("risk_register_2:success"))
        except:
            # Todo: Need to print an error message here instead of redirecting
            return HttpResponse("ERROR: Please retry the previous operation.")

# ---------------------- 2.1.2 End of Custom Risk Response Entries ----------------------

# ---------------------- 2.1.3 Custom Risk and Risk Response Entries ----------------------

class CustomRisk_RREntryView(LoginRequiredMixin, TemplateView, ModelMatrices):

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/02_03_custom_r_rr_entry.html'
        context = UserRightsContext(request)
        context["cat_obj_matrix"], context["obj_risk_matrix"], context[
            "risk_rr_matrix"] = self.create_risk_library_table()
        return render(request, template_name=template_name, context=context)

    # def get_context_data(self, **kwargs):
    #     context = super(CustomRisk_RREntryView, self).get_context_data(**kwargs)
    #     context["cat_obj_matrix"], context["obj_risk_matrix"], context[
    #         "risk_rr_matrix"] = self.create_risk_library_table()
    #     return context

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted in Custom RR view\n")
            # print("\nRequest.post is:\n", request.POST)

            # Obtain the values posted for the risk register entry from request.post where a tick box was selected:
            df_selection_values = GetSelection(request, entry_type='quality_objective')
            print("\nGet selection successful!\n")
            print("\nDf selection values:\n",df_selection_values)

            df_for_input = self.merge_risk_library_tables(df_for_input=df_selection_values, entry_type='custom_r_rr')
            print("\nDf for input:\n", df_for_input)

            # Convert the dataframe into a dictionary for input into the Risk Register model
            df_for_input_dict = df_for_input.to_dict('records', into=defaultdict(list))
            print("\nDf for input dict: \n", df_for_input_dict)
            print("\nDf for input columns: \n", df_for_input.columns.values)

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # Input each row of the above dictionary into the Risk Register model
                for row in df_for_input_dict:
                    print("\nIn row to input into risk entry:\n")

                    RiskRegister.objects.create(
                        firm_name=Firm.objects.get(firm_id=current_firm),

                        quality_objective_category=row['quality_objective_category'],
                        quality_objective=row['quality_objective'],
                        quality_risk=row['quality_risk'],
                        quality_risk_firm_size=row['quality_risk_firm_size'],
                        risk_response=row['risk_response'],
                        owner=row['owner'],
                        response_mandatory=row['response_mandatory'],
                        risk_response_firm_size=row['risk_response_firm_size'],
                        response_type=row['risk_response_type'],
                        risk_response_source='Risk library',
                        response_status=row['risk_response_status'],
                        comments=row['comments'],
                        frequency_of_review=row['review_frequency'],
                        created_by=request.user.first_name + " " + request.user.last_name,
                        sign_off_owner=row['sign_off_owner'],
                        sign_off_reviewer=row['sign_off_reviewer'],
                        entry_type='custom_r_rr',
                        rd_risk_response_id=0,
                    )

                    print("\nCreated Custom Risk and Risk Response entry")
                print("\nDONE")
            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register_2:error"))
            print("\nDONE")
            return HttpResponseRedirect(reverse("risk_register_2:success"))
        except:
            # Todo: Need to print an error message here instead of redirecting
            return HttpResponse("ERROR: Please retry the previous operation.")

# ---------------------- 2.1.3 End of Custom Risk Response Entries ----------------------

# ---------------------- 2.1.4 Custom Objective, Risk and Risk Response Entries ----------------------

class CustomObjRiskRREntryView(LoginRequiredMixin, TemplateView, ModelMatrices):
    template_name = 'riskreg/02_04_custom_o_r_rr.html'

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    def get_context_data(self, **kwargs):
        context = super(CustomObjRiskRREntryView, self).get_context_data(**kwargs)
        context["cat_obj_matrix"], context["obj_risk_matrix"], context[
            "risk_rr_matrix"] = self.create_risk_library_table()
        return context

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted in Custom RR view\n")
            # print("\nRequest.post is:\n", request.POST)

            # Obtain the values posted for the risk register entry from request.post where a tick box was selected:
            df_selection_values = GetSelection(request, entry_type='quality_objective_category')
            print("\nGet selection successful!\n")
            print("\nDf selection values:\n",df_selection_values)

            df_for_input = self.merge_risk_library_tables(df_for_input=df_selection_values, entry_type='custom_o_r_rr')
            print("\nDf for input:\n", df_for_input)

            # Convert the dataframe into a dictionary for input into the Risk Register model
            df_for_input_dict = df_for_input.to_dict('records', into=defaultdict(list))
            print("\nDf for input dict: \n", df_for_input_dict)
            print("\nDf for input columns: \n", df_for_input.columns.values)

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # Input each row of the above dictionary into the Risk Register model
                for row in df_for_input_dict:
                    print("\nIn row to input into risk entry:\n")

                    RiskRegister.objects.create(
                        firm_name=Firm.objects.get(firm_id=current_firm),

                        quality_objective_category=row['quality_objective_category'],
                        quality_objective=row['quality_objective'],
                        quality_risk=row['quality_risk'],
                        quality_risk_firm_size=row['quality_risk_firm_size'],
                        risk_response=row['risk_response'],
                        owner=row['owner'],
                        response_mandatory=row['response_mandatory'],
                        risk_response_firm_size=row['risk_response_firm_size'],
                        response_type=row['risk_response_type'],
                        risk_response_source='Risk library',
                        response_status=row['risk_response_status'],
                        comments=row['comments'],
                        frequency_of_review=row['review_frequency'],
                        created_by=request.user.first_name + " " + request.user.last_name,
                        sign_off_owner=row['sign_off_owner'],
                        sign_off_reviewer=row['sign_off_reviewer'],
                        entry_type='custom_o_r_rr',
                        rd_risk_response_id=0,
                    )

                    print("\nCreated Custom Objective Risk and Risk Response entry")
                print("\nDONE")
            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register_2:error"))
            print("\nDONE")
            return HttpResponseRedirect(reverse("risk_register_2:success"))
        except:
            # Todo: Need to print an error message here instead of redirecting
            return HttpResponse("ERROR: Please retry the previous operation.")

# ---------------------- 2.1.4 End of Objective, Custom Risk Response Entries ----------------------

# ---------------------- 2.1.5 Custom Category, Objective, Risk and Risk Response Entries ----------------------

class CustomEntryView(LoginRequiredMixin, TemplateView, ModelMatrices):
    template_name = 'riskreg/02_05_custom_entry.html'

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    # def get_context_data(self, **kwargs):
    #     context = super(CustomObjRiskRREntryView, self).get_context_data(**kwargs)
    #     context["cat_obj_matrix"], context["obj_risk_matrix"], context[
    #         "risk_rr_matrix"] = self.create_risk_library_table()
    #     return context

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted in Custom entry view\n")
            # print("\nRequest.post is:\n", request.POST)

            # Obtain the values posted for the risk register entry from request.post where a tick box was selected:
            inputs_dict = request.POST

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # Input each row of the above dictionary into the Risk Register model
                print("\nIn row to input into risk entry:\n")

                RiskRegister.objects.create(
                    firm_name=Firm.objects.get(firm_id=current_firm),

                    quality_objective_category=inputs_dict['quality_objective_category'],
                    quality_objective=inputs_dict['quality_objective'],
                    quality_risk=inputs_dict['quality_risk'],
                    quality_risk_firm_size="All",
                    risk_response=inputs_dict['risk_response'],
                    owner=inputs_dict['owner'],
                    response_mandatory="No",
                    risk_response_firm_size="All",
                    response_type=inputs_dict['response_type'],
                    risk_response_source="Custom entry",
                    response_status=inputs_dict['response_status'],
                    comments=inputs_dict['comments'],
                    frequency_of_review=inputs_dict['review_frequency'],
                    created_by=request.user.first_name + " " + request.user.last_name,
                    sign_off_owner=inputs_dict['sign_off_owner'],
                    sign_off_reviewer=inputs_dict['sign_off_reviewer'],
                    entry_type='custom_c_o_r_rr',
                    rd_risk_response_id=0,
                )

                print("\nCreated Custom entry")
                print("\nDONE")
            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register_2:error"))
            print("\nDONE")
            return HttpResponseRedirect(reverse("risk_register_2:success"))
        except:
            # Todo: Need to print an error message here instead of redirecting
            return HttpResponse("ERROR: Please retry the previous operation.")

# ---------------------- 2.1.5 End of Custom Category, Objective, Custom Risk Response Entries ----------------------

# ---------------------- 2.1.6 Update risk library entry ----------------------

class UpdateRLEntry(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        risk_reg_entry = RiskRegister.objects.filter(id=self.kwargs['pk']).values()
        print(risk_reg_entry)
        template_name = ''
        if risk_reg_entry[0]['entry_type'] == 'rd_entry':
            context['form'] = RiskRegEntryForm(risk_reg_entry[0])
            template_name = 'riskreg/02_06_update_risk_library_entry.html'
        else:
            context['form'] = CustomRiskForm(risk_reg_entry[0])
            template_name = 'riskreg/02_07_update_custom_entry.html'
        context['risk_reg_entry'] = risk_reg_entry[0]
        # template_name = 'riskreg/02_06_update_risk_library_entry.html'

        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        print("Update RL Entry post: ", request.POST)

        # Model.objects.filter(id=223).update(field1=2)

        entry_type = RiskRegister.objects.filter(id=request.POST['rr_id']).values_list('entry_type')[0][0]

        print("\nEntry type: ", entry_type)

        if entry_type =='rd_entry':
            print("Choice 1")
            RiskRegister.objects.filter(id=request.POST['rr_id']).update(
                # quality_objective_category=request.POST['quality_objective_category'],
                # quality_objective=request.POST['quality_objective'],
                # quality_risk=request.POST['quality_risk'],
                # risk_response=request.POST['risk_response'],
                owner=request.POST['owner'],
                response_type=request.POST['response_type'],
                response_status=request.POST['response_status'],
                comments=request.POST['comments'],
                frequency_of_review=request.POST['frequency_of_review'],
                created_by=request.POST['created_by'],
                sign_off_owner=request.POST['sign_off_owner'],
                sign_off_reviewer=request.POST['sign_off_reviewer'],
            )
        else:
            print("Choice 2")
            RiskRegister.objects.filter(id=request.POST['rr_id']).update(
                quality_objective_category=request.POST['quality_objective_category'],
                quality_objective=request.POST['quality_objective'],
                quality_risk=request.POST['quality_risk'],
                risk_response=request.POST['risk_response'],
                owner=request.POST['owner'],
                response_type=request.POST['response_type'],
                response_status=request.POST['response_status'],
                comments=request.POST['comments'],
                frequency_of_review=request.POST['frequency_of_review'],
                created_by=request.POST['created_by'],
                sign_off_owner=request.POST['sign_off_owner'],
                sign_off_reviewer=request.POST['sign_off_reviewer'],
            )

        return HttpResponseRedirect(reverse('risk-register-2:view-risk-register'))

# ---------------------- 2.1.6 End of Update risk library entry ----------------------

# ---------------------- 2.1.7 Delete entry ----------------------

# TODO: Create a function for delete entry

class DeleteRiskRegEntry(LoginRequiredMixin, DeleteView):
    template_name = 'riskreg/02_08_delete_risk_reg_entry.html'
    context_object_name = 'risk_reg_entry'
    model = RiskRegister
    success_url = reverse_lazy('index')


# ---------------------- 2.1.7 End of Delete entry ----------------------

# ---------------------- 2.1.8 Export Risk Register ----------------------

@login_required()
def RiskRegisterExportToExcelView(request):
    print("In Risk Reg Export View")

    # TODO: Consider deleteing user rights if not needed
    # Get the user rights
    context={}

    context['is_nexia_superuser'] = False
    context['is_user_manager'] = False
    is_nexia_superuser = False
    is_user_manager = False

    try:
        # print("In try")
        is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = UserAttributes.objects.filter(
            user_id=request.user.id
        ).values_list('is_preparer', 'is_reviewer', 'is_ult_authority', 'is_user_manager', 'is_nexia_superuser')[0]
        context['is_preparer'] = is_preparer
        context['is_reviewer'] = is_reviewer
        context['is_ult_authority'] = is_ult_authority
        context['is_nexia_superuser'] = is_nexia_superuser
        context['is_user_manager'] = is_user_manager
        # print("try succesful")
    except:
        if request.user == "nexiaenhancesuperuser":
            is_nexia_superuser = True
            is_user_manager = True
            context['is_nexia_superuser'] = True
            context['is_user_manager'] = True
        else:
            is_nexia_superuser = False
            is_user_manager = False

    # print("\nUser rights: NSU, UM\n", context['is_nexia_superuser'], context['is_user_manager'])

    # # Create the risk library as a dataframe:
    # df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
    # df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
    # df_cat_obj = pd.merge(
    #     left=df_cat,
    #     left_on='quality_objective_category_id',
    #     right=df_obj,
    #     right_on='quality_objective_category_id',
    #     how='inner'
    # )
    # del df_cat, df_obj
    #
    # df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
    # df_cat_obj_risk = pd.merge(
    #     left=df_cat_obj,
    #     left_on='quality_objective_id',
    #     right=df_risk,
    #     right_on='quality_objective_id',
    #     how='inner',
    # )
    # del df_risk, df_cat_obj
    #
    # df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
    # df_cat_obj_risk_rr = pd.merge(
    #     left=df_cat_obj_risk,
    #     left_on='quality_risk_id',
    #     right=df_rr,
    #     right_on='quality_risk_id',
    #     how='inner',
    # )
    # del df_cat_obj_risk, df_rr
    #
    # df_cat_obj_risk_rr.drop(
    #     columns=['quality_objective_category_id','quality_objective_id', 'quality_risk_id', 'risk_response_id'],
    #     inplace=True
    # )
    #
    # # df_risk_reg = pd.DataFrame(Risk.objects.values()).drop(columns='id')
    # print("\n Risk library: \n", df_cat_obj_risk_rr)

    # Create the risk register as a dataframe:

    rr_df = pd.DataFrame(
        RiskRegister.objects.values(
            'quality_objective_category', 'quality_objective',
             'quality_risk', 'risk_response', 'owner', 'response_type',
             'risk_response_source', 'response_status', 'comments', 'frequency_of_review',
             'created_by', 'sign_off_owner', 'sign_off_reviewer'
        )
    )
    print("Risk reg database: ","\n",rr_df)
    print("Risk reg database columns: ", "\n", rr_df.columns.values)


    # Unmark from here

    # Create an excel file:
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Risk_Register")

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
    worksheet.write(start_row - 2, start_col, "Risk register:", text_bold_format)

    # END OF CREATE TABLE

    # CLOSE FILE:
    workbook.close()
    output.seek(0)

    # DOWNLOAD FILE:
    # Set up the Http response.

    filename = 'risk_register.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    print(response)

    return response

    # return render(request,template_name='riskreg/01_view_risk_register.html')

# ---------------------- 2.8 End of Export Risk Register ----------------------


# ---------------------- 2.9 Import Risk Register ----------------------
class RiskRegisterImportView(LoginRequiredMixin, TemplateView):


    def __init__(self):
        super(RiskRegisterImportView, self).__init__()
        self.df_temp = pd.DataFrame
        self.df_risk_reg_entries = pd.DataFrame()

    def get(self, request, *args, **kwargs):
        template_name = 'riskreg/02_12_import_risk_register.html'
        context = UserRightsContext(request)
        context['can_import'] = False

        if True in list([context['is_preparer'],context['is_reviewer'], context['is_nexia_superuser'], context['is_nexia_superuser']]):
            print("Can import")
            context['can_import'] = True
        else:
            print("cant import")

        context['form'] = UploadFileForm()
        return render(request, template_name=template_name,context=context)

    def cleanse_sheet(self,sheet, risk_response_source, entry_type):
        try:
            self.df_temp['SNO'] = np.arange(1, len(self.df_temp) + 1)

            print("Step 1 parse done")

            if risk_response_source=="Custom entry":
                self.df_temp = self.df_temp[['SNO', 'Quality objective', 'Quality Risk',
                                             'Responses to address the quality risks',
                                             'Owner',
                                             'Response type', 'Response status', 'Comments', 'Review frequency']]
            else:
                self.df_temp = self.df_temp[['SNO', 'Quality objective', 'Quality Risk',
                               'Responses to address the quality risks', 'Mandatory?', 'Applicable?', 'Owner',
                               'Response type', 'Response status', 'Comments', 'Review frequency']]

            print("Step 2 Filter done")

            df_1 = self.df_temp[['SNO', 'Quality objective', 'Quality Risk',
                            'Responses to address the quality risks']]
            df_1.fillna(method="ffill", inplace=True)

            print("Step 3 Fill na done")

            if risk_response_source=="Custom entry":
                df_2 = self.df_temp[['SNO', 'Owner',
                                     'Response type', 'Response status', 'Comments', 'Review frequency']]
            else:
                df_2 = self.df_temp[['SNO', 'Mandatory?', 'Applicable?', 'Owner',
                            'Response type', 'Response status', 'Comments', 'Review frequency']]

            print("Step 4 second df done")

            self.df_temp = pd.merge(left=df_1, left_on="SNO", right=df_2, right_on="SNO", how="inner")
            del df_1, df_2

            print("Step 5 merge two dfs")

            if risk_response_source == "Custom entry":
                pass
            else:
                self.df_temp = self.df_temp[self.df_temp['Applicable?'] == "Yes"]

            print("Step 6 Filter by applicable done")

            self.df_temp.drop(columns=["SNO"], inplace=True)

            print("Step 7 dropped SNO done")

            self.df_temp['Quality objective category'] = self.df_temp['Quality objective'].apply(lambda x: sheet)
            self.df_temp['Risk response source'] = self.df_temp['Quality objective'].apply(lambda x: risk_response_source)
            self.df_temp['Entry type'] = self.df_temp['Quality objective'].apply(lambda x: entry_type)

            print("Step 8 added cat, rr source and entry type to col done")

            df_rl_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values('risk_response','risk_response_id'))

            print("\nRL RR cols: ", df_rl_rr.columns.values,"\n")

            self.df_temp = pd.merge(left=self.df_temp, left_on='Responses to address the quality risks', right=df_rl_rr, right_on='risk_response', how='left')
            self.df_temp.drop(columns=['risk_response'], inplace=True)
            self.df_temp['risk_response_id'] = self.df_temp['risk_response_id'].fillna(0)

            print("\nDf temp len: ", len(self.df_temp))
            print("\nDf temp cols: ", self.df_temp.columns.values)

        except:
            self.df_temp = pd.DataFrame()

        return self.df_temp

    def post(self, request, *args, **kwargs):
        print("Form has been posted")

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("File found")

            # df = pd.read_excel(request.FILES['file'],engine = 'openpyxl')

            risk_reg_xl = pd.ExcelFile(request.FILES['file'])

            risk_reg_sheets = ['Governance and Leadership',
                               'Relevant Ethical Requirements',
                               'Acceptance and Continuance',
                               'Engagement performance',
                               'Resources',
                               'Information and Communication',
                               'Custom risks']

            # self.df_risk_reg_entries = pd.DataFrame()

            for sheet in risk_reg_sheets:
                try:
                    print("\n\nSheet name: ", sheet)

                    self.df_temp = risk_reg_xl.parse(sheet)
                    print("Step 0 - parse done")

                    if sheet == 'Custom risks':
                        self.df_temp = self.cleanse_sheet(sheet, "Custom entry", "custom_c_o_r_rr")
                    else:
                        self.df_temp = self.cleanse_sheet(sheet, "Risk library", "rd_entry")
                    print(type(self.df_temp))

                    self.df_risk_reg_entries = pd.concat([self.df_risk_reg_entries, self.df_temp], ignore_index=True)
                except:
                    pass

            len(self.df_risk_reg_entries)
            print(self.df_risk_reg_entries)

            # self.df_risk_reg_entries.to_excel("risk_reg_combined.xlsx")

            df_for_input_dict = self.df_risk_reg_entries.to_dict('records', into=defaultdict(list))
            print("\nDf for input dict: \n", df_for_input_dict[0])

            # Find out the firm of the current user
            current_firm = 0
            current_user = request.user

            if str(current_user) == "nexiaenhancesuperuser":
                print("\nNESU\n")
            else:
                print("\nNot NESU\n")
                current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[
                    0]
                print("In Not Nesu, current firm is: ", current_firm)

            if current_firm != 0:
                print("Firm exists")

                # # Pass the variable to a view to show the data to be input and confirm its right:
                # return ConfirmCreateEntryView(request, df_for_input_dict)
                #
                # # This was used to input data here. Now being passed to another function:

                # Input each row of the above dictionary into the Risk Register model
                for row in df_for_input_dict:
                    # pass
                    # print("\nIn row to input into RRs:\n")

                    RiskRegister.objects.get_or_create(
                        firm_name=Firm.objects.get(firm_id=current_firm),

                        quality_objective_category=row['Quality objective category'],
                        quality_objective=row['Quality objective'],
                        quality_risk=row['Quality Risk'],
                        # quality_risk_firm_size=row['quality_risk_firm_size'],
                        risk_response=row['Responses to address the quality risks'],
                        owner=row['Owner'],
                        response_mandatory=row['Mandatory?'],
                        # risk_response_firm_size=row['risk_response_firm_size'],
                        response_type=row['Response type'],
                        risk_response_source='Risk library',
                        response_status=row['Response status'],
                        comments=row['Comments'],
                        frequency_of_review=row['Review frequency'],
                        created_by=request.user.first_name + " " + request.user.last_name,
                        # sign_off_owner=row['sign_off_owner'],
                        # sign_off_reviewer=row['sign_off_reviewer'],
                        entry_type=row['Entry type'],
                        rd_risk_response_id=row['risk_response_id'],
                    )
                    print("\nCreated Risk entry")
                print("\nDONE")
            else:
                print("firm does not exist")
        else:
            print("File not found")

        return HttpResponseRedirect(reverse('risk-register-2:view-risk-register'))

# ---------------------- 2.9 End of Import Risk Register ----------------------

# ---------------------- 2.10 Delete Risk Register ----------------------

@login_required()
def DeleteRiskRegister(request):

    print("In delete view")
    RiskRegister.objects.all().delete()

    return HttpResponseRedirect(reverse('risk-register-2:delete-risk-register-complete'))

class DeleteRegComplete(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_10_b_delete_reg_complete.html'
        return render(request, template_name=template_name, context=context)


# ---------------------- 2.9 End of Delete Risk Register ----------------------

# ---------------------- 3.5 Success View ----------------------

class SuccessView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_09_success.html'
        return render(request, template_name=template_name, context=context)


class ImportSuccessView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_12_b_import_success.html'
        return render(request, template_name=template_name, context=context)


# ---------------------- 3.5 End of Success View ----------------------


#
class UpdateRRSuccessView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_11_update_rr_success.html'
        return render(request, template_name=template_name, context=context)


class ErrorView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_14_error.html'
        return render(request, template_name=template_name, context=context)

class ImportErrorView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        template_name = 'riskreg/02_12_b_import_success.html'
        return render(request, template_name=template_name, context=context)


# .as_view(), name='success'),
#     path('error/', views.