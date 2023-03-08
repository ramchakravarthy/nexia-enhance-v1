from django.contrib import admin

from riskregister.models import (
    RiskRegister_01_QualityObjectiveCategory,
    RiskRegister_02_QualityObjective,
    RiskRegister_03_QualityRisk,
    RiskRegister_04_RiskResponse
)

from riskregister.models import RiskRegister, RCA

# Register your models here.

admin.site.register(RiskRegister_01_QualityObjectiveCategory)
admin.site.register(RiskRegister_02_QualityObjective)
admin.site.register(RiskRegister_03_QualityRisk)
admin.site.register(RiskRegister_04_RiskResponse)

admin.site.register(RiskRegister)
admin.site.register(RCA)