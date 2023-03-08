from django import forms

class ImportRiskDatabaseForm(forms.Form):
    risk_database = forms.FileField(label_suffix="upload file", label="")