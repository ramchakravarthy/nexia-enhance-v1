from django.db import models
from django.urls import reverse

# Create your models here.

# Model 1: Quality Objective Category

class RiskDatabase_01_QualityObjectiveCategory(models.Model):
    quality_objective_category_id = models.AutoField(primary_key=True)
    quality_objective_category = models.CharField(max_length=150, unique=False)

    def __str__(self):
        return str(self.quality_objective_category)

    def get_absolute_url(self):
        return reverse("risk_database:view-risk-database")

    class Meta:
        ordering = ["quality_objective_category"]

# Model 2: Quality Objective and associated Quality Objective Category

class RiskDatabase_02_QualityObjective(models.Model):
    quality_objective_id = models.AutoField(primary_key=True)
    quality_objective = models.CharField(max_length=5000, unique=False)
    quality_objective_ref = models.CharField(max_length=120, unique=False)

    quality_objective_category = models.ForeignKey(RiskDatabase_01_QualityObjectiveCategory, related_name='objectives',
                                                   on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality_objective)

    def get_absolute_url(self):
        return reverse("risk_database:view-risk-database")

    class Meta:
        ordering = ["quality_objective_category", "quality_objective"]

# Model 3: Quality Risks and associated Quality Objective

class RiskDatabase_03_QualityRisk(models.Model):
    quality_risk_id = models.AutoField(primary_key=True)
    quality_risk = models.CharField(max_length=5000, unique=False)
    quality_risk_ref = models.CharField(max_length=150, unique=False)
    quality_risk_firm_size_choices = [
        ('Small', 'Small'),
        ('Large', 'Large'),
        ('All', 'All'),
    ]
    quality_risk_firm_size = models.CharField(max_length=256,unique=False,choices=quality_risk_firm_size_choices)

    quality_objective = models.ForeignKey(RiskDatabase_02_QualityObjective, related_name='risks', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quality_risk)

    def get_absolute_url(self):
        return reverse("risk_database:view-risk-database")

    class Meta:
        ordering = ["quality_objective", "quality_risk"]

# Model 4: Risk Responses and associated Risks

class RiskDatabase_04_RiskResponse(models.Model):
    risk_response_id = models.AutoField(primary_key=True)
    risk_response = models.CharField(max_length=10000, unique=False)
    risk_response_ref = models.CharField(max_length=150, unique=False)
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
    additional_mercia_guidance = models.CharField(max_length=150, unique=False)
    quality_risk = models.ForeignKey(RiskDatabase_03_QualityRisk, related_name='risk_response', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.risk_response)

    def get_absolute_url(self):
        return reverse("risk_database:view-risk-database")

    class Meta:
        ordering = ["quality_risk", "risk_response"]
