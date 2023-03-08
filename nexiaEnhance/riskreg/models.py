from django.db import models
from django.urls import reverse
from accounts.models import Firm
from django_quill.fields import QuillField

from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Quill model

class NonQuillPost(models.Model):
    content = QuillField()
    text = models.TextField(max_length=5000, unique=False, null=True, blank=True)

class QuillPost(models.Model):
    content = QuillField()
    text = models.TextField(max_length=5000, unique=False, null=True, blank=True)

# Table 1: Complete Risk Register

class RiskRegister(models.Model):
    # entry_id = models.AutoField(primary_key=True)
    firm_name = models.ForeignKey(Firm, related_name='risk_register_2_entry', on_delete=models.CASCADE)

    quality_objective_category = models.CharField(max_length=500, unique=False)
    quality_objective = models.TextField(max_length=5000, unique=False)
    quality_risk = models.TextField(max_length=10000, unique=False)

    quality_risk_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    quality_risk_firm_size = models.CharField(max_length=256, unique=False, choices=quality_risk_firm_size_choices)

    risk_response = models.TextField(max_length=100000, unique=False)

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
    risk_response_firm_size = models.CharField(max_length=256, unique=False, choices=risk_response_firm_size_choices)

    response_type_choices = [
        ('',''),
        ('Off-the-shelf software', 'Off-the-shelf software'),
        ('In-house software', 'In house software'),
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
    risk_response_source = models.CharField(max_length=50,unique=False, choices=risk_response_source_choices, null=True, blank=True, default='risk_library')

    risk_response_status_choices = [
        ('', ''),
        ("In place", "In place"),
        ("in_progress", "In progress"),
        ("not_started", "Not started")
    ]
    response_status = models.CharField(max_length=150, unique=False, choices=risk_response_status_choices, null=True, blank=True)

    comments = models.TextField(max_length=10000, unique=False, null=True, blank=True)
    review_frequency_choices = [
        ('', ''),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
    ]
    frequency_of_review = models.CharField(max_length=256, unique=False, choices=review_frequency_choices, null=True, blank=True)

    created_by = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_owner = models.CharField(max_length=256, unique=False, null=True, blank=True)
    sign_off_reviewer = models.CharField(max_length=256, unique=False, null=True, blank=True)

    entry_type_choices = [
        ('rd_entry', 'Risk library entry'),
        ('custom_rr', 'Custom risk response'),
        ('custom_r_rr', 'Custom risk, risk response'),
        ('custom_o_r_rr', 'Custom objective, risk and risk response'),
        ('custom_c_o_r_rr', 'Custom entry'),
    ]
    entry_type = models.CharField(max_length=256, unique=False, choices=entry_type_choices)

    rd_risk_response_id = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.firm_name) + " - " + str(self.risk_response))

    def get_absolute_url(self):
        return reverse("risk-register-2:view-risk-register")

    # class Meta:
    #     unique_together = ['firm_name', 'quality_objective_category']


# Model 2: Root Cause Analysis:

class RCA(models.Model):
    identified_deficiency_id = models.AutoField(primary_key=True)
    identified_deficiency = QuillField("Identified deficiency", unique=False, null=False, blank=False)
    # identified_deficiency = models.TextField(unique=False, null=False, blank=False)

    immediate_cause = QuillField("Immediate cause", unique=False, null=False, blank=False)
    # immediate_cause = models.TextField("Immediate cause", unique=False, null=False, blank=False)
    immediate_cause_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    contributory_cause_1 = QuillField("First contributory cause", unique=False, null=False, blank=False)
    # contributory_cause_1 = models.TextField(unique=False, null=False, blank=False)
    contributory_cause_1_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    contributory_cause_2 = QuillField("Second contributory cause",unique=False, null=True, blank=True)
    contributory_cause_2_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    contributory_cause_3 = QuillField("Third contributory cause",unique=False, null=True, blank=True)
    contributory_cause_3_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    root_cause = QuillField("Root cause", unique=False, null=False, blank=False)
    root_cause_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    is_severe = models.BooleanField("Is the deficiency severe?", default=False)
    is_severe_comments = QuillField("Comments", unique=False, null=False, blank=False)

    is_pervasive = models.BooleanField("Is the deficiency pervasive?", default=False)
    is_pervasive_comments = QuillField("Comments",unique=False, null=False, blank=False)

    proposed_remedial_action = QuillField("Proposed remedial action", unique=False, null=False, blank=False)
    proposed_remedial_action_reviewer_comments = QuillField("Reviewer comments", unique=False, null=True, blank=True)

    proposed_remedial_action_status_choices = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In progress'),
        ('implemented', 'Implemented'),
    ]
    proposed_remedial_action_status = models.CharField(max_length=256, unique=False, choices=proposed_remedial_action_status_choices)

    remedial_action_conclusion = QuillField("Remedial action conclusion", unique=False, null=False, blank=False)
    remedial_action_change = QuillField("What has changed as a result of the remedial action?", unique=False, null=False, blank=False)

    preparer_signature = models.CharField(max_length=1000)
    preparer_signature_date = models.DateField(auto_now=True)

    quality_management_head_signature = models.CharField(max_length=1000)
    quality_management_head_signature_date = models.DateField(auto_now=True)

    old_risk_response = models.TextField(unique=False, null=False, blank=False)
    new_risk_response = models.TextField(unique=False, null=False, blank=False)

    risk_response = models.ForeignKey(RiskRegister, related_name='root_cause_analysis',
                                        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.identified_deficiency)

    def get_absolute_url(self):
        return reverse("risk_register:view-risk-register")