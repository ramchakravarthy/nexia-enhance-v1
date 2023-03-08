from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import SelectRelatedMixin

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404

from riskregister.models import (RiskRegister_01_QualityObjectiveCategory,
                                 RiskRegister_02_QualityObjective,
                                 RiskRegister_03_QualityRisk,
                                 RiskRegister_04_RiskResponse)

from riskregister.models import RiskRegister, RCA

from riskdatabase.models import (
    RiskDatabase_01_QualityObjectiveCategory,
    RiskDatabase_02_QualityObjective,
    RiskDatabase_03_QualityRisk,
    RiskDatabase_04_RiskResponse,
)

from collections import OrderedDict, defaultdict

from accounts.models import User, UserAttributes, Firm

import numpy as np
import pandas as pd

from django.contrib.auth import get_user_model

# Create your views here.


# ---------------------- 0.2. INSTRUCTIONS ----------------------

class RiskRegInstructions(TemplateView):
    template_name = 'riskregister/00_02_a_risk_register_instructions.html'


class RiskRegInstructionsRiskAssessment(TemplateView):
    template_name = 'riskregister/00_02_b_risk_assessment.html'














# Create Risk Database Entry:

# ---------------------- 2.1 Risk Library Entries ----------------------

class ModelMatrices:
    def create_risk_library_table(self, current_user):
        print("\nIn create risk lib table, current user is: ",current_user,"\n")

        # ------------------------------ Cat - Objective Matrix --------------------

        current_firm=0

        if str(current_user)=="nexiaenhancesuperuser":
            print("\nNESU\n")
        else:
            print("\nNot NESU\n")
            current_firm = Firm.objects.filter(userattributes__user=current_user).values_list('firm_id', flat=True)[0]
            print("In Not Nesu, current firm is: ", current_firm)

        if current_firm!=0:
            print("Firm exists")
        else:
            print("firm does not exist")

        df_rd_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())
        df_rr_in_rr = pd.DataFrame(RiskRegister_04_RiskResponse.objects.filter(firm_name_id=current_firm).values('rd_risk_response_id'))

        # List of risk responses in Risk Register:
        rrs = set(list(df_rr_in_rr['rd_risk_response_id']))
        # print("\nRd risk response id\n", rrs)

        # Function to return false if a risk response in the Risk Database is in the Risk register
        def rr_in_col(x):
            if x in rrs:
                return False
            else:
                return True

        df_rd_rr['rr_in_col'] = df_rd_rr['risk_response_id'].apply(lambda x: rr_in_col(x))

        # print("\nRR in col: ",df_rd_rr['rr_in_col'],"\n")

        df_rd_rr = df_rd_rr[df_rd_rr['rr_in_col']==True].drop(columns=['rr_in_col'])
        print(df_rd_rr)

        # df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        # df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
        # df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())

        # df_rd_in_rr = pd.merge(
        #     left=
        # )


        # df_risk_rr =
        #
        # df_obj_risk_rr =

        df_rd_in_rr_combined = pd.merge(
            left= pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values()),
            left_on='quality_objective_category_id',
            right=pd.merge(
                left=pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values()),
                left_on='quality_objective_id',
                right=pd.merge(
                    left=pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values()),
                    left_on='quality_risk_id',
                    right=df_rd_rr,
                    right_on='quality_risk_id',
                    how='inner',
                ),
                right_on='quality_objective_id',
                how='inner',
            ),
            right_on='quality_objective_category_id',
            how='inner'
        )

        print("\nDf rd in rr combined: \n", df_rd_in_rr_combined.to_dict('records')[0])


        # df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        # df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())

        df_cat = df_rd_in_rr_combined[['quality_objective_category_id','quality_objective_category']].drop_duplicates()
        df_obj = df_rd_in_rr_combined[['quality_objective_category_id', 'quality_objective', 'quality_objective_id', 'quality_objective_ref']].drop_duplicates()

        # print("\nDf cat \n", df_cat.columns.values)
        # print("\nDf obj \n", df_obj.columns.values)

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
                df_cat_obj['quality_objective_category'] == cat['quality_objective_category']
                ].to_dict('records', into=defaultdict(list))

            # print("\nCat obj dict is:", df_cat_obj_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_risk = []
            for obj in df_cat_obj_dict:
                temp_dict_risk = {}
                temp_dict_risk['objective'] = obj['quality_objective']
                temp_dict_risk['objective_id'] = "obj_"+str(obj['quality_objective_id'])
                temp_list_risk.append(temp_dict_risk)
                del temp_dict_risk
            temp_dict['objectives'] = temp_list_risk

            cat_obj_matrix.append(temp_dict)

            del temp_dict, df_cat_obj_dict

        # print("Cat obj matrix is: \n", cat_obj_matrix)
        # ------------------------------ END OF Cat - Objective Matrix --------------------

        # ------------------------------ Objective - Risk Matrix --------------------

        # print("\n OBJECTIVE RISK MATRIX \n")

        # df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
        # df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())

        df_obj = df_rd_in_rr_combined[['quality_objective_category_id', 'quality_objective', 'quality_objective_id',
                                       'quality_objective_ref']].drop_duplicates()

        df_risk = df_rd_in_rr_combined[[
            'quality_risk_id', 'quality_risk', 'quality_risk_ref', 'quality_risk_firm_size', 'quality_objective_id',
        ]].drop_duplicates()

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
            temp_dict['objective_id'] = "obj_"+str(obj['quality_objective_id'])

            df_obj_risk_dict = df_obj_risk[
                df_obj_risk['quality_objective'] == obj['quality_objective']].to_dict('records', into=defaultdict(list))
            # print("\nCat obj dict is:", df_obj_risk_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_risk = []
            for risk in df_obj_risk_dict:
                temp_dict_risk = {}
                temp_dict_risk['quality_risk'] = risk['quality_risk']
                temp_dict_risk['quality_risk_id'] = "risk_"+str(risk['quality_risk_id'])
                temp_list_risk.append(temp_dict_risk)
                del temp_dict_risk
            temp_dict['risks'] = temp_list_risk

            obj_risk_matrix.append(temp_dict)

            del temp_dict, df_obj_risk_dict

        # print(obj_risk_matrix)

        # -------------- END OF OBJ RISK MATRIX --------------------

        # ------------------------------ RISK - RISK RESPONSE Matrix --------------------

        # print("\n RISK - RISK RESPONSE MATRIX \n")

        # df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
        # df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())

        df_risk = df_rd_in_rr_combined[[
            'quality_risk_id', 'quality_risk', 'quality_risk_ref', 'quality_risk_firm_size', 'quality_objective_id',
        ]].drop_duplicates()
        df_rr = df_rd_in_rr_combined[[
            'risk_response_id', 'risk_response', 'risk_response_ref', 'response_mandatory', 'risk_response_firm_size', 'additional_mercia_guidance', 'quality_risk_id',
        ]].drop_duplicates()

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
            temp_dict['quality_risk_id'] = "risk_"+str(risk['quality_risk_id'])

            df_risk_rr_dict = df_risk_rr[
                df_risk_rr['quality_risk'] == risk['quality_risk']].to_dict('records', into=defaultdict(list))
            # print("\nCat obj dict is:", df_obj_risk_dict)
            # print("\n\n End of Dict \n\n")

            temp_list_rr = []
            for rr in df_risk_rr_dict:
                temp_dict_rr = {}
                temp_dict_rr['risk_response'] = rr['risk_response']
                temp_dict_rr['risk_response_id'] = "rr_"+str(rr['risk_response_id'])
                temp_list_rr.append(temp_dict_rr)
                del temp_dict_rr
            temp_dict['rr'] = temp_list_rr

            risk_rr_matrix.append(temp_dict)

            del temp_dict, df_risk_rr_dict

        return cat_obj_matrix, obj_risk_matrix, risk_rr_matrix

    def merge_risk_library_tables(self, df_to_merge, levels):
        # Obtain the values stored in the risk library models
        df_cat = pd.DataFrame(RiskDatabase_01_QualityObjectiveCategory.objects.values())
        df_obj = pd.DataFrame(RiskDatabase_02_QualityObjective.objects.values())
        df_risk = pd.DataFrame(RiskDatabase_03_QualityRisk.objects.values())
        df_rr = pd.DataFrame(RiskDatabase_04_RiskResponse.objects.values())

        # Starting from the risk response model, merge each model to the dataframe created from response.post
        df_for_input = pd.merge(
            left=df_rr,
            left_on='risk_response_id',
            right=df_to_merge,
            right_on='risk_response_id',
            how="inner",
        )
        if levels > 0:
            df_for_input = pd.merge(
                left=df_risk,
                left_on='quality_risk_id',
                right=df_for_input,
                right_on='quality_risk_id',
                how='inner'
            )
        else:
            pass
        if levels > 1:
            df_for_input = pd.merge(
                left=df_obj,
                left_on='quality_objective_id',
                right=df_for_input,
                right_on='quality_objective_id',
                how='inner'
            )
        else:
            pass
        if levels > 2:
            df_for_input = pd.merge(
                left=df_cat,
                left_on='quality_objective_category_id',
                right=df_for_input,
                right_on='quality_objective_category_id',
                how='inner'
            )
        else:
            pass
        return df_for_input


class CreateRiskLibraryEntryView(TemplateView, ModelMatrices):

    def __init__(self):
        super().__init__()

        # -------------- END OF RISK - RISK RESPONSE MATRIX --------------------

    def get(self, request, *args, **kwargs):
        context = {}

        context['is_nexia_superuser'] = False
        context['is_user_manager'] = False
        context['is_preparer'] = False
        context['is_reviewer'] = False
        context['is_ult_authority'] = False

        is_nexia_superuser = False
        is_user_manager = False

        try:
            print("In try")
            is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = \
            UserAttributes.objects.filter(
                user_id=request.user.id
            ).values_list('is_preparer', 'is_reviewer', 'is_ult_authority', 'is_user_manager', 'is_nexia_superuser')[0]
            context['is_preparer'] = is_preparer
            context['is_reviewer'] = is_reviewer
            context['is_ult_authority'] = is_ult_authority
            context['is_nexia_superuser'] = is_nexia_superuser
            context['is_user_manager'] = is_user_manager
            print("try succesful")
        except:

            current_user = str(request.user)
            # print("\nIn except, current user is: ", request.user, "\n")
            if current_user == 'nexiaenhancesuperuser':
                # print("user is superuser")
                is_nexia_superuser = True
                is_user_manager = True
                context['is_nexia_superuser'] = True
                context['is_user_manager'] = True
            else:
                # print("In else of nexiaenhancesuperuser")
                is_nexia_superuser = False
                is_user_manager = False

        print("\nUser rights: NSU, UM: ", context['is_nexia_superuser'], context['is_user_manager'])

        if context['is_preparer']==True or context['is_reviewer']==True or context['is_ult_authority']==True:
            print("to edit")
            context["cat_obj_matrix"], context["obj_risk_matrix"], context[
                "risk_rr_matrix"] = self.create_risk_library_table(request.user)
        else:
            print('not to edit')

        return render(request, template_name='riskregister/01_a_risk_library_entry.html', context=context)
        # return render(request, template_name ='riskregister/01_a_create_risk_database_entry.html', context=context)

    def post(self, request, *args, **kwargs):
        try:
            print("\nA form was posted\n")

            # print(request.POST)

            # print("Current user: ", request.user.id)
            # print("Current user: ", request.user)
            # print("Current user: ", request.user.first_name)

            # Obtain a list of risk response ids from "request.POST" that have been selected:
            rr_selection_list = [x.replace("_selection", "") for x in list(request.POST) if "_selection" in x]
            # ONLY FOR DEV:

            temp_list = []
            response_post_list = list(request.POST)
            # print("\nLength of Response post list is: ",len(response_post_list),"\n")
            for rr in rr_selection_list:
                print("\nrr is ", rr)
                temp_dict = {}
                i = 0
                while i < len(response_post_list):
                    key = response_post_list[i]
                    # print("Key is: ",key, " and Length of Response post list is: ",len(response_post_list))
                    if rr in key:
                        # print("key is: ",key)
                        # print('RR found: ',rr, ' Dict is empty? :', not bool(temp_dict))
                        if not bool(temp_dict):
                            # print("Dict is empty and adding id")
                            temp_dict['risk_response_id'] = rr
                        else:
                            # print("dict is NOT empty")
                            pass
                        temp_dict[key.replace(rr + "_", "")] = request.POST[key]
                        # print("Key to be removed is: ",key)
                        response_post_list.remove(key)
                        # print("Removed and Length of Response post list is: ", len(temp_response_post_list))
                        # print("temp req post list is: ",temp_response_post_list, "\n and other is: ",response_post_list)
                    else:
                        i = i + 1
                    del key
                # print("After first RR loop, temp rep.post list is: ", temp_response_post_list, "\n")

                if bool(temp_dict):
                    temp_list.append(temp_dict)
                else:
                    pass
                del temp_dict

            df_selection_values = pd.DataFrame(temp_list)
            del temp_list
            print("\n Dataframe selection: \n", df_selection_values)
            print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))


            def return_rr(x):
                return int(x.replace("rr_",""))

            df_selection_values['risk_response_id'] = df_selection_values['risk_response_id'].apply(lambda x:return_rr(x))

            print("\n Dataframe selection dict: \n", df_selection_values.to_dict('records'))

            df_for_input = self.merge_risk_library_tables(df_to_merge=df_selection_values, levels=3)

            # print("\n\n Updated RR selection Dataframe columns: \n", rr_df.columns.values)

            # Convert the dataframe into a dictionary for input into the Risk Register model
            df_for_input_dict = df_for_input.to_dict('records', into=defaultdict(list))
            print("\n Dict converstion done\n")

            print("\nDf for input: \n", df_for_input_dict)

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

                    # TODO: Consider deleting the old model creation:
                    # These were the old models and inputs to the old model

                    # RiskRegister_01_QualityObjectiveCategory.objects.get_or_create(
                    #     quality_objective_category=row['quality_objective_category'],
                    #     firm_name=Firm.objects.get(firm_id=current_firm)
                    # )
                    #
                    # print("\nCreated RR Cat")
                    #
                    # RiskRegister_02_QualityObjective.objects.get_or_create(
                    #     quality_objective=row['quality_objective'],
                    #     quality_objective_category=RiskRegister_01_QualityObjectiveCategory.objects.get(
                    #         quality_objective_category=row['quality_objective_category'])
                    # )
                    #
                    # print("\nCreated RR Obj")
                    #
                    # RiskRegister_03_QualityRisk.objects.get_or_create(
                    #     quality_risk=row['quality_risk'],
                    #     quality_risk_firm_size=row['quality_risk_firm_size'],
                    #     quality_objective=RiskRegister_02_QualityObjective.objects.get(
                    #         quality_objective=row['quality_objective'],
                    #     )
                    # )
                    #
                    # print("\nCreated RR Risk")
                    #
                    # qr = RiskRegister_03_QualityRisk.objects.get(quality_risk=row['quality_risk']),
                    # print("\nQr: ", qr, "\n")
                    #
                    # RiskRegister_04_RiskResponse.objects.get_or_create(
                    #     risk_response=row['risk_response'],
                    #     owner=row['owner'],
                    #     response_mandatory=row['response_mandatory'],
                    #     risk_response_firm_size=row['risk_response_firm_size'],
                    #     response_type=row['risk_response_type'],
                    #     risk_response_source='Risk library',
                    #     response_status=row['risk_response_status'],
                    #     comments=row['comments'],
                    #     frequency_of_review=row['review_frequency'],
                    #     created_by=request.user,
                    #     sign_off_owner=row['sign_off_owner'],
                    #     sign_off_reviewer=row['sign_off_reviewer'],
                    #     entry_type='rd_entry',
                    #     quality_risk=RiskRegister_03_QualityRisk.objects.get(quality_risk=row['quality_risk']),
                    #     rd_risk_response_id=row['risk_response_id'],
                    #     firm_name=Firm.objects.get(firm_id=current_firm),
                    # )
                    #
                    # print("\nCreated RR RR")

                print("\nDONE")

            else:
                print("firm does not exist")
                return HttpResponseRedirect(reverse("risk_register:error"))

            return HttpResponseRedirect(reverse("risk_register:success"))
        except:
            return HttpResponseRedirect(reverse("risk_register:error"))


# ---------------------- 2. View Risk Register ----------------------


class ViewRiskRegisterView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}

        context['is_nexia_superuser'] = False
        context['is_user_manager'] = False
        is_nexia_superuser = False
        is_user_manager = False

        try:
            print("In try")
            is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = \
                UserAttributes.objects.filter(
                    user_id=request.user.id
                ).values_list('is_preparer', 'is_reviewer', 'is_ult_authority', 'is_user_manager',
                              'is_nexia_superuser')[0]
            context['is_preparer'] = is_preparer
            context['is_reviewer'] = is_reviewer
            context['is_ult_authority'] = is_ult_authority
            context['is_nexia_superuser'] = is_nexia_superuser
            context['is_user_manager'] = is_user_manager
            print("try succesful")
        except:
            if request.user == "nexiaenhancesuperuser":
                is_nexia_superuser = True
                is_user_manager = True
                context['is_nexia_superuser'] = True
                context['is_user_manager'] = True
            else:
                is_nexia_superuser = False
                is_user_manager = False

        print("\nUser rights: NSU, UM\n", context['is_nexia_superuser'], context['is_user_manager'])



        print("\n In View Register: \n")

        # OLD CODES - TODO: DELETE

        # df_cat = pd.DataFrame(RiskRegister_01_QualityObjectiveCategory.objects.values())
        # print("\nDf cat:\n",df_cat)
        #
        # df_obj = pd.DataFrame(RiskRegister_02_QualityObjective.objects.values())
        # print("\nDf obj: \n",df_obj)
        # df_risk = pd.DataFrame(RiskRegister_03_QualityRisk.objects.values())
        # print("\nDf risk: \n", df_risk)
        # df_rr = pd.DataFrame(RiskRegister_04_RiskResponse.objects.values())
        # print("\nDf rr: \n", df_rr)
        #
        # df_c_o = pd.merge(
        #     left=df_cat,
        #     left_on='quality_objective_category_id',
        #     right=df_obj,
        #     right_on='quality_objective_category_id',
        #     how='inner'
        # )
        #
        # print("\nDf CO: \n", df_c_o.columns.values)
        #
        # df_c_o_r = pd.merge(
        #     left=df_c_o,
        #     left_on='quality_objective_id',
        #     right=df_risk,
        #     right_on='quality_objective_id',
        #     how='inner'
        # )
        #
        # print("\nDf COR: \n", df_c_o_r.columns.values)
        #
        # df_c_o_r_rr = pd.merge(
        #     left=df_c_o_r,
        #     left_on='quality_risk_id',
        #     right=df_rr,
        #     right_on='quality_risk_id',
        #     how='inner'
        # )
        #
        # print("\nDf CORRR: \n", df_c_o_r_rr.columns.values)

        df_risk_reg = pd.DataFrame(RiskRegister.objects.values())

        print("\nDf combined:\n", df_risk_reg)

        df_combined_dict = df_risk_reg.to_dict('records', into=defaultdict(list))

        # print("\ndf combined dict:\n", df_combined_dict)
        context['risklibrary'] = df_combined_dict

        print("\nDf combined columns:\n", df_risk_reg.columns.values)
        # print("\nDf cat_obj:\n", df_c_o)
        # print("\nDf cat_obj cols:\n", df_c_o.columns.values)

        # quality_objective_category_id

        return render(request, template_name = 'riskregister/02_view_risk_register.html', context=context)


# ---------------------- 2. end of View Risk Register ----------------------



# ---------------------- 9.a Success URL ----------------------

class SuccessView(TemplateView):
    template_name = 'riskregister/09_a_success.html'

    def get(self, request, *args, **kwargs):
        context = {}

        context['is_nexia_superuser'] = False
        context['is_user_manager'] = False
        is_nexia_superuser = False
        is_user_manager = False

        try:
            print("In try")
            is_preparer, is_reviewer, is_ult_authority, is_user_manager, is_nexia_superuser = \
            UserAttributes.objects.filter(
                user_id=request.user.id
            ).values_list('is_preparer', 'is_reviewer', 'is_ult_authority', 'is_user_manager', 'is_nexia_superuser')[0]
            context['is_preparer'] = is_preparer
            context['is_reviewer'] = is_reviewer
            context['is_ult_authority'] = is_ult_authority
            context['is_nexia_superuser'] = is_nexia_superuser
            context['is_user_manager'] = is_user_manager
            print("try succesful")
        except:
            if request.user == "nexiaenhancesuperuser":
                is_nexia_superuser = True
                is_user_manager = True
                context['is_nexia_superuser'] = True
                context['is_user_manager'] = True
            else:
                is_nexia_superuser = False
                is_user_manager = False

        print("\nUser rights: NSU, UM\n", context['is_nexia_superuser'], context['is_user_manager'])



        return render(request, "riskregister/09_a_success.html", context=context)

    # def get_context_data(self, request, **kwargs):
    #     context = super(SuccessView, self).get_context_data(**kwargs)
    #     context['rca_rr_id']=request.session.rca_rr_id
    #     return context


# ---------------------- END OF Success URL ----------------------

# ---------------------- 9.b Error URL ----------------------

class ErrorView(TemplateView):
    template_name = 'riskregister/09_b_error.html'


# ---------------------- End of Error URL ----------------------






class View1(TemplateView):
    template_name = 'riskregister/01.html'

    def post(self, request, *args, **kwargs):
        print("\nRequest.post:\n", request.POST)

        df = pd.DataFrame(np.array([1,2,3]), columns=['Col1'])
        print("\ndf\n", df)
        df_dict = df.to_dict('records', into=defaultdict(list))
        print("\ndf dict\n", df_dict)
        return View2(request, df_dict)

        # return HttpResponseRedirect(reverse('risk_register:success'))


def View2(request, df_dict):
    print("\nIn view 2\n")
    context={}
    context['df_dict'] = df_dict
    return render(request, template_name='riskregister/02.html', context=context)











# Create Category

class CreateCategoryView(CreateView):
    model = RiskRegister_01_QualityObjectiveCategory

# Create Objective

class CreateObjectiveView(CreateView):
    model = RiskRegister_02_QualityObjective


# View Categories List
class CategoryListView(LoginRequiredMixin, ListView):
    model=RiskRegister_01_QualityObjectiveCategory
    # template_name = 'riskregister/cat-list-view.html'
    # context_object_name = 'risk_register'

    def get(self, request, *args, **kwargs):
        context = {}

        current_user_id = request.user.id
        current_user_firm = Firm.objects.filter(userattributes__user_id=current_user_id)

        try:
            context['categories'] = RiskRegister_01_QualityObjectiveCategory.objects.filter(firm_name__userattributes__user_id=21)
        except:
            context['categories'] = []

        # print("Contex - rr: ",len(context['risk_register']))

        context['firm'] = current_user_firm
        return render(request, 'riskregister/OLD/cat-list-view.html', context)

class CategoryDetailedView(LoginRequiredMixin, DetailView):
    model = RiskRegister_01_QualityObjectiveCategory
    context_object_name = 'categories'
    template_name = 'riskregister/OLD/cat-detailed-view.html'

