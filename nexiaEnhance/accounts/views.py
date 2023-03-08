from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView
from accounts.models import Firm, User, UserAttributes

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django import forms


class ImportForm(forms.Form):
    file = forms.FileField(label_suffix="upload file", label="")

from accounts.forms import CreateUserForm, CreateUserAttributesForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from . import forms

from nexiaEnhance.views import UserRightsContext

from django import forms as d_forms

import pandas as pd
import numpy as np
from collections import OrderedDict, defaultdict

# ----------------------------------------------------------------------
# ------------------------------User Views------------------------------
# ----------------------------------------------------------------------

# 00. Admin homepage
class AdminView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/00_admin_homepage.html'

# 01. Create a user
class CreateUserView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/01_create_user.html'

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        # context['user_ref'] = self.kwargs['user_ref']

        print("")

        # TODO: Delete the following commented lines
        # current_user_role = UserAttributes.objects.filter(user_id=request.user.id).values_list('user_role',flat=True)[0]
        # print("\nUser role from attr model: ", current_user_role, "\n")

        # current_user_role = UserAttributes.objects.filter(user_id=request.user.id).values_list('is_user_manager','is_nexia_superuser')[0]
        # print("\nUser role from attr model: ", current_user_role, "\n")

        print(UserAttributes.objects.filter(user_id=request.user.id).values_list())

        is_nexia_superuser = False
        is_user_manager = False

        try:
            is_user_manager, is_nexia_superuser = UserAttributes.objects.filter(user_id=request.user.id).values_list('is_user_manager','is_nexia_superuser')[0]
            # print("try succesful")
        except:
            if request.user == "nexiaenhancesuperuser":
                is_nexia_superuser=True
                is_user_manager=True
            else:
                is_nexia_superuser = False
                is_user_manager = False
            # return HttpResponseRedirect(reverse('error'))


        # TODO: Delete the following commented lines
        # print("\nIs user manager: ", is_user_manager)
        # print("\nIs nexia super user: ", is_nexia_superuser)

        user_firm_name = Firm.objects.filter(userattributes__user_id=request.user.id)[0]
        print("user_firm name: ", user_firm_name)

        firms = list(Firm.objects.values_list('firm_name', flat=True))
        # print("\nFirms: ", firms)

        a = []
        a = [(x,x) for x in firms]

        # print("\nFirms tuple: ", a)

        if is_user_manager==True or is_nexia_superuser==True:
            print("\nThe user is a user manager/nexia super user.\n")

            class CreateUserAttributesForm(d_forms.Form):

                # For both user manager and nexia superuser, provide options to create preparer, reviewer, ult_auth and NE_admin
                user_role_choices = [
                    ('preparer', 'Preparer'),
                    ('reviewer', 'Reviewer'),
                    ('ult_resp_auth', 'Ultimate responsible authority'),
                    ('nexia_enhance_admin', 'Nexia Enhance administrator'),
                ]

                if is_nexia_superuser==True:
                    # print("\n in Nexia Superuser\n")

                    # if the user is  nexia superuser, provide options to select a firm
                    firms_list = Firm.objects.values_list('firm_name', flat=True)
                    firm_name = d_forms.ChoiceField(choices=[(x, x) for x in firms_list])

                    # if the user is a nexia superuser, provide options to create staff, reviewer, ult_auth, NE_admin, IT_admin, nexia_user and nexia_superuser
                    user_role_additional_choices = [
                        ('IT_admin', 'IT administrator'),
                        ('nexia_user', 'Nexia user'),
                        ('nexia_superuser', 'Nexia superuser')
                    ]

                    for i in range(len(user_role_additional_choices)):
                        user_role_choices.append(user_role_additional_choices[i])

                    # print("all choices: ", user_role_choices)
                    user_role = d_forms.ChoiceField(
                        choices=user_role_choices
                    )
                else:
                    print("\n in user manager\n")
                    # Firm name is the same as the user manager
                    firm_name = d_forms.CharField(
                        initial=Firm.objects.filter(userattributes__user_id=request.user.id)[0], disabled=True)
                    # if the user is  user manager, provide options to create preparer, reviewer, ult_auth and NE_admin
                    user_role = d_forms.ChoiceField(choices=user_role_choices)

                # for both users, upload profile picture
                profile_pic = d_forms.ImageField(required=False)

            context['user_form'] = CreateUserForm
            # context['user_2_form'] = CreateFirmITAdminUserAttributesForm
            context['user_attributes_form'] = CreateUserAttributesForm
            context['is_not_blank']=True

        else:
            # If the current user is not a user manager or a superuser, they should not be able to add a user.
            # Hence, create a form that is blank and display text that the user should not be in this view.
            class BlankForm(d_forms.Form):
                disabled_field = d_forms.CharField(initial="You are not authorised to add users. Please speak to your administrator.", disabled=True, label="")

            context['is_not_blank'] = False
            context['error_text'] = "You are not authorised to add users. Please speak to your administrator."

        # TODO: Delete the following commented lines
        # class CreateUserAttributesForm(d_forms.Form):
        #     firm_name = d_forms.ChoiceField(
        #         choices= [(x,x) for x in firms]
        #     )
        # context['user_attributes_form'] =CreateUserAttributesForm

        # CreateNexiaSuperUserAttributesForm



        # user_model = User.objects.filter(id=request.user.id).values()
        # print("\nUser from user model: ", user_model, "\n")

        # current_user = request.user
        # print("Current user: ", current_user.id)
        #
        # user_model_attrs = User.objects.filter(id=current_user.id).values_list('is_superuser', flat=True)[0]
        # print("User model attrs (is user a superuser): ", user_model_attrs)
        #
        # firm_names = Firm.objects.values()
        # print("Firms: ", firm_names)
        #
        # user_attrs = UserAttributes.objects.values()
        # print("User attrs: ", user_attrs)
        #
        # current_user_firm_id = \
        # UserAttributes.objects.filter(user_id=current_user.id).values_list(('firm_name_id'), flat=True)[0]
        # print("Current user's firm id: ", current_user_firm_id)
        #
        # current_user_firm_name = Firm.objects.filter(firm_id=current_user_firm_id)[0]
        # print("Current user's firm name: ", current_user_firm_name)

        return render(request, 'accounts/01_create_user.html', context)

    # TODO: Delete the following commented lines
    # def get_context_data(self, **kwargs):
    #     context = super(RegisterUser, self).get_context_data(**kwargs)
    #     context['user_ref'] = self.kwargs['user_ref']
    #     context['user_form'] = CreateUserForm
    #     context['user_attributes_form'] = CreateUserAttributesForm
    #     print("User ref: ", context['user_ref'])
    #
    #     return context

    def post(self, request, *args, **kwargs):
        # TODO: Delete the following commented lines
        # print("In post")
        # print("\nRequest posted: ", request.POST)
        # print("\nUser ref: ",request.POST['user_ref'])
        # print("\nRequest.files: ", request.FILES)

        user_role = request.POST['user_role']

        # Initialise rights for user. Initially, all rights should be assigned false and then changed based on the role
        # submitted in the form above

        is_viewer = False
        is_preparer = False
        is_reviewer = False
        is_ult_authority = False
        is_user_manager = False
        is_nexia_reviewer = False
        is_nexia_superuser = False

        # TODO: Delete the following commented lines
        # print('is_viewer : ', is_viewer, '\n')
        # print('is_preparer : ', is_preparer, '\n')
        # print('is_reviewer : ', is_reviewer, '\n')
        # print('is_ult_authority : ', is_ult_authority, '\n')
        # print('is_user_manager : ', is_user_manager, '\n')
        # print('is_nexia_reviewer : ', is_nexia_reviewer, '\n')
        # print('is_nexia_superuser : ', is_nexia_superuser, '\n')

        # Determine rights for user based on the role submitted in the form

        # Viewer and Preparer:
        if user_role!= 'IT_admin':
            is_viewer = True
            if user_role != 'nexia_user':
                is_preparer=True
            else:
                pass
        else:
            pass

        # reviewer
        if user_role in ['reviewer','ult_resp_auth','nexia_enhance_admin','nexia_superuser']:
            is_reviewer=True
        else:
            pass


        # ult auth

        if user_role in ['ult_resp_auth','nexia_enhance_admin','nexia_superuser']:
            is_ult_authority=True
        else:
            pass

        # user manager
        if user_role in ['nexia_enhance_admin','IT_admin','nexia_superuser']:
            is_user_manager=True
        else:
            pass

        # nexia reviewer and Nexia superuser:
        if user_role in ['nexia_superuser','nexia_user']:
            is_nexia_reviewer = True
            if user_role == 'nexia_superuser':
                is_nexia_superuser = True
            else:
                pass
        else:
            pass

        # TODO: Delete the following commented lines
        # print('is_viewer : ', is_viewer, '\n')
        # print('is_preparer : ', is_preparer, '\n')
        # print('is_reviewer : ', is_reviewer, '\n')
        # print('is_ult_authority : ', is_ult_authority, '\n')
        # print('is_user_manager : ', is_user_manager, '\n')
        # print('is_nexia_reviewer : ', is_nexia_reviewer, '\n')
        # print('is_nexia_superuser : ', is_nexia_superuser, '\n')

        # Initialise variables for user form
        user_form = CreateUserForm(data=request.POST)
        # print("\n\nUserform created")

        # Create a dictionary to store the data to be imported into the "Create User Attribute" form

        user_attribute_form_data = {}

        # Check the role of the current user creating the form
        is_current_user_manager, is_current_nexia_superuser = UserAttributes.objects.filter(user_id=request.user.id).values_list('is_user_manager','is_nexia_superuser')[0]

        if is_current_nexia_superuser == True:
            user_attribute_form_data['firm_name'] = \
            Firm.objects.filter(firm_name=request.POST['firm_name']).values_list('firm_id', flat=True)[0]
        elif is_current_user_manager == True:
            user_attribute_form_data['firm_name'] = Firm.objects.filter(userattributes__user_id=request.user.id).values_list('firm_id',flat=True)[0]
        else:
            return HttpResponse("Error: please try again later.")

        user_attribute_form_data['profile_pic'] = request.POST['profile_pic']

        # Save user rights in the dictionary
        user_attribute_form_data['is_viewer'] = is_viewer
        user_attribute_form_data['is_preparer'] = is_preparer
        user_attribute_form_data['is_reviewer'] = is_reviewer
        user_attribute_form_data['is_ult_authority'] = is_ult_authority
        user_attribute_form_data['is_user_manager'] = is_user_manager
        user_attribute_form_data['is_nexia_reviewer'] = is_nexia_reviewer
        user_attribute_form_data['is_nexia_superuser'] = is_nexia_superuser

        # save the user role from the form
        user_attribute_form_data['user_role'] = request.POST['user_role']

        print("\nUser attribute form data: \n", user_attribute_form_data)

        # Create a query dictionary to be imported into the "Create User Attribute" form as data
        user_attribute_form_data_query_dict = QueryDict('',mutable=True)
        user_attribute_form_data_query_dict.update(user_attribute_form_data)

        # print(user_attribute_form_data_query_dict)

        # Initialise variable for "Create User Attribute" form
        user_attributes_form = CreateUserAttributesForm(data=user_attribute_form_data_query_dict)

        # TODO: Delete the following commented lines
        # if int(request.POST['user_ref']) < 2:
        #     print("\nUser: Nexia User")
        # elif int(request.POST['user_ref']) == 2:
        #     print("\nUser: IT admin")
        # else:
        #     print("\nUser: Normal")
        #
        # # Initialise variables for user form and user attributes forms
        # user_form = CreateUserForm(data=request.POST)
        # print("\n\nUserform created")
        #
        # print("\n\nNexia International object: ",Firm.objects.filter(firm_name="Nexia International"))
        #
        # user_attributes_form_dict = {
        #     0: CreateNexiaSuperUserAttributesForm,
        #     1: CreateNexiaUserAttributesForm,
        #     2: CreateFirmITAdminUserAttributesForm,
        #     3: CreateUserAttributesForm,
        # }
        #
        #
        #
        # class CreateNEUserAttributesForm(d_forms.ModelForm):
        #     if int(request.POST['user_ref'])<2:
        #         print("\nUser: Nexia User")
        #     elif int(request.POST['user_ref'])==2:
        #         print("\nUser: IT admin")
        #     else:
        #         print("\nUser: Normal")
        #
        #
        #     firm_name = d_forms.CharField(initial=Firm.objects.get(firm_name="Nexia International"), disabled=True)
        #     user_role = d_forms.CharField(initial='nexia_superuser', disabled=True)
        #
        #     class Meta:
        #         model = UserAttributes
        #         fields = ['user_role', 'firm_name', 'profile_pic']
        #
        # user_attributes_form = CreateNEUserAttributesForm(data=request.POST)
        # # user_attributes_form = user_attributes_form_dict[int(request.POST['user_ref'])](data=request.POST)
        #
        #
        #

        # Check if the forms are valid
        if user_form.is_valid() and user_attributes_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Save the user model
            user.save()

            # save user attributes form to database
            user_attributes = user_attributes_form.save(commit=False)
            # print("Firm name: ", user_attributes.firm_name)

            user_attributes.user = user

            # print("Firm name: ",user_attributes.firm_name)

            # TODO: Need to have a validation check to ensure the domain from the email is the same as the firm domain

            # Check if user has provided a profile picture
            if 'profile_pic' in request.FILES:
                # print('found profile pic')
                # If yes, then grab it from the POST form reply
                user_attributes.profile_pic = request.FILES['profile_pic']
            else:
                # print('profile pic not found')
                pass

            # Save user attributes model
            user_attributes.save()

            print("User profile created successfully")

        else:
            print("ERRORS in Userform: ", user_form.errors)
            print("ERRORS in User attributes form: ", user_attributes_form.errors)

        return HttpResponseRedirect(reverse('accounts:view-users'))

# 01.b Import users:

class ImportUserView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        context['form'] = ImportForm
        template_name = 'accounts/01_a_create_or_edit_user_form.html'
        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        print("In post")

        print("In Risk library import Post view - a Form has been posted")

        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            print("File found")

            print(request.POST)
            print(request.FILES)

            try:
                df_firms = pd.read_excel(request.FILES['file'])
                print("\nFirms to upload:\n", df_firms)

                print(df_firms.columns.values)

                firms_dict = df_firms.to_dict('records', into=defaultdict(list))

                for firm in firms_dict:
                    try:

                        firm_name = firm['Firm name']
                        # This code takes care of a space at the end of each name
                        firm_obj = Firm.objects.get(
                            firm_name=firm_name[:len(firm['Firm name'])-1] if firm_name[len(firm_name)-1]==" " else firm['Firm name']
                        )
                        print("\nFirm exists and is : ", firm_obj)

                        firm_obj.firm_domain = firm['Firm domain']
                        firm_obj.save()

                    except:
                        print("\nFirm does not exist already: ", firm['firm_name'])
                        Firm.objects.create(
                            firm_name=firm['Firm name'],
                            firm_domain=firm['Firm domain'],
                            is_active=True,
                        )
                        print("\nFirm created successfully: ", firm['Firm name'],"\n")

            except:
                print("Import didnt work")
        else:
            print("File not found")

        return HttpResponseRedirect(reverse('accounts:view-firms'))



# 02. View users

class ViewUsersView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context=UserRightsContext(request)

        context['users']=False
        context['is_nexia_superuser']=False
        context['is_user_manager']=False

        is_nexia_superuser = False
        is_user_manager = False

        try:
            is_user_manager, is_nexia_superuser = \
            UserAttributes.objects.filter(user_id=request.user.id).values_list('is_user_manager', 'is_nexia_superuser')[
                0]
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

            # return HttpResponseRedirect(reverse('error'))

        # print("SU, UM: ",is_nexia_superuser, is_user_manager,"\n")
        #
        # print("Context is superuser: ", context['is_nexia_superuser'])
        # print("Context is user manager: ", context['is_user_manager'])

        if is_nexia_superuser==True:

            context['is_nexia_superuser'] = True
            context['is_user_manager'] = True

            df_users = pd.DataFrame(
                User.objects.values_list('first_name', 'last_name', 'username', 'email', 'id'),
                columns=['first_name', 'last_name', 'username', 'email', 'user_id'],
            )
            # print("Users df: \n", df_users)

            df_user_attrs = pd.DataFrame(
                UserAttributes.objects.values_list('id','user_id','firm_name_id','profile_pic','user_role'),
                columns=['user_attr_id','user-id','firm_name_id','profile_pic','user_role']
            )
            # print("\nUser attrs df: \n", df_user_attrs)

            df_firms = pd.DataFrame(
                Firm.objects.filter(is_active=True).values('firm_id','firm_name'),
                # columns=['Firm id','Firm name']
            )
            # print("\nFirms df: \n", df_firms)

            df_attr_users = pd.merge(
                left=df_users,
                left_on='user_id',
                right=df_user_attrs,
                right_on='user-id',
                how='inner',
            ).drop(columns='user-id')
            # print("\nView user attrs df: \n",df_attr_users)

            df_view_users = pd.merge(
                left=df_attr_users,
                left_on='firm_name_id',
                right=df_firms,
                right_on='firm_id',
                how='inner',
            ).drop(columns='firm_name_id')
            # print("\nView users df: \n", df_view_users)

            context['users']= df_view_users.to_dict('records', into=defaultdict(list))
        elif is_user_manager==True:

            context['is_nexia_superuser'] = False
            context['is_user_manager'] = True

            current_user_firm = Firm.objects.filter(userattributes__user_id=request.user.id).values_list('firm_id',flat=True)[0]

            # print("\nIn user manager:\n")

            df_users = pd.DataFrame(
                User.objects.filter(userattributes__firm_name__exact=current_user_firm).values_list('first_name', 'last_name', 'username', 'email', 'id'),
                columns=['first_name', 'last_name', 'username', 'email', 'user_id'],
            )


            # print("Users df: \n", df_users)

            df_user_attrs = pd.DataFrame(
                UserAttributes.objects.filter(firm_name_id=current_user_firm).values_list('id', 'user_id', 'firm_name_id', 'profile_pic', 'user_role'),
                columns=['user_attr_id', 'user-id', 'firm_name_id', 'profile_pic', 'user_role']
            )
            # print("\nUser attrs df: \n", df_user_attrs)

            df_firms = pd.DataFrame(
                Firm.objects.filter(is_active=True, firm_id=current_user_firm).values('firm_id', 'firm_name'),
                # columns=['Firm id','Firm name']
            )
            # print("\nFirms df: \n", df_firms)

            df_attr_users = pd.merge(
                left=df_users,
                left_on='user_id',
                right=df_user_attrs,
                right_on='user-id',
                how='inner',
            ).drop(columns='user-id')
            # print("\nView users df: \n", df_attr_users)

            df_view_users = pd.merge(
                left=df_attr_users,
                left_on='firm_name_id',
                right=df_firms,
                right_on='firm_id',
                how='inner',
            ).drop(columns=['firm_name_id','firm_name'])
            # print("\nView users df: \n", df_view_users)

            context['users'] = df_view_users.to_dict('records', into=defaultdict(list))
        else:
            context['user']=False
            context['is_nexia_superuser'] = False
            context['is_user_manager'] = False

        # print("Context users: ", context['users'])
        # print("Context is superuser: ",context['is_nexia_superuser'])
        # print("Context is user manager: ",context['is_user_manager'])

        return render(request,'accounts/02_view_users.html',context)



# 03. Edit user
class EditUserView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)

        context['is_not_blank'] = False
        context['error_text'] = "You are not authorised to add users. Please speak to your administrator."
        context['user_pk'] = self.kwargs['pk']


        # Add an if - if the primary key is wrong, then no need to go into any loops

        context['users'] = False
        context['is_nexia_superuser'] = False
        context['is_user_manager'] = False

        is_firms_match=False

        try:
            is_firms_match = Firm.objects.filter(
                userattributes__user_id=request.user.id
            ).values_list('firm_id', flat=True)[0] == Firm.objects.filter(
                userattributes__user_id=self.kwargs['pk']
            ).values_list('firm_id',flat=True)[0]
        except:
            print("Error in comparison of firms")

        print("Is firm same: ",is_firms_match)

        is_nexia_superuser = False
        is_user_manager = False

        try:
            is_user_manager, is_nexia_superuser = UserAttributes.objects.filter(
                user_id=request.user.id
            ).values_list('is_user_manager', 'is_nexia_superuser')[0]
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

            # return HttpResponseRedirect(reverse('error'))

        print("SU, UM: ", is_nexia_superuser, is_user_manager, "\n")

        print("Context superuser: ", context['is_nexia_superuser'])
        print("Context user manager: ", context['is_user_manager'])

        if is_user_manager==True:
            if is_nexia_superuser==True or is_firms_match==True:

                try:

                    print("Edit only firm")

                    print("User is NESuper or UserMgr")
                    user_id_to_edit = self.kwargs['pk']
                    df_user_list = pd.DataFrame(
                        User.objects.filter(id=user_id_to_edit).values('id', 'first_name', 'last_name', 'username',
                                                                       'email')
                    )
                    df_user_attr = pd.DataFrame(
                        UserAttributes.objects.filter(user_id=user_id_to_edit).values('id', 'user_id', 'user_role',
                                                                                      'firm_name_id')
                    ).rename(columns={"id": "user_attr_id"})
                    print('Firm name id: ', df_user_attr['firm_name_id'][0])
                    df_firm = pd.DataFrame(
                        Firm.objects.filter(firm_id=df_user_attr['firm_name_id'][0]).values('firm_id', 'firm_name')
                    )
                    df_user_and_attr = pd.merge(
                        left=df_user_list, left_on='id', right=df_user_attr, right_on='user_id', how='inner'
                    ).drop(columns=['id'])
                    df_user_to_edit = pd.merge(
                        left=df_user_and_attr, left_on='firm_name_id', right=df_firm, right_on='firm_id', how='inner'
                    ).drop(columns=['firm_name_id'])
                    print("\nUser: \n", df_user_list)
                    print("\nUser attr: \n", df_user_attr)
                    print("\nDf firm: \n", df_firm)
                    print("\nUser to edit: \n", df_user_to_edit)

                    df_user_to_edit_dict = df_user_to_edit.to_dict('records', into=defaultdict(list))[0]
                    print("\nDf users dict: \n", df_user_to_edit_dict)

                    print("\nThe user is a user manager/nexia super user.\n")

                    class EditUserForm(d_forms.Form):
                        first_name = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict['first_name'])
                        last_name = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict['last_name'])
                        username = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict['username'],
                                                      help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
                        email = d_forms.EmailField(max_length=255, initial=df_user_to_edit_dict['email'])

                    class EditUserAttrForm(d_forms.Form):

                        # For both user manager and nexia superuser, provide options to create preparer, reviewer, ult_auth and NE_admin
                        user_role_choices = [
                            ('preparer', 'Preparer'),
                            ('reviewer', 'Reviewer'),
                            ('ult_resp_auth', 'Ultimate responsible authority'),
                            ('nexia_enhance_admin', 'Nexia Enhance administrator'),
                        ]

                        if is_nexia_superuser == True:
                            # print("\n in Nexia Superuser\n")

                            # if the user is  nexia superuser, provide options to select a firm
                            firms_list = Firm.objects.values_list('firm_name', flat=True)
                            firm_name = d_forms.ChoiceField(choices=[(x, x) for x in firms_list],
                                                            initial=df_user_to_edit_dict['firm_name'])

                            # if the user is a nexia superuser, provide options to create staff, reviewer, ult_auth, NE_admin, IT_admin, nexia_user and nexia_superuser
                            user_role_additional_choices = [
                                ('IT_admin', 'IT administrator'),
                                ('nexia_user', 'Nexia user'),
                                ('nexia_superuser', 'Nexia superuser')
                            ]

                            for i in range(len(user_role_additional_choices)):
                                user_role_choices.append(user_role_additional_choices[i])

                            # print("all choices: ", user_role_choices)
                            # user_role = d_forms.ChoiceField(
                            #     choices=user_role_choices
                            # )
                        else:
                            print("\n in user manager\n")
                            # Firm name is the same as the user manager
                            firm_name = d_forms.CharField(
                                initial=df_user_to_edit_dict['firm_name'], disabled=True)
                            # if the user is  user manager, provide options to create preparer, reviewer, ult_auth and NE_admin

                        user_role = d_forms.ChoiceField(choices=user_role_choices,
                                                        initial=df_user_to_edit_dict['user_role'])

                        # for both users, upload profile picture
                        profile_pic = d_forms.ImageField(required=False)

                    context['user_form'] = EditUserForm
                    # context['user_2_form'] = CreateFirmITAdminUserAttributesForm
                    context['user_attributes_form'] = EditUserAttrForm
                    context['is_not_blank'] = True
                    print("Successfully created user and user attr forms to edit user.")
                    # Superceded by above:
                    # if is_nexia_superuser == True:
                    #     print("add attributes to edit all")
                    # else:
                    #     print("dont add additional attributes")

                except:
                    context['is_not_blank'] = False
                    context['error_text'] = "Sorry, there is an error with editing this user. Please visit this page later or contact your administrator."
                    print("Error in creating forms")

            else:
                print("Edit none")
        #
        # if is_nexia_superuser == True or is_user_manager == True:
        #     print("User is NESuper or UserMgr")
        #     user_id_to_edit = self.kwargs['pk']
        #     df_user_list = pd.DataFrame(
        #         User.objects.filter(id=user_id_to_edit).values('id', 'first_name', 'last_name', 'username',
        #                                                        'email')
        #     )
        #     df_user_attr = pd.DataFrame(
        #         UserAttributes.objects.filter(user_id=user_id_to_edit).values('id', 'user_id', 'user_role',
        #                                                                       'firm_name_id')
        #     ).rename(columns={"id": "user_attr_id"})
        #     print('Firm name id: ', df_user_attr['firm_name_id'][0])
        #     df_firm = pd.DataFrame(
        #         Firm.objects.filter(firm_id=df_user_attr['firm_name_id'][0]).values('firm_id', 'firm_name')
        #     )
        #     df_user_and_attr = pd.merge(
        #         left=df_user_list, left_on='id', right=df_user_attr, right_on='user_id', how='inner'
        #     ).drop(columns=['id'])
        #     df_user_to_edit = pd.merge(
        #         left=df_user_and_attr, left_on='firm_name_id', right=df_firm, right_on='firm_id', how='inner'
        #     ).drop(columns=['firm_name_id'])
        #     print("\nUser: \n", df_user_list)
        #     print("\nUser attr: \n", df_user_attr)
        #     print("\nDf firm: \n", df_firm)
        #     print("\nUser to edit: \n", df_user_to_edit)
        #
        #     df_user_to_edit_dict = df_user_to_edit.to_dict('records', into=defaultdict(list))
        #     print("\nDf users dict: \n", df_user_to_edit_dict)
        #
        #     print("\nThe user is a user manager/nexia super user.\n")
        #
        #     class EditUserForm(d_forms.Form):
        #         first_name = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict[0]['first_name'])
        #         last_name = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict[0]['last_name'])
        #         user_name = d_forms.CharField(max_length=255, initial=df_user_to_edit_dict[0]['username'],
        #                                       help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
        #         email = d_forms.EmailField(max_length=255, initial=df_user_to_edit_dict[0]['email'])
        #
        #     class EditUserAttrForm(d_forms.Form):
        #
        #         # For both user manager and nexia superuser, provide options to create preparer, reviewer, ult_auth and NE_admin
        #         user_role_choices = [
        #             ('preparer', 'Preparer'),
        #             ('reviewer', 'Reviewer'),
        #             ('ult_resp_auth', 'Ultimate responsible authority'),
        #             ('nexia_enhance_admin', 'Nexia Enhance administrator'),
        #         ]
        #
        #         if is_nexia_superuser == True:
        #             # print("\n in Nexia Superuser\n")
        #
        #             # if the user is  nexia superuser, provide options to select a firm
        #             firms_list = Firm.objects.values_list('firm_name', flat=True)
        #             firm_name = d_forms.ChoiceField(choices=[(x, x) for x in firms_list],
        #                                             initial=df_user_to_edit_dict[0]['firm_name'])
        #
        #             # if the user is a nexia superuser, provide options to create staff, reviewer, ult_auth, NE_admin, IT_admin, nexia_user and nexia_superuser
        #             user_role_additional_choices = [
        #                 ('IT_admin', 'IT administrator'),
        #                 ('nexia_user', 'Nexia user'),
        #                 ('nexia_superuser', 'Nexia superuser')
        #             ]
        #
        #             for i in range(len(user_role_additional_choices)):
        #                 user_role_choices.append(user_role_additional_choices[i])
        #
        #             # print("all choices: ", user_role_choices)
        #             # user_role = d_forms.ChoiceField(
        #             #     choices=user_role_choices
        #             # )
        #         else:
        #             print("\n in user manager\n")
        #             # Firm name is the same as the user manager
        #             firm_name = d_forms.CharField(
        #                 initial=df_user_to_edit_dict['firm_name'], disabled=True)
        #             # if the user is  user manager, provide options to create preparer, reviewer, ult_auth and NE_admin
        #
        #         user_role = d_forms.ChoiceField(choices=user_role_choices,
        #                                         initial=df_user_to_edit_dict[0]['user_role'])
        #
        #         # for both users, upload profile picture
        #         profile_pic = d_forms.ImageField(required=False)
        #
        #     context['user_form'] = EditUserForm
        #     # context['user_2_form'] = CreateFirmITAdminUserAttributesForm
        #     context['user_attributes_form'] = EditUserAttrForm
        #     context['is_not_blank'] = True
        #
        # else:
        #
        #     # If the current user is not a user manager or a superuser, they should not be able to add a user.
        #     # Hence, create a form that is blank and display text that the user should not be in this view.
        #     class BlankForm(d_forms.Form):
        #         disabled_field = d_forms.CharField(
        #             initial="You are not authorised to add users. Please speak to your administrator.",
        #             disabled=True,
        #             label="")
        #
        #     context['is_not_blank'] = False
        #     context['error_text'] = "You are not authorised to add users. Please speak to your administrator."
        #
        return render(request,'accounts/03_edit_user.html',context)

    def post(self, request, *args, **kwargs):
        # TODO: Delete the following commented lines
        # print("In post")
        # print("\nRequest posted: ", request.POST)
        # print("\nUser ref: ",request.POST['user_ref'])
        # print("\nRequest.files: ", request.FILES)

        print("In post of edit user")
        user_role = request.POST['user_role']
        print("\nUser role: ", user_role,"\n")

        # Initialise rights for user. Initially, all rights should be assigned false and then changed based on the role
        # submitted in the form above

        is_viewer = False
        is_preparer = False
        is_reviewer = False
        is_ult_authority = False
        is_user_manager = False
        is_nexia_reviewer = False
        is_nexia_superuser = False

        # TODO: Delete the following commented lines
        # print('is_viewer : ', is_viewer, '\n')
        # print('is_preparer : ', is_preparer, '\n')
        # print('is_reviewer : ', is_reviewer, '\n')
        # print('is_ult_authority : ', is_ult_authority, '\n')
        # print('is_user_manager : ', is_user_manager, '\n')
        # print('is_nexia_reviewer : ', is_nexia_reviewer, '\n')
        # print('is_nexia_superuser : ', is_nexia_superuser, '\n')

        # Determine rights for user based on the role submitted in the form

        # Viewer and Preparer:
        if user_role!= 'IT_admin':
            is_viewer = True
            if user_role != 'nexia_user':
                is_preparer=True
            else:
                pass
        else:
            pass

        # reviewer
        if user_role in ['reviewer','ult_resp_auth','nexia_enhance_admin','nexia_superuser']:
            is_reviewer=True
        else:
            pass

        # ult auth

        if user_role in ['ult_resp_auth','nexia_enhance_admin','nexia_superuser']:
            is_ult_authority=True
        else:
            pass

        # user manager
        if user_role in ['nexia_enhance_admin','IT_admin','nexia_superuser']:
            is_user_manager=True
        else:
            pass

        # nexia reviewer and Nexia superuser:
        if user_role in ['nexia_superuser','nexia_user']:
            is_nexia_reviewer = True
            if user_role == 'nexia_superuser':
                is_nexia_superuser = True
            else:
                pass
        else:
            pass

        # TODO: Delete the following commented lines
        # print('is_viewer : ', is_viewer, '\n')
        # print('is_preparer : ', is_preparer, '\n')
        # print('is_reviewer : ', is_reviewer, '\n')
        # print('is_ult_authority : ', is_ult_authority, '\n')
        # print('is_user_manager : ', is_user_manager, '\n')
        # print('is_nexia_reviewer : ', is_nexia_reviewer, '\n')
        # print('is_nexia_superuser : ', is_nexia_superuser, '\n')

        # Initialise variables for user form

        # print("\nRequest.POST: ", request.POST,"\n")


        try:
            print("\n\nIn Update User's Try section")

            current_user = request.POST['user_ref']


            User_to_update = User.objects.get(id=current_user)

            User_to_update.first_name = request.POST['first_name']
            User_to_update.last_name = request.POST['last_name']
            User_to_update.username = request.POST['username']
            User_to_update.email = request.POST['email']

            User_attrs_to_update = UserAttributes.objects.get(user_id=current_user)

            User_attrs_to_update.firm_name = Firm.objects.get(
                firm_name=request.POST['firm_name']
            )
            User_attrs_to_update.user_role = request.POST['user_role']
            User_attrs_to_update.is_viewer = is_viewer
            User_attrs_to_update.is_preparer = is_preparer
            User_attrs_to_update.is_reviewer = is_reviewer
            User_attrs_to_update.is_ult_authority = is_ult_authority
            User_attrs_to_update.is_user_manager = is_user_manager
            User_attrs_to_update.is_nexia_reviewer = is_nexia_reviewer
            User_attrs_to_update.is_nexia_superuser = is_nexia_superuser

            User_to_update.save()
            # print("\nUser values updated")

            User_attrs_to_update.save()

            # print("\nUser attrs values updated")

            # print("\n\nUser updated values",User.objects.filter(id=current_user).values())
            # print("\n\nUser attrs updated values",UserAttributes.objects.filter(user_id=current_user).values())
            #
            # print("\n\nUpdated values successfully!")

            return HttpResponseRedirect(reverse('accounts:view-users'))

        except:
            return HttpResponse("Error in updating user. Contact your administrator.")
            # print("\n\nIn Update User's Try's Except section")

        # return HttpResponseRedirect(reverse('accounts:view-users'))

# 04. Delete user
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/04_delete_user.html'
    success_url = reverse_lazy('accounts:view-users')



print("")
# TODO: Delete markup
# class SignUp(CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy("accounts:login")
#     template_name = "accounts/signup.html"
print("")

# ----------------------------------------------------------------------
# ------------------------------Firms Views-----------------------------
# ----------------------------------------------------------------------

# View Firms
class FirmsListView(LoginRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):

        # get the current user's role
        # if the user is a nexia superuser, then
        #   get a list of firms and display
        #   else not authorised

        context = UserRightsContext(request)
        context['is_nexia_superuser'] = False
        context['is_user_manager'] = False
        context['firm_list'] = ""
        is_nexia_superuser = False
        is_user_manager = False

        try:
            is_user_manager, is_nexia_superuser = UserAttributes.objects.filter(
                user_id=request.user.id
            ).values_list('is_user_manager', 'is_nexia_superuser')[0]
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

        if is_nexia_superuser == True:
            context['firm_list'] = Firm.objects.all()
        else:
            context['firm_list'] = ""

        # print(context)
        return render(request, 'accounts/06_view_firms.html', context)

# Create Firm
class CreateFirmView(LoginRequiredMixin, CreateView):
    template_name = 'accounts/05_create_firm.html'
    model = Firm
    fields = ('firm_name', 'firm_domain')
    success_url = reverse_lazy('accounts:view-firms')

# Firm - Bulk upload

class ImportFirmView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        context = UserRightsContext(request)
        context['form'] = ImportForm
        template_name = 'accounts/05_b_import_firms.html'
        return render(request, template_name=template_name, context=context)

    def post(self, request, *args, **kwargs):
        print("In post")

        print("In Risk library import Post view - a Form has been posted")

        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            print("File found")

            print(request.POST)
            print(request.FILES)

            try:
                df_firms = pd.read_excel(request.FILES['file'])
                print("\nFirms to upload:\n", df_firms)

                print(df_firms.columns.values)

                firms_dict = df_firms.to_dict('records', into=defaultdict(list))

                for firm in firms_dict:
                    try:

                        firm_name = firm['Firm name']
                        # This code takes care of a space at the end of each name
                        firm_obj = Firm.objects.get(
                            firm_name=firm_name[:len(firm['Firm name'])-1] if firm_name[len(firm_name)-1]==" " else firm['Firm name']
                        )
                        print("\nFirm exists and is : ", firm_obj)

                        firm_obj.firm_domain = firm['Firm domain']
                        firm_obj.save()

                    except:
                        print("\nFirm does not exist already: ", firm['firm_name'])
                        Firm.objects.create(
                            firm_name=firm['Firm name'],
                            firm_domain=firm['Firm domain'],
                            is_active=True,
                        )
                        print("\nFirm created successfully: ", firm['Firm name'],"\n")

            except:
                print("Import didnt work")
        else:
            print("File not found")

        return HttpResponseRedirect(reverse('accounts:view-firms'))


# Edit Firm
class EditFirm(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/05_create_firm.html'
    model = Firm
    fields = ['firm_name','firm_domain']
    success_url = reverse_lazy('accounts:view-firms')

# Delete Firm
class DeleteFirm(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/07_firm_confirm_delete.html'
    model = Firm
    success_url = reverse_lazy('accounts:view-firms')

# TODO: Consider deleting?
class FirmsDetailedView(LoginRequiredMixin, DetailView):
    context_object_name = 'firm_detail'
    model = Firm
    template_name = 'accounts/firm_detail.html'

# class SignUp2(CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy("login")
#     template_name = "accounts/create_nexia_enhance_user.html"
