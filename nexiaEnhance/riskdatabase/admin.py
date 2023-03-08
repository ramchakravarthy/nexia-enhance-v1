from django.contrib import admin

from riskdatabase.models import RiskDatabase_01_QualityObjectiveCategory, RiskDatabase_02_QualityObjective, RiskDatabase_03_QualityRisk, RiskDatabase_04_RiskResponse

# Register your models here.

admin.site.register(RiskDatabase_01_QualityObjectiveCategory)
admin.site.register(RiskDatabase_02_QualityObjective)
admin.site.register(RiskDatabase_03_QualityRisk)
admin.site.register(RiskDatabase_04_RiskResponse)