from django.shortcuts import render, redirect
from general.models import *
from personnel.models import *
from .models import *
from .forms import *
from general.decorators import *
from general.functions import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ajax_datatable.views import AjaxDatatableView
from datetime import datetime, timedelta
from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalUpdateView,
  BSModalReadView,
  BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views.generic.edit import (
  CreateView, UpdateView
)

def is_ajax(meta):
  if 'HTTP_X_REQUESTED_WITH' not in meta:
    return False
  if meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
    return True
  return False

@login_required(login_url='login')
def orders_view(request):
  template = 'orders.html'
  context = {
    'title' : 'Orders',
    'uri' : 'orders',
    'options': get_settings(),
  }
  return render(request, template, context)

class OrdersAjaxDatatableView(AjaxDatatableView):
  model = Order
  title = 'Orders'
  
  initial_order = [ ["id", "asc"], ]
  length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
  search_values_separator = '+'

  column_defs = [
    {'name': 'id', 'visible': False, 'orderable': True},
    {'name': 'order_no', 'title': 'Order No', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-center', },
    {'name': 'title', 'title': 'Title', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-left', },
    {'name': 'type', 'foreign_field': 'type__type', 'title': 'Type', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-center', },
    {'name': 'tags', 'title': 'Tags', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-left', },
    {'name': 'date_published', 'title': 'Date Published', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-center', },
    {'name': 'updated_at', 'title': 'Date Modified', 'placeholder': True, 'searchable': True, 'orderable': True, 'className': 'text-center', },
    {'name': 'tools', 'title': 'Tools', 'placeholder': True, 'searchable': False, 'orderable': False, 'className': 'text-center', },
    
  ]
  
  def customize_row(self, row, obj):
    row['title'] = '<a href="%s" target="_blank">%s</a>' % (obj.attachment.url, obj.title)
    if obj.tags:
      row['tags'] = f'<span class="badge badge-info">{'</span>&nbsp;<span class="badge badge-info">'.join(obj.tags.split(','))}</span>'
    row['tools'] = '<div class="btn-group"><a href="update/%s/" type="button" class="update-data btn btn-xs btn-primary"><i class="fas fa-edit"></i></a><a type="button" class="delete-data btn btn-xs btn-danger" href="#" data-form-url="delete/%s/"><i class="fas fa-trash"></i></a></div>' % (obj.unique_id, row['pk'])
    return

  def get_initial_queryset(self, request=None):
    qs = super().get_initial_queryset(request)
    return qs

class OrderInLine():
  form_class = OrderModelForm
  model = Order
  template_name = "orders/form_order.html"

  def form_valid(self, form):
    named_formsets = self.get_named_formsets()
    if not all((x.is_valid() for x in named_formsets.values())):
      return self.render_to_response(self.get_context_data(form=form))
    self.object = form.save()

    for name, formset in named_formsets.items():
      formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
      if formset_save_func is not None:
          formset_save_func(formset)
      else:
          formset.save()
    return redirect('orders')

  def formset_orderpersonnel_valid(self, formset):
    orderpersonnel = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for orderpers in orderpersonnel:
      orderpers.order = self.object
      orderpers.save()

class OrderCreate(OrderInLine, CreateView):
  def get_context_data(self, **kwargs):    
    ctx = super(OrderCreate, self).get_context_data(**kwargs)
    ctx['named_formsets'] = self.get_named_formsets()
    ctx['title'] = 'Create Order'
    ctx['uri'] = 'form_order'
    ctx['options'] = get_settings()
    return ctx

  def get_named_formsets(self):
    return {
      'orderpersonnel': OrderFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='orderpersonnel'),
    }

class OrderUpdate(OrderInLine, UpdateView):
  def get_object(self, queryset=None):
    return Order.objects.get(unique_id=self.kwargs.get("uuid"))
      
  def get_context_data(self, **kwargs):    
    ctx = super(OrderUpdate, self).get_context_data(**kwargs)
    ctx['named_formsets'] = self.get_named_formsets()
    ctx['title'] = 'Create Order'
    ctx['uri'] = 'form_order'
    ctx['options'] = get_settings()
    return ctx

  def get_named_formsets(self):
    return {
      'orderpersonnel': OrderFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='orderpersonnel'),
    }

class OrderDeleteView(BSModalDeleteView):
  model = Order
  template_name = 'orders/delete_order.html'
  success_message = 'Order was successfully deleted.'
  success_url = reverse_lazy('orders')