from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms import Form, MultipleChoiceField, ChoiceField
from captcha.fields import CaptchaField
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.Form):
  username = forms.CharField(label='Username', max_length=150)
  password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput())
  # captcha = CaptchaField()
  
  def clean_username(self):
    username = self.cleaned_data['username']
    return username
  
  def clean_password(self):
    password = self.cleaned_data['password']
    return password

class RankModelForm(BSModalModelForm):
  TYPE_CHOICES = (
    ('', '-- S E L E C T --'),
    ('Officer', 'Officer'),
    ('EP', 'EP'),
    ('CHR', 'CHR'),
  )
  rank = forms.CharField(label='Rank', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  rank_full = forms.CharField(label='Rank Name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  grade = forms.IntegerField(label='Grade', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  type = forms.ChoiceField(choices = TYPE_CHOICES, label="Type", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  class Meta:
    model = Rank
    fields = ['rank', 'rank_full', 'grade', 'type']

class OfficeModelForm(BSModalModelForm):
  PROGRAM_CHOICES = (
    ('', '-- S E L E C T --'),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
  )
  office = forms.CharField(label='Office', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  office_name = forms.CharField(label='Office Name', max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  office_category = forms.ModelChoiceField(queryset=OfficeCategory.objects.all(), label="Office Category", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  program = forms.ChoiceField(choices = PROGRAM_CHOICES, label="Program", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  parent = forms.ModelChoiceField(queryset=Office.objects.all(), label="Parent Unit", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  is_school = forms.BooleanField(label='Is training school?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  is_medical = forms.BooleanField(label='Is medical facility?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  is_active = forms.BooleanField(label='Is active?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  obi01 = forms.IntegerField(label='O-BI 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi02 = forms.IntegerField(label='O-BI 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi03 = forms.IntegerField(label='O-BI 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi04 = forms.IntegerField(label='O-BI 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi05 = forms.IntegerField(label='O-BI 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi06 = forms.IntegerField(label='O-BI 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi07 = forms.IntegerField(label='O-BI 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi08 = forms.IntegerField(label='O-BI 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi09 = forms.IntegerField(label='O-BI 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  obi10 = forms.IntegerField(label='O-BI 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa01 = forms.IntegerField(label='O-PA 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa02 = forms.IntegerField(label='O-PA 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa03 = forms.IntegerField(label='O-PA 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa04 = forms.IntegerField(label='O-PA 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa05 = forms.IntegerField(label='O-PA 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa06 = forms.IntegerField(label='O-PA 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa07 = forms.IntegerField(label='O-PA 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa08 = forms.IntegerField(label='O-PA 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa09 = forms.IntegerField(label='O-PA 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opa10 = forms.IntegerField(label='O-PA 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf01 = forms.IntegerField(label='O-PAF 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf02 = forms.IntegerField(label='O-PAF 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf03 = forms.IntegerField(label='O-PAF 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf04 = forms.IntegerField(label='O-PAF 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf05 = forms.IntegerField(label='O-PAF 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf06 = forms.IntegerField(label='O-PAF 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf07 = forms.IntegerField(label='O-PAF 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf08 = forms.IntegerField(label='O-PAF 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf09 = forms.IntegerField(label='O-PAF 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opaf10 = forms.IntegerField(label='O-PAF 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn01 = forms.IntegerField(label='O-PN 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn02 = forms.IntegerField(label='O-PN 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn03 = forms.IntegerField(label='O-PN 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn04 = forms.IntegerField(label='O-PN 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn05 = forms.IntegerField(label='O-PN 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn06 = forms.IntegerField(label='O-PN 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn07 = forms.IntegerField(label='O-PN 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn08 = forms.IntegerField(label='O-PN 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn09 = forms.IntegerField(label='O-PN 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  opn10 = forms.IntegerField(label='O-PN 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas01 = forms.IntegerField(label='O-TAS 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas02 = forms.IntegerField(label='O-TAS 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas03 = forms.IntegerField(label='O-TAS 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas04 = forms.IntegerField(label='O-TAS 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas05 = forms.IntegerField(label='O-TAS 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas06 = forms.IntegerField(label='O-TAS 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas07 = forms.IntegerField(label='O-TAS 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas08 = forms.IntegerField(label='O-TAS 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas09 = forms.IntegerField(label='O-TAS 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  otas10 = forms.IntegerField(label='O-TAS 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi01 = forms.IntegerField(label='E-BI 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi02 = forms.IntegerField(label='E-BI 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi03 = forms.IntegerField(label='E-BI 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi04 = forms.IntegerField(label='E-BI 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi05 = forms.IntegerField(label='E-BI 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi06 = forms.IntegerField(label='E-BI 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi07 = forms.IntegerField(label='E-BI 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi08 = forms.IntegerField(label='E-BI 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi09 = forms.IntegerField(label='E-BI 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  ebi10 = forms.IntegerField(label='E-BI 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa01 = forms.IntegerField(label='E-PA 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa02 = forms.IntegerField(label='E-PA 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa03 = forms.IntegerField(label='E-PA 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa04 = forms.IntegerField(label='E-PA 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa05 = forms.IntegerField(label='E-PA 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa06 = forms.IntegerField(label='E-PA 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa07 = forms.IntegerField(label='E-PA 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa08 = forms.IntegerField(label='E-PA 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa09 = forms.IntegerField(label='E-PA 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epa10 = forms.IntegerField(label='E-PA 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf01 = forms.IntegerField(label='E-PAF 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf02 = forms.IntegerField(label='E-PAF 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf03 = forms.IntegerField(label='E-PAF 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf04 = forms.IntegerField(label='E-PAF 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf05 = forms.IntegerField(label='E-PAF 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf06 = forms.IntegerField(label='E-PAF 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf07 = forms.IntegerField(label='E-PAF 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf08 = forms.IntegerField(label='E-PAF 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf09 = forms.IntegerField(label='E-PAF 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epaf10 = forms.IntegerField(label='E-PAF 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn01 = forms.IntegerField(label='E-PN 01', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn02 = forms.IntegerField(label='E-PN 02', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn03 = forms.IntegerField(label='E-PN 03', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn04 = forms.IntegerField(label='E-PN 04', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn05 = forms.IntegerField(label='E-PN 05', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn06 = forms.IntegerField(label='E-PN 06', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn07 = forms.IntegerField(label='E-PN 07', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn08 = forms.IntegerField(label='E-PN 08', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn09 = forms.IntegerField(label='E-PN 09', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  epn10 = forms.IntegerField(label='E-PN 10', widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-right', 'min': 0, 'step': 1}), required=False)
  
  class Meta:
    model = Office
    exclude = ['created_at', 'updated_at', 'updated_by', 'is_un', 'is_do']
    # fields = ['office', 'office_name', 'office_category', 'program', 'parent', 'is_school', 'is_medical', 'is_active']

class BOSModelForm(BSModalModelForm):
  MS_CHOICES = (
    ('', '-- S E L E C T --'),
    ('PA', 'PA'),
    ('PN', 'PN'),
    ('PAF', 'PAF'),
    ('TAS', 'TAS'),
    ('CHR', 'CHR'),
  )
  bos = forms.CharField(label='Branch of Service', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  ms = forms.ChoiceField(choices = MS_CHOICES, label="Major Service", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  class Meta:
    model = BOS
    fields = ['bos', 'ms']

# User Management
class CreateUserForm(UserCreationForm):
  username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  email = forms.EmailField(label='Email', max_length=254, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  password1 = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  password2 = forms.CharField(label='Confirm Password', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  is_active = forms.BooleanField(label='Is active?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True, )
  
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'groups', ]
    
class UpdateUserForm(UserChangeForm):
  username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'readonly': True}), required=False)
  email = forms.EmailField(label='Email', max_length=254, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'readonly': True}), required=False)
  first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  is_active = forms.BooleanField(label='Is active?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
  groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True, )
  
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'groups', ]

class UpdateMyUserForm(UserChangeForm):
  first_name = forms.CharField(label='First Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  
  class Meta:
    model = User
    fields = ['first_name', 'last_name', ]
    
class ProfileForm(forms.ModelForm):
  office = forms.ModelChoiceField(queryset=Office.objects.all(), label="Office", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  rank = forms.ModelChoiceField(queryset=Rank.objects.all(), label="Rank", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  bos = forms.ModelChoiceField(queryset=BOS.objects.all(), label="Branch of Service", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  sign_name = forms.CharField(label='Name (Sign)', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  sign_rank = forms.CharField(label='Rank (Sign)', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  sign_designation = forms.CharField(label='Designation (Sign)', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  
  class Meta:
    model = Profile
    fields = ['office', 'rank', 'bos', 'sign_name', 'sign_rank', 'sign_designation', 'picture', 'sign', ]

class CreateProfileForm(forms.ModelForm):
  required_css_class = 'required'
  # rank = forms.ModelChoiceField(queryset=Rank.objects.all(), label="Rank", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  # bos = forms.ModelChoiceField(queryset=BOS.objects.all(), label="BOS", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  middle_name = forms.CharField(label='Middle Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  ext_name = forms.CharField(label='Extension Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  # picture = forms.ImageField(label='Picture', allow_empty_file=True, widget=forms.FileInput(attrs={}), required=False)
  # office = forms.ModelChoiceField(queryset=Office.objects.all(), label="Office", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  complete_address = forms.CharField(label='Complete Address', max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  cp_number = forms.CharField(label='Cellphone Number', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  # afpcaa_member = forms.CharField(label='AFP/CAA Member', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  afpcaa_relationship = forms.CharField(label='Relationship', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  # guardian = forms.CharField(label='Guardian', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  dob = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
  pob = forms.CharField(label='Place of Birth', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  # religion = forms.CharField(label='Religion', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  CIVIL_STATUS_CHOICES = (
    ('', '---------'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Separated', 'Separated'),
  )
  # civil_status = forms.ChoiceField(choices = CIVIL_STATUS_CHOICES, label='Civil Status', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  SEX_CHOICES = (
    ('', '---------'),
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = forms.ChoiceField(choices = SEX_CHOICES, label='Sex', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  
  class Meta:
    model = Profile
    fields = ['middle_name', 'ext_name', 'complete_address', 'cp_number', 'afpcaa_relationship', 'dob', 'pob', 'sex']
    # fields = ['rank', 'bos', 'middle_name', 'ext_name', 'complete_address', 'cp_number', 'afpcaa_member', 'relationship', 'guardian', 'dob', 'pob', 'religion', 'civil_status', 'sex']

class UpdateMyProfileForm(forms.ModelForm):
  required_css_class = 'required'
  rank = forms.ModelChoiceField(queryset=Rank.objects.all(), label="Rank", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  bos = forms.ModelChoiceField(queryset=BOS.objects.all(), label="BOS", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  middle_name = forms.CharField(label='Middle Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  ext_name = forms.CharField(label='Extension Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  picture = forms.ImageField(label='Picture', allow_empty_file=True, widget=forms.FileInput(attrs={}), required=False)
  # office = forms.ModelChoiceField(queryset=Office.objects.all(), label="Office", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
  complete_address = forms.CharField(label='Complete Address', max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  cp_number = forms.CharField(label='Cellphone Number', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  afpcaa_member = forms.CharField(label='AFP/CAA Member', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  relationship = forms.CharField(label='Relationship', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  guardian = forms.CharField(label='Guardian', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  dob = forms.DateField(label='Date of Birth', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
  pob = forms.CharField(label='Place of Birth', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  religion = forms.CharField(label='Religion', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  CIVIL_STATUS_CHOICES = (
    ('', '---------'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Separated', 'Separated'),
  )
  civil_status = forms.ChoiceField(choices = CIVIL_STATUS_CHOICES, label='Civil Status', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  SEX_CHOICES = (
    ('', '---------'),
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = forms.ChoiceField(choices = SEX_CHOICES, label='Sex', widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  
  class Meta:
    model = Profile
    fields = ['rank', 'bos', 'middle_name', 'ext_name', 'picture', 'complete_address', 'cp_number', 'afpcaa_member', 'relationship', 'guardian', 'dob', 'pob', 'religion', 'civil_status', 'sex']


class OptionForm(forms.ModelForm):
  app_name = forms.CharField(label='Application Name', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  app_brand = forms.CharField(label='Application Brand', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  app_description = forms.CharField(label='Application Description', widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}), required=False)
  app_logo = forms.ImageField(allow_empty_file=True, widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
  THEME_CHOICES = (
    ('dark', 'Dark'),
    ('light', 'Light'),
  )
  theme = forms.ChoiceField(label='Theme', widget=forms.RadioSelect(attrs={'class': 'd-flex justify-content-between w-50',}), required=True, choices=THEME_CHOICES)
  theme_color = forms.CharField(label='Theme Color', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'readonly': True}), required=True)
  upload_max_size = forms.IntegerField(label='Upload Max Size', widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  
  class Meta:
    model = Option
    fields = ['app_name', 'app_brand', 'app_description', 'app_logo', 'theme', 'theme_color', 'upload_max_size']