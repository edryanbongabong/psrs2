from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q

def get_settings():
  options = Option.objects.first()
  return options

def groups_str(groups):
  return ', '.join([group.name for group in groups])

def get_units(id, all_units=False):
  units = []
  if all_units:
    units.append(Office.objects.get(id=id))
  offices = Office.objects.filter(Q(parent=id))
  if not offices:
    return units
  for unit in offices:
    units.append(unit)
    if get_units(unit.id):
      units += get_units(unit.id)
  return units

def get_units_flat(id, all_units=False):
  units = []
  if all_units:
    units.append(Office.objects.get(id=id))
  offices = Office.objects.filter(Q(parent=id))
  if not offices:
    return units
  for unit in offices:
    units.append(unit)
    if get_units_flat(unit.id):
      units += get_units_flat(unit.id)
  return units