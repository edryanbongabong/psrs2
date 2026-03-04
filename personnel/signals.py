from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from general.models import *

@receiver(pre_save, sender=Personnel)
def compare_field_values(sender, instance, **kwargs):
    if instance.pk:
      old_instance = sender.objects.get(pk=instance.pk)
      if instance.office_id != old_instance.office_id or instance.ds_unit_id != old_instance.ds_unit_id:
        PersonnelMovement.objects.create(
          personnel=instance,
          date=instance.updated_at,
          soa1=SOA.objects.get(id=instance.status_assignment_id) if instance.status_assignment_id else None,
          office1=Office.objects.get(id=instance.office_id) if instance.office_id else None,
          temp_office1=Office.objects.get(id=instance.ds_unit_id) if instance.ds_unit_id else None,
          soa2=instance.status_assignment,
          office2=instance.office,
          temp_office2=instance.ds_unit,
          updated_by=instance.updated_by,
        )

@receiver(post_save, sender=Personnel)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    created = PersonnelMovement.objects.create(
        personnel=instance,
        date=instance.updated_at,
        soa1=None,
        office1=None,
        temp_office1=None,
        soa2=instance.status_assignment,
        office2=instance.office,
        temp_office2=instance.ds_unit,
        updated_by=instance.updated_by,
      )