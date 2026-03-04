from django.shortcuts import render, redirect
from personnel.models import *
from .models import *
from .forms import *
from .decorators import *
from .functions import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
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
from django.urls import reverse_lazy, reverse
import html
from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
from django.db import connection

def handler404(request, exception):
  return render(request, '404.html')

def is_ajax(meta):
  if 'HTTP_X_REQUESTED_WITH' not in meta:
    return False
  if meta['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
    return True
  return False

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('login')
  else:
    if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
          login(request, user)
          messages.success(request, 'Login successfully')
          return redirect('home')
        else:
          messages.info(request, 'Username or password is incorrect')
      else:
          messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
      form = LoginForm()
    
    context = {"form": form, "options": get_settings()}
    
    return render(request, 'login.html', context)

@login_required(login_url='login')
def logoutUser(request):
  logout(request)
  
  return redirect('login')

@login_required(login_url='login')
def profile(request):
  uid = request.user.id
  user = User.objects.get(id=int(uid))
 
  form = UpdateMyUserForm(instance=user)
  template = 'profile.html'
  
  if request.method == 'POST':
    form = UpdateMyUserForm(request.POST, instance=user)
    profile = Profile.objects.get(user=int(uid))
    if profile:
      profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
    else:
      profileForm = ProfileForm(request.POST, request.FILES)
    if form.is_valid() and profileForm.is_valid():
      form.save()
      profileForm.save()
   
      messages.success(request, 'Profile updated successfully!')
      return redirect('profile')
    else:
      context = {
        'title' : 'My Profile',
        'options': get_settings(),
        'form' : form,
        'profileForm' : profileForm,
      }
      messages.error(request, 'Please correct the error below.')
  else:
    profile = Profile.objects.get(user=int(uid))
    if profile:
      profileForm = ProfileForm(instance=profile)
    else:
      profileForm = ProfileForm()
    context = {
      'title' : 'My Profile',
      'options': get_settings(),
      'form' : form,
      'profileForm' : profileForm,
    }
  
  return render(request, template, context)

def get_next_color(index):
  colors = [
    "rgba(202, 201, 197, 0.7)",  # Light gray
    "rgba(171, 9, 0, 0.7)",  # Red
    "rgba(166, 78, 46, 0.7)",  # Light orange
    "rgba(255, 190, 67, 0.7)",  # Yellow
    "rgba(163, 191, 63, 0.7)",  # Light green
    "rgba(122, 159, 191, 0.7)",  # Light blue
    "rgba(140, 5, 84, 0.7)",  # Pink
    "rgba(166, 133, 93, 0.7)",
    "rgba(75, 64, 191, 0.7)",
    "rgba(237, 124, 60, 0.7)",
  ]
  return colors[index % len(colors)]

@login_required(login_url='login')
def donut_chart(request, cat):
  reports = get_published_reports(request, True)
  if reports:
    ids = tuple(reports) if len(reports) > 1 else f"({reports[0]})"
    query = f"SELECT DISTINCT {cat} FROM personnel_personnelhist WHERE report_id IN {ids};"
  else:
    query = f"SELECT DISTINCT {cat} FROM personnel_personnelhist WHERE report_id IN ();"
  with connection.cursor() as cursor:
    cursor.execute(query)
    results = cursor.fetchall()
  
  labels = []
  data = []
  colors = []
  for i, field in enumerate(results):
    labels.append(field[0])
    data.append(PersonnelHist.objects.filter(**{cat: field[0]}).filter(report_id__in=reports).count())
    colors.append(get_next_color(i))

  context = {
    'labels' : labels,
    'datasets' : [{
      'data': data,
      'backgroundColor': colors,
    }],
  }
  return JsonResponse({'data': context})

@login_required(login_url='login')
def home(request):
  template = 'dashboard.html'
  context = {
    'title' : 'Home',
    'uri' : 'dashboard',
    'options': get_settings(),
    'personnel' : get_personnel(request),
    'submission' : get_submission(request),
    'movements' : get_personnel_movement(request),
  }
  return render(request, template, context)

@login_required(login_url='login')
def get_published_reports(request, id_only=False):
  data = []
  office = request.user.users_profile.office
  current_date = datetime.now().date()
  if request.user.groups.filter(name='System Administrator').exists():
    units = Office.objects.filter(is_active=True)
    for unit in units:
      report = Report.objects.filter(office=unit, is_approved=True, date__lte=current_date).order_by('-date')
      if report:
        data.append(report[0].id if id_only else report[0])
  else:
    units = get_units(office.id, True)
    for unit in units:
      report = Report.objects.filter(office=unit, is_approved=True, date__lte=current_date).order_by('-date')
      if report:
        data.append(report[0].id if id_only else report[0])
  return data

@login_required(login_url='login')
def get_submission(request):
  data = {}
  subdata = []
  office = request.user.users_profile.office
  current_date = datetime.now().date()
  current_datetime = datetime.now()
  current_hour = current_datetime.hour
  compare_date = current_datetime - timedelta(days=1 if current_hour >= 8 else 2)
  compare_date = compare_date.date()
  units = Office.objects.filter(is_active=True, parent=None if request.user.groups.filter(name='System Administrator').exists() else office).order_by('id')
  total = 0
  for unit in units:
    offices = get_units(unit.id, True)
    subtotal = 0
    date = ''
    for office in offices:
      report = Report.objects.filter(office=office, is_approved=True, date__lte=current_date).order_by('-date')
      if report:
        subtotal = subtotal + PersonnelHist.objects.filter(report=report[0]).count()
        if office == unit:
          date = report[0].date
    if subtotal:
      subdata.append({
        'unit': unit,
        'strength': subtotal,
        'status': '<span class="badge badge-success">Updated</span>' if date >= compare_date else '<span class="badge badge-warning">Outdated</span>',
        'date': date.strftime('%d %b %Y'),
      })
      total = total + subtotal
    else:
      subdata.append({
        'unit': unit,
        'strength': '',
        'status': '<span class="badge badge-light font-italic">No Data!</span>',
        'date': '',
      })
  data['subdata'] = subdata
  data['total'] = total
  return data

@login_required(login_url='login')
def get_personnel(request):
  reports = get_published_reports(request)
  data = {}
  personnel = PersonnelHist.objects.filter(report__in=reports)
  data['total'] = personnel.count()
  if request.user.groups.filter(name='System Administrator').exists():
    data['current_unit'] = 'All Offices'
  else:
    data['current_unit'] = request.user.users_profile.office
  
  distinct_profiles = PersonnelHist.objects.filter(report__in=reports).order_by('-profile').values_list('profile', flat=True).distinct()
  profiles = []
  badge_colors = ['primary', 'success', 'warning', 'info', 'danger', ]
  for i, profile in enumerate(distinct_profiles):
    count = PersonnelHist.objects.filter(report__in=reports, profile=profile).count()
    profiles_data = {
      'profile': profile,
      'count': count,
      'width': round((count/personnel.count())*100),
      'color': badge_colors[i]
    }
    profiles.append(profiles_data)
  data['profiles'] = profiles
  
  profile_types = ['Officer', 'EP']
  mss = ['PA', 'PN', 'PAF', 'TAS']
  profile_type_data = {}
  for i, profile_type in enumerate(profile_types):
    distinct_ranks = Rank.objects.filter(type=profile_type).order_by('-grade').values_list('grade', flat=True).distinct()
    total = [0,0,0,0]
    rank_data = {}
    for j, rank_code in enumerate(distinct_ranks):
      ms_data = {}
      for k, ms in enumerate(mss):
        bos_ms = BOS.objects.filter(ms=ms).values('bos')
        rank = Rank.objects.filter(type=profile_type, grade=rank_code).values('rank')
        personnel_list = PersonnelHist.objects.filter(report__in=reports, profile=profile_type, bos__in=bos_ms, rank__in=rank)
        ms_data[ms] = personnel_list.count()
        total[k] = total[k] + personnel_list.count()
        
      rank_data[rank_code] = ms_data
      if j == distinct_ranks.count()-1:
        rank_data['total'] = total
    profile_type_data[profile_type] = rank_data
  data['fillup'] = profile_type_data
  return data

@login_required(login_url='login')
def get_personnel_movement(request):
  office = request.user.users_profile.office
  if request.user.groups.filter(name='System Administrator').exists():
    return PersonnelMovement.objects.order_by('-date')[:20]
  else:    
    return PersonnelMovement.objects.filter(Q(office1=office)|Q(office2=office)|Q(temp_office1=office)|Q(temp_office2=office)).order_by('-date')[:20]

# User Management
@login_required(login_url='login')
@allowed_users(allowed_groups=['System Administrator'])
def users_view(request):
  template = 'users/table.html'
  context = {
    'title' : 'Users',
    'modal_size' : 'xl',
    'options': get_settings(),
  }
  return render(request, template, context)

class UserAjaxDatatableView(AjaxDatatableView):
  model = Profile
  title = 'Users'
  
  initial_order = [["id", "asc"], ]
  length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
  search_values_separator = '+'

  column_defs = [
    {'name': 'id', 'visible': False, 'orderable': True},
    {'name': 'picture', 'title': 'Pic', 'searchable': False, 'orderable': False, 'visible': True, 'className': 'text-center', },
    {'name': 'username', 'title': 'Username', 'foreign_field': 'user__username',  'visible': True, 'className': 'text-center', },
    {'name': 'first_name', 'title': 'First Name', 'foreign_field': 'user__first_name',  'visible': True, 'className': 'text-center', },
    {'name': 'last_name', 'title': 'Last Name', 'foreign_field': 'user__last_name',  'visible': True, 'className': 'text-center', },
    {'name': 'email', 'title': 'Email', 'foreign_field': 'user__email',  'visible': True, 'className': 'text-center', },
    {'name': 'office', 'title': 'Office',  'visible': True, 'className': 'text-center', },
    {'name': 'groups', 'title': 'Groups', 'searchable': False, 'orderable': False,  'visible': True, 'className': 'text-center', },
    {'name': 'sign_name', 'title': 'Name (Sign)',  'visible': True, 'className': 'text-center', },
    {'name': 'sign_rank', 'title': 'Rank (Sign)',  'visible': True, 'className': 'text-center', },
    {'name': 'sign_designation', 'title': 'Designation (Sign)',  'visible': True, 'className': 'text-center', },
    {'name': 'sign', 'title': 'Sign',  'visible': True, 'className': 'text-center', },
    {'name': 'is_active', 'title': 'Active', 'foreign_field': 'user__is_active',  'visible': True, 'className': 'text-center', },
    {'name': 'tools', 'title': 'Tools', 'placeholder': True, 'searchable': False, 'orderable': False, 'className': 'text-center', },
  ]
  
  def customize_row(self, row, obj):
    row['picture'] = f'<a href="{ obj.picture.url }" target="_blank"><img class="img-fluid img-circle" width="50" src="{ obj.picture.url }" alt="User profile picture"></a>'
    row['groups'] = groups_str(obj.user.groups.all())
    if obj.sign:
      row['sign'] = f'<a href="{ obj.sign.url }" target="_blank"><img class="img-fluid img-circle" width="50" src="{ obj.sign.url }" alt="Signature"></a>'
    edit_url = reverse('update-user', kwargs={'id': obj.user.id })
    delete_url = reverse('delete-user', kwargs={'pk': obj.user.id })
    change_password_url = reverse('change-password-user', kwargs={'id': obj.user.id })
    row['tools'] = (
      f'<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><i class="fas fa-sliders-h"></i></button>'
      f'<div class="dropdown-menu">'
      f'<a href="#" class="dropdown-item py-2 bs-modal update-data" data-form-url="{edit_url}"><i class="fas fa-pencil-alt"></i> Edit</a>'
      f'<a href="#" class="dropdown-item py-2 bs-modal change-password-data" data-form-url="{change_password_url}"><i class="fas fa-key"></i> Change Password</a>'
      f'<div class="dropdown-divider"></div>'
      f'<a href="#" class="dropdown-item py-2 text-danger bs-modal delete-data" data-form-url="{delete_url}"><i class="fas fa-trash"></i> Delete</a>'
      f'</div>'
    )
    return

@login_required(login_url='login')
@allowed_users(allowed_groups=['System Administrator'])
def change_password_user(request, id):
  template = 'layouts/form-data.html'
  user = User.objects.get(id=id)
  form = SetPasswordForm(user)
  if request.method == 'POST':
    form = SetPasswordForm(user, request.POST)
    if form.is_valid():
      if not is_ajax(request.META):
        form.save()
      messages.success(request, 'Password successfully updated!')
      return redirect('users')
    else:
      messages.error(request, 'Please correct the error below.')
  context = {
    'options': get_settings(),
    'form' : form,
    'mode' : 'Change Password',
    'segment' : 'User',
  }
  return render(request, template, context)

@login_required(login_url='login')
def create_user(request):
  template = 'users/create_user.html'
  form = CreateUserForm()
  profileForm = ProfileForm()
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    profileForm = ProfileForm(request.POST, request.FILES)
    if form.is_valid() and profileForm.is_valid():
      if not is_ajax(request.META):
        user = form.save()
        user_object = User.objects.get(pk=user.id)
        group_field = form.cleaned_data['groups']
        for g in group_field:
          group = Group.objects.get(name=g)
          user_object.groups.add(group)
        
        profile = Profile.objects.get(user=int(user.id))
        profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        p = profileForm.save(commit=False)
        p.user_id = user.id
        p.save()
      messages.success(request, 'User details was successfully added!')
      return redirect('users')
    else:
      messages.error(request, 'Please correct the error.')
  context = {
    'options': get_settings(),
    'form' : form,
    'profileForm' : profileForm,
  }
  return render(request, template, context)

@login_required(login_url='login')
@allowed_users(allowed_groups=['System Administrator'])
def update_user(request, id):
  template = 'users/update_user.html'
  user = User.objects.get(id=id)
  form = UpdateUserForm(instance=user)
  profile = Profile.objects.get(user=int(user.id))
  profileForm = ProfileForm(instance=profile)
  if request.method == 'POST':
    form = UpdateUserForm(request.POST, instance=user)
    profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid() and profileForm.is_valid():
      if not is_ajax(request.META):
        form.save()
        user.groups.clear()
        group_field = form.cleaned_data['groups']
        for g in group_field:
          group = Group.objects.get(name=g)
          user.groups.add(group)
        profileForm.save()
      messages.success(request, 'User details was successfully updated!')
      return redirect('users')
    else:
      messages.error(request, 'Please correct the error.')
  context = {
    'options': get_settings(),
    'form' : form,
    'profileForm' : profileForm,
  }
  return render(request, template, context)

class UserDeleteView(BSModalDeleteView):
  model = User
  template_name = 'users/delete_user.html'
  success_message = 'User was successfully deleted.'
  success_url = reverse_lazy('users')

# Settings
@login_required(login_url='login')
@allowed_users(allowed_groups=['System Administrator'])
def settings(request):
  template = 'settings.html'
  colors = [
    "primary",
    "secondary",
    "info",
    "success",
    "danger",
    "indigo",
    "purple",
    "pink",
    "navy",
    "lightblue",
    "teal",
    "cyan",
    "gray-dark",
    "gray",
    "light",
    "warning",
    "orange",
  ]
  
  options = Option.objects.first()
  form = OptionForm(instance=options)
  if request.method == 'POST':
    form = OptionForm(request.POST, request.FILES, instance=options)
    if form.is_valid():      
      form.save()  
      messages.success(request, 'System settings was successfully updated.')
      return redirect('settings')
    else:
      messages.error(request, 'Please correct the error below.')
  context = {
    'title' : 'System Settings',
    'options': get_settings(),
    'form' : form,
    'colors' : colors,
  }
  return render(request, template, context)

# Ranks
@login_required(login_url='login')
def ranks(request):
  template = 'layouts/table.html'
  context = {
    'title' : 'Ranks',
    'modal_size' : 'md',
    'options': get_settings(),
  }
  return render(request, template, context)

class RankAjaxDatatableView(AjaxDatatableView):
  model = Rank
  title = 'Ranks'
  
  initial_order = [["type", "desc"], ["grade", "desc"], ["id", "asc"], ]
  length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
  search_values_separator = '+'

  column_defs = [
    # AjaxDatatableView.render_row_tools_column_def(),
    {'name': 'id', 'visible': False, 'orderable': True},
    {'name': 'rank', 'visible': True, },
    {'name': 'rank_full', 'visible': True, },
    {'name': 'grade', 'visible': True, 'className': 'text-center', },
    {'name': 'type', 'visible': True, 'className': 'text-center', },
    {'name': 'tools', 'title': 'Tools', 'placeholder': True, 'searchable': False, 'orderable': False, 'className': 'text-center', },
  ]
  
  def customize_row(self, row, obj):
    row['tools'] = '<button type="button" class="update-data bs-modal btn btn-xs btn-primary" data-form-url="update/%s/"><i class="fas fa-pencil-alt"></i> Edit</button>&nbsp;<button type="button" class="delete-data bs-modal btn btn-xs btn-danger" data-form-url="delete/%s/"><i class="fas fa-trash"></i> Delete</button>' % (row['pk'], row['pk'])
    if(row['type'] in ['Officer', 'EP']):
      row['grade'] = f"{row['type'][0]}-{row['grade']}"
    return

class RankCreateView(BSModalCreateView):
  template_name = 'layouts/form-data.html'
  form_class = RankModelForm
  success_message = 'Rank was successfully created.'
  success_url = reverse_lazy('ranks')
  
  def get_context_data(self, **kwargs):
    ctx = super(RankCreateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Rank'
    ctx['mode'] = 'Create'
    ctx['options'] = get_settings()
    return ctx

class RankUpdateView(BSModalUpdateView):
  model = Rank
  template_name = 'layouts/form-data.html'
  form_class = RankModelForm
  success_message = 'Rank was successfully updated.'
  success_url = reverse_lazy('ranks')
  
  def get_context_data(self, **kwargs):
    ctx = super(RankUpdateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Rank'
    ctx['mode'] = 'Update'
    ctx['options'] = get_settings()
    return ctx
  
class RankDeleteView(BSModalDeleteView):
  model = Rank
  template_name = 'layouts/form-data-delete.html'
  success_message = 'Rank was successfully deleted.'
  success_url = reverse_lazy('ranks')
  
  def get_context_data(self, **kwargs):
    ctx = super(RankDeleteView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Rank'
    ctx['mode'] = 'Delete'
    ctx['object_name'] = self.object.rank
    ctx['options'] = get_settings()
    return ctx

# Offices
@login_required(login_url='login')
def offices(request):
  template = 'layouts/table.html'
  context = {
    'title' : 'Offices',
    'modal_size' : 'xl',
    'options': get_settings(),
  }
  return render(request, template, context)

class OfficeAjaxDatatableView(AjaxDatatableView):
  model = Office
  title = 'Offices'
  
  initial_order = [["program", "asc"], ["office_category", "asc"], ["id", "asc"], ]
  length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
  search_values_separator = '+'

  column_defs = [
    {'name': 'id', 'visible': False, 'orderable': True},
    {'name': 'office', 'visible': True, },
    {'name': 'office_name', 'visible': True, },
    {'name': 'office_category', 'foreign_field': 'office_category__category', 'visible': True, 'className': 'text-center', },
    {'name': 'program', 'visible': True, 'className': 'text-center', },
    {'name': 'parent', 'foreign_field': 'parent__office', 'visible': True, 'className': 'text-center', },
    {'name': 'is_school', 'searchable': False, 'visible': True, 'className': 'text-center', },
    {'name': 'is_medical', 'searchable': False, 'visible': True, 'className': 'text-center', },
    {'name': 'is_active', 'searchable': False, 'visible': True, 'className': 'text-center', },
    {'name': 'tools', 'title': 'Tools', 'placeholder': True, 'searchable': False, 'orderable': False, 'className': 'text-center', },
  ]
  
  def customize_row(self, row, obj):
    row['tools'] = '<button type="button" class="update-data bs-modal btn btn-xs btn-primary" data-form-url="update/%s/"><i class="fas fa-pencil-alt"></i> Edit</button>&nbsp;<button type="button" class="delete-data bs-modal btn btn-xs btn-danger" data-form-url="delete/%s/"><i class="fas fa-trash"></i> Delete</button>' % (row['pk'], row['pk'])
    return

class OfficeCreateView(BSModalCreateView):
  template_name = 'offices/form-data.html'
  form_class = OfficeModelForm
  success_message = 'Office was successfully created.'
  success_url = reverse_lazy('offices')
  
  def get_context_data(self, **kwargs):
    ctx = super(OfficeCreateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Office'
    ctx['mode'] = 'Create'
    ctx['options'] = get_settings()
    return ctx

class OfficeUpdateView(BSModalUpdateView):
  model = Office
  template_name = 'offices/form-data.html'
  form_class = OfficeModelForm
  success_message = 'Office was successfully updated.'
  success_url = reverse_lazy('offices')
  
  def get_context_data(self, **kwargs):
    ctx = super(OfficeUpdateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Office'
    ctx['mode'] = 'Update'
    ctx['options'] = get_settings()
    return ctx
  
class OfficeDeleteView(BSModalDeleteView):
  model = Office
  template_name = 'layouts/form-data-delete.html'
  success_message = 'Office was successfully deleted.'
  success_url = reverse_lazy('offices')
  
  def get_context_data(self, **kwargs):
    ctx = super(OfficeDeleteView, self).get_context_data(**kwargs)
    ctx['segment'] = 'Office'
    ctx['mode'] = 'Delete'
    ctx['options'] = get_settings()
    ctx['object_name'] = self.object.office
    return ctx

# BOS
@login_required(login_url='login')
def bos(request):
  template = 'layouts/table.html'
  context = {
    'title' : 'BOS',
    'modal_size' : 'sm',
    'options': get_settings(),
  }
  return render(request, template, context)

class BOSAjaxDatatableView(AjaxDatatableView):
  model = BOS
  title = 'BOS'
  
  initial_order = [["id", "asc"], ]
  length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
  search_values_separator = '+'

  column_defs = [
    {'name': 'id', 'visible': False, 'orderable': True},
    {'name': 'bos', 'visible': True, 'className': 'text-center', },
    {'name': 'ms', 'visible': True, 'className': 'text-center', },
    {'name': 'tools', 'title': 'Tools', 'placeholder': True, 'searchable': False, 'orderable': False, 'className': 'text-center', },
  ]
  
  def customize_row(self, row, obj):
    row['tools'] = '<button type="button" class="update-data bs-modal btn btn-xs btn-primary" data-form-url="update/%s/"><i class="fas fa-pencil-alt"></i> Edit</button>&nbsp;<button type="button" class="delete-data bs-modal btn btn-xs btn-danger" data-form-url="delete/%s/"><i class="fas fa-trash"></i> Delete</button>' % (row['pk'], row['pk'])
    return

class BOSCreateView(BSModalCreateView):
  template_name = 'layouts/form-data.html'
  form_class = BOSModelForm
  success_message = 'BOS was successfully created.'
  success_url = reverse_lazy('bos')
  
  def get_context_data(self, **kwargs):
    ctx = super(BOSCreateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'BOS'
    ctx['mode'] = 'Create'
    ctx['options'] = get_settings()
    return ctx

class BOSUpdateView(BSModalUpdateView):
  model = BOS
  template_name = 'layouts/form-data.html'
  form_class = BOSModelForm
  success_message = 'BOS was successfully updated.'
  success_url = reverse_lazy('bos')
  
  def get_context_data(self, **kwargs):
    ctx = super(BOSUpdateView, self).get_context_data(**kwargs)
    ctx['segment'] = 'BOS'
    ctx['mode'] = 'Update'
    ctx['options'] = get_settings()
    return ctx
  
class BOSDeleteView(BSModalDeleteView):
  model = BOS
  template_name = 'layouts/form-data-delete.html'
  success_message = 'BOS was successfully deleted.'
  success_url = reverse_lazy('bos')
  
  def get_context_data(self, **kwargs):
    ctx = super(BOSDeleteView, self).get_context_data(**kwargs)
    ctx['segment'] = 'BOS'
    ctx['mode'] = 'Delete'
    ctx['options'] = get_settings()
    ctx['object_name'] = self.object.bos
    return ctx
