# OLD VIEW REGISTER:
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

        df_cat = pd.DataFrame(RiskRegister_01_QualityObjectiveCategory.objects.values())
        print("\nDf cat:\n",df_cat)

        df_obj = pd.DataFrame(RiskRegister_02_QualityObjective.objects.values())
        print("\nDf obj: \n",df_obj)
        df_risk = pd.DataFrame(RiskRegister_03_QualityRisk.objects.values())
        print("\nDf risk: \n", df_risk)
        df_rr = pd.DataFrame(RiskRegister_04_RiskResponse.objects.values())
        print("\nDf rr: \n", df_rr)

        df_c_o = pd.merge(
            left=df_cat,
            left_on='quality_objective_category_id',
            right=df_obj,
            right_on='quality_objective_category_id',
            how='inner'
        )

        print("\nDf CO: \n", df_c_o.columns.values)

        df_c_o_r = pd.merge(
            left=df_c_o,
            left_on='quality_objective_id',
            right=df_risk,
            right_on='quality_objective_id',
            how='inner'
        )

        print("\nDf COR: \n", df_c_o_r.columns.values)

        df_c_o_r_rr = pd.merge(
            left=df_c_o_r,
            left_on='quality_risk_id',
            right=df_rr,
            right_on='quality_risk_id',
            how='inner'
        )

        print("\nDf CORRR: \n", df_c_o_r_rr.columns.values)

        df_combined_dict = df_c_o_r_rr.to_dict('records', into=defaultdict(list))

        # print("\ndf combined dict:\n", df_combined_dict)
        context['risklibrary'] = df_combined_dict

        print("\nDf combined columns:\n", df_c_o_r_rr.columns.values)
        # print("\nDf cat_obj:\n", df_c_o)
        # print("\nDf cat_obj cols:\n", df_c_o.columns.values)

        # quality_objective_category_id

        return render(request, template_name = 'riskregister/02_view_risk_register.html', context=context)


# ---------------------- 2. end of View Risk Register ----------------------

def ConfirmCreateEntryView(request, df_for_input_dict):


    # Columns to enter:
    #
    # {'quality_objective_category_id': 2, 'quality_objective_category': 'Relevant Ethical Requirements',
    #  'quality_objective_id': 8,
    #  'quality_objective': "Others, including the network, network firms, individuals in the network or network firms, or service providers, who are subject to the relevant ethical requirements to which the firm and the firm's engagements are subject:\ni) Understand the relevant ethical requirements that apply to them; and\nii) Fulfil their responsibilities in relation to the relevant ethical requirements that apply to them.",
    #  'quality_objective_ref': '1.29(b)', 'quality_risk_id': 25,
    #  'quality_risk': 'Network requirements, for example in respect of software utilised to record independence issues, does not comply with local regulatory requirements with the risk that the firm is not alerted when there is an independence breach.',
    #  'quality_risk_ref': 'nan', 'quality_risk_firm_size': 'Large', 'risk_response_id': 79,
    #  'risk_response': 'The firm operates a parallel system designed to ensure compliance with local regulatory and professional requirements.',
    #  'risk_response_ref': 'nan', 'response_mandatory': 'No', 'risk_response_firm_size': 'Large',
    #  'additional_mercia_guidance': 'nan', 'selection': 'on', 'owner': '', 'risk_response_type': '',
    #  'risk_response_status': '', 'comments': '', 'review_frequency': '', 'sign_off_owner': '', 'sign_off_reviewer': ''}

    context = {}

    context['df_for_input'] = df_for_input_dict
    request.method='GET'

    if request.method=="POST":
        print("RD entry form was posted\n")
        print("\nRequest.post is:\n", request.POST)
        return HttpResponseRedirect(reverse_lazy('risk_register:success'))
    else:
        print("not post")


    return render(request, template_name='riskregister/01_f_confirm_create_entry.html',context=context)