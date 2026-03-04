from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *

class RankChoiceWidget(forms.Select):
  def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
    option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
    if value and hasattr(value, 'instance'):
      instance = value.instance
      option['attrs']['data-type'] = instance.type
      option['attrs']['data-grade'] = instance.grade
    return option

class BOSChoiceWidget(forms.Select):
  def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
    option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
    if value and hasattr(value, 'instance'):
      instance = value.instance
      option['attrs']['data-ms'] = instance.ms
    return option

class PersonnelForm(forms.ModelForm):
  PROFILE_CHOICES = (
    ('', '---------'),
    ('Officer', 'Officer'),
    ('EP', 'EP'),
    ('CHR', 'CHR'),
  )
  profile = forms.ChoiceField(choices = PROFILE_CHOICES, label='Profile', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  rank = forms.ModelChoiceField(queryset=Rank.objects.all(), label="Rank", widget=RankChoiceWidget(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  middle_name = forms.CharField(label='Middle Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  ext_name = forms.CharField(label='Extension Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  afpsn = forms.CharField(label='AFPSN', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  item_no = forms.CharField(label='Plantilla Item No', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  bos = forms.ModelChoiceField(queryset=BOS.objects.all(), label="BOS", widget=BOSChoiceWidget(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  SEX_CHOICES = (
    ('', '---------'),
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = forms.ChoiceField(choices = SEX_CHOICES, label='Sex', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  dob = forms.DateField(label='DOB', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
  office = forms.ModelChoiceField(queryset=Office.objects.all(), label="Office", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  position = forms.ModelChoiceField(queryset=Position.objects.all(), label="Position Title", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  desig = forms.CharField(label='Designation', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  status_assignment = forms.ModelChoiceField(queryset=SOA.objects.all(), label="SOA", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  ds_unit = forms.ModelChoiceField(queryset=Office.objects.all(), label="New Unit", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  fos = forms.CharField(label='FOS/MOS', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  daghq = forms.DateField(label='DAGHQ', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  dapda = forms.DateField(label='DAPDA', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  rrfcd = forms.CharField(label='RRFCD', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  skills = forms.CharField(label='Skills', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  dot = forms.DateField(label='DOT', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  doc = forms.DateField(label='DOC', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  dolp = forms.DateField(label='DOLP', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  hcc = forms.CharField(label='HCC', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  soc = forms.CharField(label='SOC', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  doret = forms.DateField(label='DORET', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  auth = forms.CharField(label='AUTH', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  act = forms.CharField(label='ACT', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  vacant = forms.CharField(label='Vacant', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  cti = forms.CharField(label='CTI', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  is_active = forms.BooleanField(label='Is active?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
    
  class Meta:
    model = Personnel
    fields = ['profile', 'rank', 'first_name', 'middle_name', 'last_name', 'ext_name', 'afpsn', 'item_no', 'bos', 'sex', 'dob', 'office', 'position', 'desig', 'status_assignment', 'ds_unit', 'fos', 'daghq', 'dapda', 'rrfcd', 'skills', 'dot', 'doc', 'dolp', 'hcc', 'soc', 'doret', 'auth', 'act', 'vacant', 'cti', 'is_active', ]

class DSForm(forms.Form):
  personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label="Personnel", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  
class StudentForm(forms.ModelForm):
  personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label="Personnel", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  
  class Meta:
    model = Student
    fields = ['personnel', ]

class PatientForm(forms.ModelForm):
  personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label="Personnel", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  
  class Meta:
    model = Patient
    fields = ['personnel', ]

class ReportDateFilterForm(forms.Form):
  date = forms.DateField(label='Date', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=False)
  
class UploadFileForm(forms.Form):
  file = forms.FileField(label='File')
  
class AdminUploadFileForm(forms.Form):
  office = forms.ModelChoiceField(queryset=Office.objects.all(), label="Office", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  file = forms.FileField(label='File', required=True)

class SOAForm(BSModalModelForm):
  soa = forms.CharField(label='SOA', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  description = forms.CharField(label='Description', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  is_effective = forms.BooleanField(label='Effectiveness', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  with_unit = forms.BooleanField(label='With Carrying Unit?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  reporting = forms.BooleanField(label='Reporting', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  is_school = forms.BooleanField(label='School', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  is_medical = forms.BooleanField(label='Medical Facility', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  is_outside = forms.BooleanField(label='Outside Organization', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  
  class Meta:
    model = SOA
    fields = ['soa', 'description', 'is_effective', 'with_unit', 'reporting', 'is_school', 'is_medical', 'is_outside', ]

class PositionForm(BSModalModelForm):
  position = forms.CharField(label='Position', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  description = forms.CharField(label='Description', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  parenthetical = forms.CharField(label='Parenthetical', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  grade = forms.IntegerField(label='Grade', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm',}), required=True)
        
  class Meta:
    model = Position
    fields = ['position', 'description', 'parenthetical', 'grade', ]

class AgeReportFilterForm(forms.Form):
  category = forms.ModelChoiceField(queryset=OfficeCategory.objects.all(), label="Office Category", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  