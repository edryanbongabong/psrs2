from django.db import models
from django.contrib.auth.models import User
from general.models import *
from personnel.models import *
from django.core.validators import FileExtensionValidator
import uuid

class CommonInfo(models.Model):
  created_at = models.DateTimeField('Created At', null=False, blank=False, auto_now_add=True, )
  updated_at = models.DateTimeField('Updated At', null=False, blank=False, auto_now=True, )
  
  def save(self, *args, **kwargs):
    for field in self._meta.fields:
      field_name = field.name
      field_value = getattr(self, field_name)
      if field_value == "":
        setattr(self, field_name, None)
    self.updated_by = kwargs.pop('user', None)
    super().save(*args, **kwargs)
    
  class Meta:
    abstract = True

class OrderType(CommonInfo):
  type = models.CharField(verbose_name='Order Type', unique=True, max_length=255, null=False, blank=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_ordertype', )
  
  def __str__(self):
    return self.type
  
  class Meta:
    verbose_name = "Order Type"
    verbose_name_plural = "Order Types"
    ordering = ('created_at', )
    
def custom_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.unique_id, filename)

class Order(CommonInfo):
  unique_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
  order_no = models.CharField('Order Number', unique=True, max_length=255, null=False, blank=False, )
  title = models.CharField('Title', max_length=255, null=False, blank=False, )
  date_published = models.DateField(verbose_name='Date Published', null=False, blank=False, )
  type = models.ForeignKey(OrderType, verbose_name='Order Type', null=True, blank=True, default=None, on_delete=models.RESTRICT, related_name='order_ordertype', )
  attachment = models.FileField('Attachment', upload_to='orders', blank=False, null=False, validators=[FileExtensionValidator(['pdf'])])
  tags = models.TextField('Tags', default=None, null=True, blank=True, )
  is_published = models.BooleanField(verbose_name='Is Published', null=False, blank=False, default=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_order', )
  
  def __str__(self):
    return self.order_no
  
  class Meta:
    verbose_name = "Order "
    verbose_name_plural = "Orders"
    ordering = ('created_at', )

class OrderPersonnel(CommonInfo):
  personnel = models.ForeignKey('personnel.Personnel', verbose_name='Personnel', null=False, blank=False, related_name='orderpersonnel_personnel', on_delete=models.RESTRICT, )
  order = models.ForeignKey(Order, verbose_name='Order', null=False, blank=False, related_name='orderpersonnel_order', on_delete=models.CASCADE, )
  office = models.ForeignKey(Office, verbose_name='New Unit', null=True, blank=True, default=None, related_name='orderpersonnel_office', on_delete=models.RESTRICT, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_orderpersonnel', )
    
  def __str__(self):
    return f'{str(self.personnel)} - {self.office}'
  
  class Meta:
    verbose_name = "Order Personnel"
    verbose_name_plural = "Order Personnel"
    ordering = ('created_at', )
