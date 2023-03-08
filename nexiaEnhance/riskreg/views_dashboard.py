# import requests
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms as f
from riskreg.forms import RiskRegEntryForm, CustomRiskForm, CreateDeficiencyForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from nexiaEnhance.views import UserRightsContext

# Apps files:

from accounts.models import Firm

from nexiaEnhance.views import UserRightsContext

from riskdatabase.models import (
    RiskDatabase_01_QualityObjectiveCategory,
    RiskDatabase_02_QualityObjective,
    RiskDatabase_03_QualityRisk,
    RiskDatabase_04_RiskResponse,
)

from riskreg.models import RiskRegister, RCA


from copy import deepcopy

import pandas as pd
import numpy as np
from collections import OrderedDict, defaultdict

from json import dumps
import os, io
import xlsxwriter


# Create your views here.

# ---------------------- 0. DASHBOARDS ----------------------

# ---------------------- 0.0 HELPER FUNCTIONS ----------------------

class CreateRiskLibraryTable:
    def create_risk_library_table(self):
        # Convert the four models into dataframes.
        # Merge the four dataframes one by one from left to right.
        # Then convert the final dataframe into a dict and return it so it can be rendered.

        df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())

        # print("Df_cat: ",df_cat.columns.values)
        # print("Df_obj: ", df_obj.columns.values)

        df_cat_obj = pd.merge(
            left=df_cat,
            right=df_obj,
            left_on="quality_objective_category_id",
            right_on="quality_objective_category_id",
            how="inner"
        )
        del df_cat, df_obj

        # print("Df_cat_obj: ",df_cat_obj.columns.values)

        # df_cat_obj = df_cat_obj.drop(columns=["id_x", "quality_objective_category_id"])
        # df_cat_obj = df_cat_obj.rename(columns={"id_y": "id"})

        # print("\n", df_cat_obj)

        df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())

        # print("Df_risk: ", df_risk.columns.values)

        df_cat_obj_risk = pd.merge(
            left=df_cat_obj,
            right=df_risk,
            left_on="quality_objective_id",
            right_on="quality_objective_id",
            how="inner"
        )
        del df_cat_obj, df_risk

        # print("\nDf cat obj risk: \n", df_cat_obj_risk)
        # df_cat_obj_risk = df_cat_obj_risk.drop(columns=["id_x", "quality_objective_id"])
        # df_cat_obj_risk = df_cat_obj_risk.rename(columns={"id_y": "id"})

        # print("\n", df_cat_obj_risk)

        df_risk_response = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())

        df_risk_register = pd.merge(
            left=df_cat_obj_risk,
            right=df_risk_response,
            left_on="quality_risk_id",
            right_on="quality_risk_id",
            how="inner"
        )
        del df_cat_obj_risk, df_risk_response

        # print("Complete risk library\n", df_risk_register)
        # df_risk_register = df_risk_register.drop(columns=["id_x", "quality_risk_id"])
        # df_risk_register = df_risk_register.rename(columns={"id_y": "id"})

        # print("\n", df_risk_register,"\n")

        # df_risk_register_dict = df_risk_register.to_dict('records', into=defaultdict(list))
        # del df_risk_register
        #
        # print("Dictionary: \n",df_risk_register_dict)

        # return df_risk_register_dict
        return df_risk_register

# ---------------------- 0.1 RISK REGISTER HOME (KPIS) ----------------------

class RiskRegHomeView(LoginRequiredMixin, TemplateView, CreateRiskLibraryTable):

    def __init__(self):
        super().__init__()

    def response_evaluated(self, rr_status, owner, reviewer):
        if rr_status == "In place" and owner != "" and reviewer != "":
            return 1
        else:
            return 0

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        print("\nContext at start: ", context)
        template_name = 'riskreg/00_01_a_risk_reg_home_kpis.html'
        print("In Risk Reg Home")

        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr)==0:
            context['is_risk_reg_empty']=True
        else:
            print(df_rr.head(3).T)

            # df_rr['response_evaluated'] = df_rr[['response_status','sign_off_owner','sign_off_reviewer']].map(self.response_evaluated())

            df_rr['response_evaluated'] = df_rr.apply(lambda x: self.response_evaluated(x.response_status, x.sign_off_owner, x.sign_off_reviewer), axis=1)

            # print(df_rr.head(3).T)
            # print("To create risk library table")

            df_rl = self.create_risk_library_table()
            # df_rl = pd.DataFrame()
            # print("\n Risk library table: \n")
            # print(df_rl)

            chart_data_dict = {}
            numbers_data_dict = {}

            # GRAPHS:

            # a.	Completion KPIs:

            # i.	% of risks evaluated

            no_of_mandatory_risks_in_rr = 0
            try:
                rrs_evaluated = df_rr['response_evaluated'].sum()
                # no_of_mandatory_risks_in_rr = pd.pivot_table(df_rr, values='id', index='response_mandatory',
                #                                                     aggfunc=len).loc['Yes', 'id']
            except:
                pass

            evaluated_percentage = rrs_evaluated/len(df_rr)*100
            chart_data_dict["a_1"] = {
                "chart_id": "a_1",
                "chart_type": "doughnut",
                "data": list([int(evaluated_percentage), 100 - int(evaluated_percentage)]),
                "labels": ["Responses fully evaluated",
                           "Responses NOT fully evaluated"],
                "colours": ["#00B9B9", "#CA1C66"],
                "data_label": "evaluated_risks_%",
                "rotation_angle": 270,
                "circumference": 180,
                "index_axis": 'x',
            }

            # ii.	% of deficiencies remediated

            deficiencies_remediated = 0
            try:
                df_def_status = pd.DataFrame(RCA.objects.filter(risk_response__firm_name_id=context['current_firm']).values('proposed_remedial_action_status'))
                print("\nDeficiencies: \n", df_def_status.head(1).T)

                df_def_status['proposed_remedial_action_status'] = df_def_status['proposed_remedial_action_status'].apply(
                    lambda x: 1 if x == "implemented" else 0)

                # print("\nDeficiencies: \n", df_def_status.head(1).T)
                #
                # print("\nDeficiencies remediated: \n", df_def_status['proposed_remedial_action_status'].sum())
                # print("\nof total : \n", len(df_def_status))

                deficiencies_remediated = df_def_status['proposed_remedial_action_status'].sum()/len(df_def_status)*100
                del df_def_status
            except:
                pass

            chart_data_dict["a_2"] = {
                "chart_id": "a_2",
                "chart_type": "doughnut",
                "data": list([int(deficiencies_remediated), 100 - int(deficiencies_remediated)]),
                "labels": ["Deficiencies fully remediated",
                           "Deficiencies NOT fully remediated"],
                "colours": ["#00B9B9", "#CA1C66"],
                # rgba(251, 185, 17, 0.4)
                "data_label": "mandatory_risks_%",
                "rotation_angle": 270,
                "circumference": 180,
                "index_axis": 'x',
            }

            # iii.	% of mandatory risks included in risk reg

            no_of_mandatory_risks_in_rr = 0
            no_of_mandatory_risks_in_rl = pd.pivot_table(df_rl, values='quality_objective_category_id',
                                                                    index='response_mandatory',
                                                                    aggfunc=len).loc['Yes', 'quality_objective_category_id']

            print("\n\nNumber of mandatory risks in rl: ", no_of_mandatory_risks_in_rl)

            try:
                no_of_mandatory_risks_in_rr = pd.pivot_table(df_rr, values='id', index='response_mandatory',
                                                             aggfunc=len).loc['Yes', 'id']

                print("\n\nNumber of mandatory risks in rr: ", no_of_mandatory_risks_in_rr)

            except:
                pass

            mandatory_risks_in_risk_reg_percentage = no_of_mandatory_risks_in_rr * 100 / no_of_mandatory_risks_in_rl

            #
            # print(
            #     "\nPercentage of mandatory risks in risk register: ", mandatory_risks_in_risk_reg_percentage, "\n"
            # )
            #
            # print(list([mandatory_risks_in_risk_reg_percentage, 100 - mandatory_risks_in_risk_reg_percentage]))

            # mandatory_risks_in_risk_reg_percentage = 20

            chart_data_dict["a_3"] = {
                "chart_id": "a_3",
                "chart_type": "doughnut",
                "data": list(
                    [int(mandatory_risks_in_risk_reg_percentage), 100 - int(mandatory_risks_in_risk_reg_percentage)]),
                "labels": ["Mandatory responses included in risk register",
                           "Mandatory responses NOT included in risk register"],
                "colours": ["#00B9B9", "#CA1C66"],
                "data_label": "mandatory_risks_%",
                "rotation_angle": 270,
                "circumference": 180,
                "index_axis": 'x',
            }

            # iv.	% of risks signed off

            def is_blank(x):
                try:
                    if len(x) < 2:
                        return 0
                    else:
                        return 1
                except:
                    return 0

            sign_off_percent = 0

            try:
                df_rr_copy = deepcopy(df_rr)
                df_rr_copy['sign_off_reviewer_tag'] = df_rr_copy['sign_off_reviewer'].apply(lambda x: is_blank(x))
                #
                # print("\nIsnul: ", df_rr_copy['sign_off_reviewer_tag'].isnull().sum(),"\n length of df_rr: ",len(df_rr_copy))
                #
                # print("\n sign offs: \n", df_rr_copy['sign_off_reviewer_tag'])

                sign_off_percent = int((df_rr_copy['sign_off_reviewer_tag'].sum() / len(df_rr_copy)) * 100)
                del df_rr_copy
            except:
                pass
            chart_data_dict["a_4"] = {
                "chart_id": "a_4",
                "chart_type": "doughnut",
                "data": list([sign_off_percent, 100 - sign_off_percent]),
                "labels": ["% risk responses signed off",
                           "% risk responses NOT signed off"],
                "colours": ["#00B9B9", "#CA1C66"],
                # rgba(251, 185, 17, 0.4)
                "data_label": "mandatory_risks_%",
                "rotation_angle": 270,
                "circumference": 180,
                "index_axis": 'x',
            }

            # b.	Overview numbers (these will be numbers and not charts):

            # i.	Number of Categories in risk reg
            # print(len(df_rr['quality_objective_category'].unique()))
            numbers_data_dict['b_1'] = len(df_rr['quality_objective_category'].unique())

            # ii.	Obj
            # print(len(df_rr['quality_objective_category'].unique()))
            numbers_data_dict['b_2'] = len(df_rr['quality_objective'].unique())

            # iii.	Risks
            # print(len(df_rr['quality_objective_category'].unique()))
            numbers_data_dict['b_3'] = len(df_rr['quality_risk'].unique())

            # iv.	RRs
            # print(len(df_rr['quality_objective_category'].unique()))
            numbers_data_dict['b_4'] = len(df_rr['risk_response'].unique())

            context['chart_data'] = dumps(chart_data_dict)
            context['numbers_data'] = numbers_data_dict
            # return context

        return render(request, template_name=template_name, context=context)


# ---------------------- 0.1 END OF RISK REGISTER HOME (KPIS) ----------------------


# ---------------------- 0.2 RISK PROFILE ----------------------
class RiskRegHomeViewRiskProfile(LoginRequiredMixin, TemplateView, CreateRiskLibraryTable):


    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):

        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        print("\nContext at start: ", context)
        template_name = 'riskreg/riskreghomecomponents/01_risks_profile.html'
        print("In Risk Reg Home")

        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr) == 0:
            context['is_risk_reg_empty'] = True
        else:


            print(df_rr.head(1).T)

            print("To create risk library table")

            df_rl = self.create_risk_library_table()
            print("\n Risk library table: \n")
            print(df_rl)

            chart_data_dict = {}
            numbers_data_dict = {}

            # GRAPHS:

            # c.	Risks profile:
            # i.	Risks by owner

            print("\nNull in df rr: \n", df_rr.isnull().sum())

            def blank_entry_check(x):
                try:
                    temp = pd.DataFrame(list(x), columns=['col_1'])['col_1'].unique()
                except:
                    temp = ""
                if len(temp) < 1:
                    temp_1 = 'Blank'
                elif (len(temp) == 1 and temp[0] == ' '):
                    temp_1 = 'Blank'
                elif len(temp) > 1:
                    temp_1 = x
                return temp_1

            df_rr_owner = deepcopy(df_rr)
            df_rr_owner['owner'] = df_rr_owner['owner'].apply(lambda x: blank_entry_check(x))
            # print("Df risk profile after getting data: \n", df_rr_owner.T)

            rr_owner_pivot = pd.pivot_table(df_rr_owner, values='risk_response', index='owner',
                                            aggfunc=len)
            # print("rr_owner_pivot: \n", rr_owner_pivot)

            chart_data_dict["c_1"] = {
                "chart_id": "c_1",
                "chart_type": "bar",
                "data": list(rr_owner_pivot['risk_response']),
                "labels": list(rr_owner_pivot.index),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                # "colours": ["#0d5257", "#00b2a9", "#2b52a0", "#ca0e63", "#841262", "#1584c2"],

                "data_label": "Owner",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # ii.	Risks by category

            rr_cat_pivot = pd.pivot_table(df_rr, values='risk_response', index='quality_objective_category',
                                          aggfunc=len)

            print("RR Cat Pivot: \n", rr_cat_pivot)

            chart_data_dict["c_2"] = {
                "chart_id": "c_2",
                "chart_type": "bar",
                "data": list(rr_cat_pivot['risk_response']),
                "labels": list(rr_cat_pivot.index),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Quality risk category",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # iii.	Risks per objective – histogram

            rr_obj_risk_count = pd.pivot_table(df_rr, values='quality_risk', index='quality_objective',
                                               aggfunc=len)
            # print("RR Obj-Risk Pivot: \n", rr_obj_risk_count)
            # print(list(rr_obj_risk_count['quality_risk']))
            count, division = np.histogram(list(rr_obj_risk_count['quality_risk']))
            # print("\nCount: ",count,"\nSeries: ",division,"\n")

            chart_data_dict["c_3"] = {
                "chart_id": "c_3",
                "chart_type": "bar",
                "data": count.tolist(),
                "labels": division.tolist(),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Number of quality risks",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # iv.	Number of responses per risk - histogram

            rr_rr_risk_count = pd.pivot_table(df_rr, values='risk_response', index='quality_risk',
                                              aggfunc=len)
            print("RR Obj-Risk Pivot: \n", rr_rr_risk_count)
            print(list(rr_rr_risk_count['risk_response']))
            count, division = np.histogram(list(rr_rr_risk_count['risk_response']))
            # print("\nCount: ",count,"\nSeries: ",division,"\n")

            chart_data_dict["c_4"] = {
                "chart_id": "c_4",
                "chart_type": "bar",
                "data": count.tolist(),
                "labels": division.tolist(),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Number of risk responses",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # print("\n Chart Data Dict: ", chart_data_dict, "\n")

            context['chart_data'] = dumps(chart_data_dict)
            context['numbers_data'] = numbers_data_dict
        return render(request, template_name=template_name,context=context)


# ---------------------- 0.2 END OF RISK PROFILE ----------------------

# ---------------------- 0.3 RISK RESPONSE PROFILE ----------------------
class RiskRegHomeViewRiskResponseProfile(LoginRequiredMixin, TemplateView, CreateRiskLibraryTable):


    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):

        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        print("\nContext at start: ", context)
        template_name = 'riskreg/riskreghomecomponents/02_risk_responses_profile.html'
        print("In Risk Reg Home")

        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr) == 0:
            context['is_risk_reg_empty'] = True
        else:

            print("In Risk Reg Home Risk Response Profile")
            df_rr = pd.DataFrame()
            try:
                df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
            except:
                pass
            # print(df_rr.head(1).T)

            print("To create risk library table")

            df_rl = self.create_risk_library_table()
            print("\n Risk library table: \n")
            # print(df_rl)

            chart_data_dict = {}
            numbers_data_dict = {}

            # GRAPHS:

            # d.	Risk response profile:

            def blank_entry_check(x):
                try:
                    temp = pd.DataFrame(list(x), columns=['col_1'])['col_1'].unique()
                except:
                    temp = ""
                if len(temp) < 1:
                    temp_1 = 'Blank'
                elif (len(temp) == 1 and temp[0] == ' '):
                    temp_1 = 'Blank'
                elif len(temp) > 1:
                    temp_1 = x
                return temp_1

            # i.	Number of rr in each response type

            # df_rr_rt = deepcopy(df_rr)
            # df_rr_rt['response_type'] = df_rr_rt['response_type'].apply(lambda x: blank_entry_check(x))
            # # print("Df risk profile after getting data: \n", df_rr_owner.T)
            #
            # rr_owner_pivot = pd.pivot_table(df_rr_rt, values='response_type', index='risk_response',
            #                                 aggfunc=len)

            rr_rt_pivot = pd.pivot_table(df_rr, values='risk_response', index='response_type',
                                         aggfunc=len)

            # print("RR Cat Pivot: \n", rr_rt_pivot)

            # print("\nRR table:\n",df_rr)

            print("\nRisk responses in RR: \n", df_rr['risk_response'], "\nRisk response types in RR: \n",
                  df_rr['response_type'])

            # todo: have all risk response types and display 0 if not present. do same for status and frequency below

            chart_data_dict["d_1"] = {
                "chart_id": "d_1",
                "chart_type": "bar",
                "data": list(rr_rt_pivot['risk_response']),
                "labels": list(rr_rt_pivot.index),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Response type",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # ii.	number of rr in each status type

            rr_status_type_pivot = pd.pivot_table(df_rr, values='risk_response', index='response_status',
                                                  aggfunc=len)

            # print("RR Status Pivot: \n", rr_status_type_pivot)
            #
            # print("Length of rr status pivot: ",len(rr_status_type_pivot))

            if len(rr_status_type_pivot) < 1:
                data = list([len(df_rr)])
                label = list(["none"])
            else:
                data = list(rr_status_type_pivot['risk_response'])
                label = list(rr_status_type_pivot.index)

            chart_data_dict["d_2"] = {
                "chart_id": "d_2",
                "chart_type": "bar",
                "data": data,
                "labels": label,
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Response status",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # iii.	number of rr in each review freq type

            rr_review_freq_pivot = pd.pivot_table(df_rr, values='risk_response', index='frequency_of_review',
                                                  aggfunc=len)

            # print("RR Review Freq Pivot: \n", rr_review_freq_pivot)
            # print("\n\nRR review freq: \n",df_rr['frequency_of_review'])
            #
            # print("Length of rr status pivot: ",len(rr_status_type_pivot))

            if len(rr_review_freq_pivot) < 1:
                data = list([len(df_rr)])
                label = list(["none"])
            else:
                data = list(rr_review_freq_pivot['risk_response'])
                label = list(rr_review_freq_pivot.index)

            chart_data_dict["d_3"] = {
                "chart_id": "d_3",
                "chart_type": "bar",
                "data": data,
                "labels": label,
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Response frequency",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            # iv.	number of rr with comments

            df_rr_comments = deepcopy(df_rr)

            def comments_tag(x):
                try:
                    if len(x) < 2:
                        return 0
                    else:
                        return 1
                except:
                    return 0

            df_rr_comments['comments_type'] = df_rr_comments['comments'].apply(lambda x: comments_tag(x))
            # df_rr_comments['comments_type'] = df_rr_comments['comments'].apply(lambda x: 0 if len(x)<2 else 1)

            print("\nDf -comments type:\n", df_rr_comments['comments_type'])

            print(pd.pivot_table(df_rr_comments, index='comments_type', values='risk_response', aggfunc=len))

            print("\nRR with comments: ", df_rr_comments['comments_type'].sum(), "\n")

            # def comments_blank(x):
            #     if len()

            with_comments = int(df_rr_comments['comments_type'].sum())
            without_comments = len(df_rr) - with_comments
            print("\n Type: ", type(with_comments))

            chart_data_dict["d_4"] = {
                "chart_id": "d_4",
                "chart_type": "bar",
                "data": list([with_comments, without_comments]),
                "labels": list(['With comments', 'Missing comments']),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Number of responses",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'x',
            }

            context['chart_data'] = dumps(chart_data_dict)
            context['numbers_data'] = numbers_data_dict
        return render(request, template_name=template_name,context=context)


# ---------------------- 0.3 END OF RISK RESPONSE PROFILE ----------------------

# ---------------------- 0.4 DATA QUALITY SUMMARY ----------------------
class RiskRegHomeViewDataQualityProfile(LoginRequiredMixin, TemplateView, CreateRiskLibraryTable):


    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):

        context = UserRightsContext(request)
        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        print("\nContext at start: ", context)
        template_name = 'riskreg/riskreghomecomponents/03_data_quality_summary.html'
        print("In Risk Reg Home")

        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr) == 0:
            context['is_risk_reg_empty'] = True
        else:

            print("In Risk Reg Home Data Quality Summary")

            df_rr = pd.DataFrame()
            try:
                df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
            except:
                pass
            # print(df_rr.head(1).T)

            # print("To create risk library table")

            df_rl = self.create_risk_library_table()
            # print("\n Risk library table: \n")
            # print(df_rl)

            chart_data_dict = {}
            numbers_data_dict = {}

            # GRAPHS:

            def blank_entry_check(x):
                try:
                    temp = pd.DataFrame(list(x), columns=['col_1'])['col_1'].unique()
                except:
                    temp = ""
                if len(temp) < 1:
                    temp_1 = 'Blank'
                elif (len(temp) == 1 and temp[0] == ' '):
                    temp_1 = 'Blank'
                elif len(temp) > 1:
                    temp_1 = x
                return temp_1

            # e.	Data Quality:

            # i.	Missing values – all columns

            df_missing = pd.DataFrame(df_rr.isnull().sum(), columns=['Columns'])

            # print("Index: ", list(df_missing.index))

            df_missing_index = list(df_missing.index)

            if 'id' in df_missing_index:
                # print("True")
                df_missing_index.remove('id')
                # print("Popped list: ", df_missing_index)

            else:
                pass
                # print("no id")

            # print("\nMissing index: ",df_missing_index,"\n")
            #
            # print(df_missing.loc[df_missing_index])
            # # print(df_missing)

            df_missing = df_missing.loc[df_missing_index]

            chart_data_dict["e_1"] = {
                "chart_id": "e_1",
                "chart_type": "bar",
                "data": list(df_missing['Columns']),
                "labels": list(df_missing.index),
                "colours": ["#00323C", "#00B9B9", "#1985C3", "#2E53A1", "#841262", "#CA1C66", "#ED9034", "#FBC311",
                            "#000000"],
                "data_label": "Number of entries",
                "rotation_angle": 0,
                "circumference": 360,
                "index_axis": 'y',
            }

            # ii.	Duplicates

            # # Concept
            # df_1 = pd.DataFrame(data=[1,2,2,2,2,2,4,3,3,3,3,3],columns=['Cols'])
            # df_1['Cols2'] = ['a','a','a','a','a','a','a','a','a','a','a','a']
            # print("Df: \n",df_1,"\n")
            # rrs = df_1["Cols"]
            # df_1[rrs.isin(rrs[rrs.duplicated()])].sort_values("Cols")
            # print("\nDuplicates:\n", df_1[rrs.isin(rrs[rrs.duplicated()])].sort_values("Cols"))

            rrs = df_rr["risk_response"]
            # print(rrs.duplicated())
            df_rr_duplicated = df_rr[rrs.isin(rrs[rrs.duplicated()])].sort_values("risk_response")
            # print("\nDuplicates:\n", df_rr[rrs.isin(rrs[rrs.duplicated()])].sort_values("risk_response"))

            print("EOD")

            context['chart_data'] = dumps(chart_data_dict)
            context['numbers_data'] = numbers_data_dict
            context['table_data'] = {} if len(df_rr_duplicated) == 0 else df_rr_duplicated.to_dict('records',
                                                                                                   into=defaultdict(list))

            print("\nContext table data: \n", context['table_data'])
        return render(request, template_name=template_name,context=context)


# ---------------------- 0.4 END OF DATA QUALITY SUMMARY ----------------------

# ---------------------- 0.5 DEFICIENCY ACTION PLAN VIEW ----------------------
class RiskRegHomeViewDeficiencyActionPlanView(LoginRequiredMixin, TemplateView, CreateRiskLibraryTable):


    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        context['is_risk_reg_empty'] = False
        print("\nContext at start: ", context)
        template_name = 'riskreg/riskreghomecomponents/04_deficiency_action_plan_view.html'
        print("In Risk Reg Home")

        df_rr = pd.DataFrame()
        try:
            df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
        except:
            pass

        if len(df_rr) == 0:
            context['is_risk_reg_empty'] = True
        else:
            print("In Risk Reg Home Data Quality Summary")

            df_rr = pd.DataFrame()
            try:
                df_rr = pd.DataFrame(RiskRegister.objects.filter(firm_name_id=context['current_firm']).values())
            except:
                pass
            # print(df_rr.head(1).T)

            df_rca = pd.DataFrame()
            try:
                df_rca = pd.DataFrame(RCA.objects.filter(risk_response__firm_name_id=context['current_firm']).values(
                    'old_risk_response',
                    'identified_deficiency',
                    'proposed_remedial_action',
                    'proposed_remedial_action_status',
                    'remedial_action_change',
                    'new_risk_response',
                    'remedial_action_conclusion',
                ))
            except:
                pass

            rca_dict_list = []
            if len(df_rca) > 0 and len(df_rr) > 0:
                for rca in RCA.objects.filter(risk_response__firm_name_id=context['current_firm']):
                    rca_dict = {}

                    print("\nRisk response of rca is: ", rca.risk_response_id)
                    # rca_dict['quality_objective_category'], rca_dict['quality_objective'], rca_dict['quality_risk'], \
                    # rca_dict['risk_response'] = \
                    #     RiskRegister.objects.filter(id=rca.risk_response_id).values_list('quality_objective_category',
                    #                                                                      'quality_objective',
                    #                                                                      'quality_risk',
                    #                                                                      'risk_response')[0]
                    rca_dict['old_risk_response'] = rca.old_risk_response
                    rca_dict['identified_deficiency'] = rca.identified_deficiency.html

                    rca_dict['root_cause'] = rca.root_cause.html
                    rca_dict['proposed_remedial_action'] = rca.proposed_remedial_action.html
                    rca_dict['proposed_remedial_action_status'] = "Not started" if \
                        rca.proposed_remedial_action_status == "not_started" else \
                        "In progress" if rca.proposed_remedial_action_status == "in_progress" else "implemented"


                    rca_dict['remedial_action_change'] = rca.remedial_action_change.html
                    rca_dict['new_risk_response'] = rca.new_risk_response
                    rca_dict['remedial_action_conclusion'] = rca.remedial_action_conclusion.html

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
                context['table_data'] = rca_dict_list
                context['is_deficiency_exists'] = True
                print("To print def.s")
            else:
                context['deficiencies_dict'] = {}

            #
            #
            # print("\nRCA table:\n",df_rca.head())

            print("EOD")

            # context['chart_data'] = dumps(chart_data_dict)
            # context['numbers_data'] = numbers_data_dict
            # context['table_data'] = {} if len(df_rca) == 0 else df_rca.to_dict('records', into=defaultdict(list))


            print("\nContext table data: \n", context['table_data'])
        return render(request, template_name=template_name,context=context)


# ---------------------- 0.5 END OF DEFICIENCY ACTION PLAN VIEW ----------------------
