from django.db import models
from django.urls import reverse
from accounts.models import Firm


# Create your models here.

# Model 1: Risk Register

class RiskRegister(models.Model):
    entry_id = models.AutoField(primary_key=True)
    firm_name = models.ForeignKey(Firm, related_name='risk_register_Entry', on_delete=models.CASCADE)

    quality_objective_category = models.CharField(max_length=150, unique=False)
    quality_objective = models.CharField(max_length=5000, unique=False)
    quality_risk = models.CharField(max_length=5000, unique=False)

    quality_risk_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    quality_risk_firm_size = models.CharField(max_length=256,unique=False,choices=quality_risk_firm_size_choices)

    risk_response = models.CharField(max_length=10000, unique=False)

    owner = models.CharField(max_length=256, unique=False, null=True, blank=True)
    response_mandatory_choices = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    response_mandatory = models.CharField(max_length=256, unique=False, choices=response_mandatory_choices)
    risk_response_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    risk_response_firm_size = models.CharField(max_length=256,unique=False,choices=risk_response_firm_size_choices)

    response_type_choices = [
        ('', ''),
        ('Off-the-shelf software', 'Off-the-shelf software'),
        ('In-house software', 'In-house software'),
        ('Certificates', 'Certificates'),
        ('Documented policy', 'Documented policy'),
        ('Documented procedure', 'Documented procedure'),
        ('Other', 'Other')
    ]
    response_type = models.CharField(max_length=256, unique=False, choices=response_type_choices, null=True, blank=True)

    risk_response_source_choices = [
        ('Risk library', 'Risk library'),
        ('Custom entry', 'Custom entry'),
        ('Custom objective, risks and response', 'Custom objective, risks and response'),
        ('Custom risks and response', 'Custom risks and response'),
        ('Custom response', 'Custom response'),
    ]
    risk_response_source = models.CharField(max_length=50, unique=False, choices=risk_response_source_choices,
                                            null=True, blank=True, default='risk_library')
    risk_response_status_choices = [
        ('', ''),
        ("In place", "In place"),
        ("in_progress", "In progress"),
        ("not_started", "Not started")
    ]
    response_status = models.CharField(max_length=150, unique=False, choices=risk_response_status_choices, null=True,
                                       blank=True)
    comments = models.TextField(unique=False, null=True, blank=True)
    review_frequency_choices = [
        ('', ''),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
    ]
    frequency_of_review = models.CharField(max_length=256, unique=False, choices=review_frequency_choices, null=True,
                                           blank=True)
    created_by = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_owner = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_reviewer = models.CharField(max_length=256, unique=False, null=True, blank=True)

    entry_type_choices = [
        ('rd_entry', 'rd_entry'),
        ('custom_rr', 'custom_rr'),
        ('custom_r_rr', 'custom_r_rr'),
        ('custom_o_r_rr', 'custom_o_r_rr'),
        ('custom_c_o_r_rr', 'custom_c_o_r_rr'),
    ]
    entry_type = models.CharField(max_length=256, unique=False, choices=entry_type_choices)

    rd_risk_response_id = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.firm_name) + " - " + str(self.risk_response))

    def get_absolute_url(self):
        return reverse("risk_register:view-risk-register")

    class Meta:
        unique_together = ['firm_name', 'quality_objective_category']

# Model 2: Root Cause Analysis:

class RCA(models.Model):
    identified_deficiency_id = models.AutoField(primary_key=True)
    identified_deficiency = models.TextField(unique=False, null=False, blank=False)

    immediate_cause = models.TextField(unique=False, null=False, blank=False)
    immediate_cause_reviewer_comments = models.TextField(unique=False, null=True, blank=True)

    contributory_cause_1 = models.TextField(unique=False, null=False, blank=False)
    contributory_cause_1_reviewer_comments = models.TextField(unique=False, null=True, blank=True)

    contributory_cause_2 = models.TextField(unique=False, null=True, blank=True)
    contributory_cause_2_reviewer_comments = models.TextField(unique=False, null=True, blank=True)

    contributory_cause_3 = models.TextField(unique=False, null=True, blank=True)
    contributory_cause_3_reviewer_comments = models.TextField(unique=False, null=True, blank=True)

    root_cause = models.TextField(unique=False, null=False, blank=False)
    root_cause_reviewer_comments = models.TextField(unique=False, null=False, blank=False)

    proposed_remedial_action = models.TextField(unique=False, null=False, blank=False)
    proposed_remedial_action_reviewer_comments = models.TextField(unique=False, null=True, blank=True)

    preparer_signature = models.CharField(max_length=1000)
    preparer_signature_date = models.DateField(auto_now=True)

    quality_management_head_signature = models.CharField(max_length=1000)
    quality_management_head_signature_date = models.DateField(auto_now=True)

    entry = models.ForeignKey(RiskRegister, related_name='root_cause_analysis',
                                        on_delete=models.CASCADE)
    firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.identified_deficiency)

    def get_absolute_url(self):
        return reverse("risk_register:view-risk-register")













# TODO: Consider deleting the following older models:
# OLD MODELS - Risk register broken down into cat, obj, risk and rr

# Model 1: Quality Objective Category

class RiskRegister_01_QualityObjectiveCategory(models.Model):
    quality_objective_category_id = models.AutoField(primary_key=True)
    quality_objective_category = models.CharField(max_length=150, unique=False)

    firm_name = models.ForeignKey(Firm, related_name='objective_categories', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.firm_name) + " - " + str(self.quality_objective_category)

    def get_absolute_url(self):
        return reverse("risk_register:risk-register-list")

    class Meta:
        unique_together = ['firm_name', 'quality_objective_category']


# Model 2: Quality Objective and associated Quality Objective Category

class RiskRegister_02_QualityObjective(models.Model):
    quality_objective_id = models.AutoField(primary_key=True)
    quality_objective = models.CharField(max_length=5000, unique=False)

    quality_objective_category = models.ForeignKey(RiskRegister_01_QualityObjectiveCategory, related_name='objectives',
                                                   on_delete=models.CASCADE)

    # firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality_objective)

    def get_absolute_url(self):
        return reverse("risk_register:risk-register-list")

    class Meta:
        unique_together = ['quality_objective_category', 'quality_objective']

# Model 3: Quality Risks and associated Quality Objective

class RiskRegister_03_QualityRisk(models.Model):
    quality_risk_id = models.AutoField(primary_key=True)
    quality_risk = models.CharField(max_length=5000, unique=False)
    quality_risk_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    quality_risk_firm_size = models.CharField(max_length=256,unique=False,choices=quality_risk_firm_size_choices)

    quality_objective = models.ForeignKey(RiskRegister_02_QualityObjective, related_name='risks', on_delete=models.CASCADE)
    # firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality_risk)

    def get_absolute_url(self):
        return reverse("risk_register:view-risk-register")

# Model 4: Risk Responses and associated Risks

class RiskRegister_04_RiskResponse(models.Model):
    risk_response_id = models.AutoField(primary_key=True)
    risk_response = models.CharField(max_length=10000, unique=False)

    owner = models.CharField(max_length=256, unique=False, null=True, blank=True)

    response_mandatory_choices = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    response_mandatory = models.CharField(max_length=256, unique=False, choices=response_mandatory_choices)
    risk_response_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    risk_response_firm_size = models.CharField(max_length=256,unique=False,choices=risk_response_firm_size_choices)

    response_type_choices = [
        ('', ''),
        ('Off-the-shelf software', 'Off-the-shelf software'),
        ('In-house software', 'In-house software'),
        ('Certificates', 'Certificates'),
        ('Documented policy', 'Documented policy'),
        ('Documented procedure', 'Documented procedure'),
        ('Other', 'Other')
    ]
    response_type = models.CharField(max_length=256, unique=False, choices=response_type_choices, null=True, blank=True)
    risk_response_source_choices = [
        ('Risk library', 'Risk library'),
        ('Custom entry', 'Custom entry'),
        ('Custom objective, risks and response', 'Custom objective, risks and response'),
        ('Custom risks and response', 'Custom risks and response'),
        ('Custom response', 'Custom response'),
    ]
    risk_response_source = models.CharField(max_length=50, unique=False, choices=risk_response_source_choices,
                                            null=True, blank=True, default='risk_library')
    risk_response_status_choices = [
        ('', ''),
        ("In place", "In place"),
        ("in_progress", "In progress"),
        ("not_started", "Not started")
    ]
    response_status = models.CharField(max_length=150, unique=False, choices=risk_response_status_choices, null=True,
                                       blank=True)
    comments = models.TextField(unique=False, null=True, blank=True)
    review_frequency_choices = [
        ('', ''),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
    ]
    frequency_of_review = models.CharField(max_length=256, unique=False, choices=review_frequency_choices, null=True,
                                           blank=True)
    created_by = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_owner = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_reviewer = models.CharField(max_length=256, unique=False, null=True, blank=True)

    entry_type_choices = [
        ('rd_entry', 'rd_entry'),
        ('custom_rr', 'custom_rr'),
        ('custom_r_rr', 'custom_r_rr'),
        ('custom_o_r_rr', 'custom_o_r_rr'),
        ('custom_c_o_r_rr', 'custom_c_o_r_rr'),
    ]
    entry_type = models.CharField(max_length=256, unique=False, choices=entry_type_choices)

    quality_risk = models.ForeignKey(RiskRegister_03_QualityRisk, related_name='risk_responses', on_delete=models.CASCADE)

    rd_risk_response_id = models.IntegerField(default=0)
    firm_name = models.ForeignKey(Firm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.risk_response)

    def get_absolute_url(self):
        return reverse("risk_register:view-risk-register")