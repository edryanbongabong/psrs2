from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *
from personnel.models import *
from django.forms import inlineformset_factory

class OrderModelForm(forms.ModelForm):
  order_no = forms.CharField(label='Order No', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  title = forms.CharField(label='Title', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=True)
  date_published = forms.DateField(label='Date Published', widget=forms.widgets.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}), required=True)
  type = forms.ModelChoiceField(queryset=OrderType.objects.all(), label="Order Type", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  tags = forms.CharField(label='Tags', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',}), required=False)
  is_published = forms.BooleanField(label='Is Published?', widget=forms.CheckboxInput(attrs={'class': 'custom-control-input',}), required=False)
    
  class Meta:
    model = Order
    fields = ['order_no', 'title', 'date_published', 'type', 'tags', 'attachment', 'is_published', ]

class OrderPersonnelModelForm(forms.ModelForm):
  personnel = forms.ModelChoiceField(queryset=Personnel.objects.all(), label="Personnel", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=True)
  office = forms.ModelChoiceField(queryset=Office.objects.all(), label="New Unit", widget=forms.Select(attrs={'class':'form-control form-control-sm select2', 'style': 'width:100%;', }), required=False)
    
  class Meta:
    model = OrderPersonnel
    fields = ['personnel', 'office']

OrderFormSet = inlineformset_factory(
  Order, OrderPersonnel, form=OrderPersonnelModelForm, extra=1, can_delete=True, can_delete_extra=True
)