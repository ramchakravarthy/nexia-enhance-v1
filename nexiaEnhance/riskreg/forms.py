from django import forms
from riskreg.models import RiskRegister, RCA, QuillPost

from django_quill.forms import QuillFormField

class QuillModelForm(forms.ModelForm):
    class Meta:
        model = QuillPost
        fields = (
            'content',
            'text'
        )

class QuillFieldForm(forms.Form):
    text = forms.TextInput()
    content = QuillFormField()

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(label="Please select a file to import")

class RiskRegEntryForm(forms.ModelForm):
    class Meta:
        model = RiskRegister
        fields = (
            'quality_risk',
            'risk_response',
            'owner',
            'response_type',
            'response_status',
            'comments',
            'frequency_of_review',
            'created_by',
            'sign_off_owner',
            'sign_off_reviewer',
        )

class CustomRiskForm(forms.ModelForm):
    class Meta:
        model = RiskRegister
        fields = (
            'quality_objective_category',
            'quality_objective',
            'quality_risk',
            'risk_response',
            'owner',
            'response_type',
            'response_status',
            'comments',
            'frequency_of_review',
            'created_by',
            'sign_off_owner',
            'sign_off_reviewer',
        )

class CreateDeficiencyForm(forms.ModelForm):
    class Meta:
        model = RCA
        fields = (
            'identified_deficiency',
            'immediate_cause',
            'immediate_cause_reviewer_comments',
            'contributory_cause_1',
            'contributory_cause_1_reviewer_comments',
            'contributory_cause_2',
            'contributory_cause_2_reviewer_comments',
            'contributory_cause_3',
            'contributory_cause_3_reviewer_comments',
            'root_cause',
            'root_cause_reviewer_comments',
            'is_severe',
            'is_severe_comments',
            'is_pervasive',
            'is_pervasive_comments',
            'proposed_remedial_action',
            'proposed_remedial_action_reviewer_comments',
            # 'proposed_remedial_action_status_choices',
            'proposed_remedial_action_status',
            'remedial_action_conclusion',
            'remedial_action_change',
            'preparer_signature',
            # 'preparer_signature_date',
            'quality_management_head_signature',
            # 'quality_management_head_signature_date',
            'old_risk_response',
            'new_risk_response',
            'risk_response',
        )



