from django import forms
from annualdeclaration.models import OLD_AnnualDeclaration, AnnualDeclaration
import datetime

class AnnualDeclarationForm(forms.ModelForm):
    previous_evaluation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AnnualDeclaration
        fields = [
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
        ]


# class AnnualDeclarationForm(forms.ModelForm):
#
#     def get_today():
#         return datetime.datetime.now().date()
#
#     def get_tomorrow():
#         return (datetime.datetime.now() + datetime.timedelta(days=1)).date()
#
#     TODAY = get_today
#     TOMORROW = get_tomorrow
#     DATE_SELECTION = (
#         (TODAY, "Today"),
#         (TOMORROW, "Tomorrow"),
#     )
#
#     date_now = datetime.datetime.now()
#
#
#     prev_eval_dates_choices = [
#         (date_now, date_now.strftime('%d-%m-%Y'))
#     ]
#
#     print("In AD FORM")
#
#     print("Length of annual dec dates: ", len(AnnualDeclaration.objects.values('evaluation_date')), "\n")
#
#     if len(AnnualDeclaration.objects.values('evaluation_date')) > 0:
#         prev_eval_dates = list(set(AnnualDeclaration.objects.values('evaluation_date', flat=True)))
#         for date in prev_eval_dates:
#             prev_eval_dates_choices.append(
#                 (date, date.strftime('%d-%m-%Y'))
#             )
#     else:
#         pass
#
#     print("AD Form var: ", prev_eval_dates_choices)
#
#     previous_evaluation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     # input_formats=["%Y-%m-%d"])
#     # previous_evaluation_date = forms.DateField(input_formats=["%Y-%m-%d"],
#     #                                            widget=forms.Select(choices=prev_eval_dates_choices))
#
#     class Meta:
#         model = AnnualDeclaration
#         fields = [
#             'evaluation_year',
#             'evaluation_1',
#             'evaluation_2',
#             'evaluation_3',
#             'conclusion_1',
#             'conclusion_2',
#             'conclusion_3',
#             'actions_and_communications_1',
#             'actions_and_communications_1_b',
#             'actions_and_communications_2',
#             'actions_and_communications_3',
#             'individual',
#         ]
