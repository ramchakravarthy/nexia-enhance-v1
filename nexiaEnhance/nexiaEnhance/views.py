from django.shortcuts import render

from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import get_user_model

from accounts.models import Firm, UserAttributes


# Create your views here.

def UserRightsContext(request):
    context = {}

    context['is_viewer'] = False
    context['is_preparer'] = False
    context['is_reviewer'] = False
    context['is_ult_authority'] = False
    context['is_user_manager'] = False
    context['is_nexia_superuser'] = False

    context['does_firm_exist'] = False
    context['current_firm'] = 0
    context['current_user'] = request.user
    context['current_firm_name'] = ""

    try:
        print("\nIn User Rights Context \n")

        context['is_viewer'], context['is_preparer'], context['is_reviewer'], context['is_ult_authority'], context[
            'is_user_manager'], context['is_nexia_superuser'] = \
        UserAttributes.objects.filter(user_id=request.user.id).values_list('is_viewer', 'is_preparer', 'is_reviewer',
                                                                           'is_ult_authority', 'is_user_manager',
                                                                           'is_nexia_superuser')[0]
        print("try succesful")
    except:
        current_user = str(request.user)
        # print("\nIn except, current user is: ", request.user, "\n")
        if current_user == 'nexiaenhancesuperuser':
            # print("user is superuser")
            context['is_nexia_superuser'] = True
            context['is_user_manager'] = True
        else:
            pass
            print("In else of nexiaenhancesuperuser")
    print("\nUser rights: NSU, UM: ", context['is_nexia_superuser'], context['is_user_manager'])
    print("\nCurrent user\n", request.user)

    if str(context['current_user']) == "nexiaenhancesuperuser":
        print("\nNESU\n")
        try:
            context['current_firm'] = \
            Firm.objects.filter(firm_name='Nexia International').values_list('firm_id', flat=True)[0]
        except:
            pass
    else:
        print("\nNot NESU\n")
        context['current_firm'] = Firm.objects.filter(userattributes__user=context['current_user']).values_list('firm_id', flat=True)[
            0]
        print("In Not Nesu, current firm is: ", context['current_firm'])
        context['current_firm_name'] = Firm.objects.filter(firm_id=context['current_firm']).values_list('firm_name', flat=True)[
            0]
        print("\nCurrent firm name: ", context['current_firm_name'])

    if context['current_firm'] != 0:
        print("Firm exists\n\n\n")
        context['does_firm_exist'] = True
    else:
        pass
    # print("\nContext: \n")
    # for key in context:
    #     print(key, ": ",context[key], "\n")
    return context

class ErrorView(TemplateView):
    template_name = '99_error.html'

class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    # template_name = '01_nexia_enhance_index.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        print("Current user: ", current_user.id)
        try:
            current_user_role = UserAttributes.objects.filter(user_id=request.user.id).values_list('user_role',flat=True)[0]
        except:
            current_user_role = "Superuser"
        else:
            pass

        print("Current user role: ",current_user_role)

        if current_user_role == 'IT_admin':
            return HttpResponseRedirect(reverse('user-administration'))
        else:
            # return HttpResponseRedirect()
            pass

        # firm_names = Firm.objects.values()
        # print("Firms: ", firm_names)
        #
        # user_attrs = UserAttributes.objects.values()
        # print("User attrs: ", user_attrs)
        #
        # current_user_firm_id = UserAttributes.objects.filter(user_id=current_user.id).values_list(('firm_name_id'),flat=True)[0]
        # print("Current user's firm id: ", current_user_firm_id)
        #
        # current_user_firm_name = Firm.objects.filter(firm_id=current_user_firm_id)[0]
        # print("Current user's firm name: ", current_user_firm_name)

        return render(request, '01_nexia_enhance_index.html', )

    # def get_context_data(self, **kwargs):
    #     context = super(HomePage, self).get_context_data(**kwargs)
    #
    #     user = get_user_model()
    #     print(user.objects.all)

    # return context

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse("test"))
    #     return super().get(request, *args, **kwargs)
