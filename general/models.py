from django.db import models
from django.contrib.auth.models import User
import uuid

class CommonInfo(models.Model):
  created_at = models.DateTimeField('Created At', null=False, blank=False, auto_now_add=True, )
  updated_at = models.DateTimeField('Updated At', null=False, blank=False, auto_now=True, )
  
  class Meta:
    abstract = True

class OfficeCategory(CommonInfo):
  CATEGORY_CHOICES = (
    ('Command', 'Command'),
    ('Personal Staff', 'Personal Staff'),
    ('Special Staff', 'Special Staff'),
    ('Coordinating Staff', 'Coordinating Staff'),
    ('AFPWSSUs', 'AFPWSSUs'),
    ('UCs', 'UCs'),
    ('MS', 'MS'),
  )
  category = models.CharField('Office Category', unique=True, max_length=255, null=False, blank=False, choices=CATEGORY_CHOICES, )
  ordering = models.IntegerField(verbose_name='Order', null=False, blank=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_officecategory', )
  
  def __str__(self):
    return self.category
  
  class Meta:
    verbose_name = "Office Category"
    verbose_name_plural = "Office Categories"
    ordering = ('created_at', )

class Office(CommonInfo):
  PROGRAM_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
  )
  office = models.CharField(verbose_name='Office', unique=True, max_length=255, null=False, blank=False, )
  office_name = models.CharField(verbose_name='Office Name', max_length=500, null=True, blank=True, )
  office_category = models.ForeignKey(OfficeCategory, verbose_name='Office Category', null=False, blank=False, related_name='office_category', on_delete=models.RESTRICT, )
  program = models.IntegerField(verbose_name='Program', null=False, blank=False, choices=PROGRAM_CHOICES, )
  parent = models.ForeignKey("self", verbose_name="Parent Unit", default=None, null=True, blank=True, related_name='office_parent', on_delete=models.CASCADE, )
  is_school = models.BooleanField(verbose_name='School', default=False)
  is_medical = models.BooleanField(verbose_name='Medical', default=False)
  is_un = models.BooleanField(verbose_name='UN', default=False)
  is_do = models.BooleanField(verbose_name='DO', default=False)
  is_active = models.BooleanField(verbose_name='Is Active', default=True)
  obi01 = models.IntegerField(verbose_name='O-BI 01', default=0, null=False, blank=False, )
  obi02 = models.IntegerField(verbose_name='O-BI 02', default=0, null=False, blank=False, )
  obi03 = models.IntegerField(verbose_name='O-BI 03', default=0, null=False, blank=False, )
  obi04 = models.IntegerField(verbose_name='O-BI 04', default=0, null=False, blank=False, )
  obi05 = models.IntegerField(verbose_name='O-BI 05', default=0, null=False, blank=False, )
  obi06 = models.IntegerField(verbose_name='O-BI 06', default=0, null=False, blank=False, )
  obi07 = models.IntegerField(verbose_name='O-BI 07', default=0, null=False, blank=False, )
  obi08 = models.IntegerField(verbose_name='O-BI 08', default=0, null=False, blank=False, )
  obi09 = models.IntegerField(verbose_name='O-BI 09', default=0, null=False, blank=False, )
  obi10 = models.IntegerField(verbose_name='O-BI 10', default=0, null=False, blank=False, )
  opa01 = models.IntegerField(verbose_name='O-PA 01', default=0, null=False, blank=False, )
  opa02 = models.IntegerField(verbose_name='O-PA 02', default=0, null=False, blank=False, )
  opa03 = models.IntegerField(verbose_name='O-PA 03', default=0, null=False, blank=False, )
  opa04 = models.IntegerField(verbose_name='O-PA 04', default=0, null=False, blank=False, )
  opa05 = models.IntegerField(verbose_name='O-PA 05', default=0, null=False, blank=False, )
  opa06 = models.IntegerField(verbose_name='O-PA 06', default=0, null=False, blank=False, )
  opa07 = models.IntegerField(verbose_name='O-PA 07', default=0, null=False, blank=False, )
  opa08 = models.IntegerField(verbose_name='O-PA 08', default=0, null=False, blank=False, )
  opa09 = models.IntegerField(verbose_name='O-PA 09', default=0, null=False, blank=False, )
  opa10 = models.IntegerField(verbose_name='O-PA 10', default=0, null=False, blank=False, )
  opaf01 = models.IntegerField(verbose_name='O-PAF 01', default=0, null=False, blank=False, )
  opaf02 = models.IntegerField(verbose_name='O-PAF 02', default=0, null=False, blank=False, )
  opaf03 = models.IntegerField(verbose_name='O-PAF 03', default=0, null=False, blank=False, )
  opaf04 = models.IntegerField(verbose_name='O-PAF 04', default=0, null=False, blank=False, )
  opaf05 = models.IntegerField(verbose_name='O-PAF 05', default=0, null=False, blank=False, )
  opaf06 = models.IntegerField(verbose_name='O-PAF 06', default=0, null=False, blank=False, )
  opaf07 = models.IntegerField(verbose_name='O-PAF 07', default=0, null=False, blank=False, )
  opaf08 = models.IntegerField(verbose_name='O-PAF 08', default=0, null=False, blank=False, )
  opaf09 = models.IntegerField(verbose_name='O-PAF 09', default=0, null=False, blank=False, )
  opaf10 = models.IntegerField(verbose_name='O-PAF 10', default=0, null=False, blank=False, )
  opn01 = models.IntegerField(verbose_name='O-PN 01', default=0, null=False, blank=False, )
  opn02 = models.IntegerField(verbose_name='O-PN 02', default=0, null=False, blank=False, )
  opn03 = models.IntegerField(verbose_name='O-PN 03', default=0, null=False, blank=False, )
  opn04 = models.IntegerField(verbose_name='O-PN 04', default=0, null=False, blank=False, )
  opn05 = models.IntegerField(verbose_name='O-PN 05', default=0, null=False, blank=False, )
  opn06 = models.IntegerField(verbose_name='O-PN 06', default=0, null=False, blank=False, )
  opn07 = models.IntegerField(verbose_name='O-PN 07', default=0, null=False, blank=False, )
  opn08 = models.IntegerField(verbose_name='O-PN 08', default=0, null=False, blank=False, )
  opn09 = models.IntegerField(verbose_name='O-PN 09', default=0, null=False, blank=False, )
  opn10 = models.IntegerField(verbose_name='O-PN 10', default=0, null=False, blank=False, )
  otas01 = models.IntegerField(verbose_name='O-TAS 01', default=0, null=False, blank=False, )
  otas02 = models.IntegerField(verbose_name='O-TAS 02', default=0, null=False, blank=False, )
  otas03 = models.IntegerField(verbose_name='O-TAS 03', default=0, null=False, blank=False, )
  otas04 = models.IntegerField(verbose_name='O-TAS 04', default=0, null=False, blank=False, )
  otas05 = models.IntegerField(verbose_name='O-TAS 05', default=0, null=False, blank=False, )
  otas06 = models.IntegerField(verbose_name='O-TAS 06', default=0, null=False, blank=False, )
  otas07 = models.IntegerField(verbose_name='O-TAS 07', default=0, null=False, blank=False, )
  otas08 = models.IntegerField(verbose_name='O-TAS 08', default=0, null=False, blank=False, )
  otas09 = models.IntegerField(verbose_name='O-TAS 09', default=0, null=False, blank=False, )
  otas10 = models.IntegerField(verbose_name='O-TAS 10', default=0, null=False, blank=False, )
  ebi01 = models.IntegerField(verbose_name='E-BI 01', default=0, null=False, blank=False, )
  ebi02 = models.IntegerField(verbose_name='E-BI 02', default=0, null=False, blank=False, )
  ebi03 = models.IntegerField(verbose_name='E-BI 03', default=0, null=False, blank=False, )
  ebi04 = models.IntegerField(verbose_name='E-BI 04', default=0, null=False, blank=False, )
  ebi05 = models.IntegerField(verbose_name='E-BI 05', default=0, null=False, blank=False, )
  ebi06 = models.IntegerField(verbose_name='E-BI 06', default=0, null=False, blank=False, )
  ebi07 = models.IntegerField(verbose_name='E-BI 07', default=0, null=False, blank=False, )
  ebi08 = models.IntegerField(verbose_name='E-BI 08', default=0, null=False, blank=False, )
  ebi09 = models.IntegerField(verbose_name='E-BI 09', default=0, null=False, blank=False, )
  ebi10 = models.IntegerField(verbose_name='E-BI 10', default=0, null=False, blank=False, )
  epa01 = models.IntegerField(verbose_name='E-PA 01', default=0, null=False, blank=False, )
  epa02 = models.IntegerField(verbose_name='E-PA 02', default=0, null=False, blank=False, )
  epa03 = models.IntegerField(verbose_name='E-PA 03', default=0, null=False, blank=False, )
  epa04 = models.IntegerField(verbose_name='E-PA 04', default=0, null=False, blank=False, )
  epa05 = models.IntegerField(verbose_name='E-PA 05', default=0, null=False, blank=False, )
  epa06 = models.IntegerField(verbose_name='E-PA 06', default=0, null=False, blank=False, )
  epa07 = models.IntegerField(verbose_name='E-PA 07', default=0, null=False, blank=False, )
  epa08 = models.IntegerField(verbose_name='E-PA 08', default=0, null=False, blank=False, )
  epa09 = models.IntegerField(verbose_name='E-PA 09', default=0, null=False, blank=False, )
  epa10 = models.IntegerField(verbose_name='E-PA 10', default=0, null=False, blank=False, )
  epaf01 = models.IntegerField(verbose_name='E-PAF 01', default=0, null=False, blank=False, )
  epaf02 = models.IntegerField(verbose_name='E-PAF 02', default=0, null=False, blank=False, )
  epaf03 = models.IntegerField(verbose_name='E-PAF 03', default=0, null=False, blank=False, )
  epaf04 = models.IntegerField(verbose_name='E-PAF 04', default=0, null=False, blank=False, )
  epaf05 = models.IntegerField(verbose_name='E-PAF 05', default=0, null=False, blank=False, )
  epaf06 = models.IntegerField(verbose_name='E-PAF 06', default=0, null=False, blank=False, )
  epaf07 = models.IntegerField(verbose_name='E-PAF 07', default=0, null=False, blank=False, )
  epaf08 = models.IntegerField(verbose_name='E-PAF 08', default=0, null=False, blank=False, )
  epaf09 = models.IntegerField(verbose_name='E-PAF 09', default=0, null=False, blank=False, )
  epaf10 = models.IntegerField(verbose_name='E-PAF 10', default=0, null=False, blank=False, )
  epn01 = models.IntegerField(verbose_name='E-PN 01', default=0, null=False, blank=False, )
  epn02 = models.IntegerField(verbose_name='E-PN 02', default=0, null=False, blank=False, )
  epn03 = models.IntegerField(verbose_name='E-PN 03', default=0, null=False, blank=False, )
  epn04 = models.IntegerField(verbose_name='E-PN 04', default=0, null=False, blank=False, )
  epn05 = models.IntegerField(verbose_name='E-PN 05', default=0, null=False, blank=False, )
  epn06 = models.IntegerField(verbose_name='E-PN 06', default=0, null=False, blank=False, )
  epn07 = models.IntegerField(verbose_name='E-PN 07', default=0, null=False, blank=False, )
  epn08 = models.IntegerField(verbose_name='E-PN 08', default=0, null=False, blank=False, )
  epn09 = models.IntegerField(verbose_name='E-PN 09', default=0, null=False, blank=False, )
  epn10 = models.IntegerField(verbose_name='E-PN 10', default=0, null=False, blank=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_office', )
  
  def __str__(self):
    return self.office
  
  class Meta:
    verbose_name = "Office"
    verbose_name_plural = "Offices"
    ordering = ('created_at', )

class Rank(CommonInfo):
  TYPE_CHOICES = (
    ('Officer', 'Officer'),
    ('EP', 'EP'),
    ('CHR', 'CHR'),
  )
  rank = models.CharField(verbose_name='Rank', unique=True, max_length=100, null=False, blank=False, )
  rank_full = models.CharField(verbose_name='Rank Name', max_length=255, null=True, blank=True, )  
  grade = models.IntegerField(verbose_name='Grade', null=False, blank=False, )
  type = models.CharField(verbose_name='Type', max_length=255, null=False, blank=False, choices=TYPE_CHOICES, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_rank', )
  
  def __str__(self):
    return self.rank
  
  class Meta:
    verbose_name = "Rank"
    verbose_name_plural = "Ranks"
    ordering = ('created_at', )

class BOS(CommonInfo):
  MS_CHOICES = (
    ('PA', 'PA'),
    ('PN', 'PN'),
    ('PAF', 'PAF'),
    ('TAS', 'TAS'),
    ('CHR', 'CHR'),
  )
  bos = models.CharField(verbose_name='Branch of Service', unique=True, max_length=100, null=False, blank=False, )
  ms = models.CharField(verbose_name='Major Service', max_length=100, choices=MS_CHOICES, null=False, blank=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_bos', )
  
  def __str__(self):
    return self.bos
  
  class Meta:
    verbose_name = "BOS"
    verbose_name_plural = "BOS"
    ordering = ('created_at', )

class Profile(CommonInfo):
  unique_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
  user = models.OneToOneField(User, verbose_name='User ID', on_delete=models.CASCADE, related_name='users_profile')
  picture = models.ImageField('Picture', default='default-profile-user.png', upload_to='pictures', null=True, blank=True, )
  office = models.ForeignKey(Office, verbose_name='Office', default=None, null=True, blank=True, related_name='profile_office', on_delete=models.RESTRICT, )
  rank = models.ForeignKey(Rank, verbose_name='Rank', default=None, null=True, blank=True, related_name='profile_rank', on_delete=models.RESTRICT, )
  bos = models.ForeignKey(BOS, verbose_name='BOS', default=None, null=True, blank=True, related_name='profile_bos', on_delete=models.RESTRICT, )
  sign_name = models.CharField('Name (Sign)', max_length=100, default=None, null=True, blank=True, )
  sign_rank = models.CharField('Rank (Sign)', max_length=100, default=None, null=True, blank=True, )
  sign_designation = models.CharField('Designation (Sign)', max_length=100, default=None, null=True, blank=True, )
  sign = models.ImageField('Signature', default=None, upload_to='signatures', null=True, blank=True, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_profile', )
  
  def __str__(self):
    str = ""
    if self.rank:
      str += self.rank.rank + " "
    if self.user.first_name:
      str += self.user.first_name + " "
    if self.user.last_name:
      str += self.user.last_name + " "
    if self.bos:
      str += self.bos.bos + " "
    if self.rank and self.rank.type == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  def user_level(self):
    if self.user.is_superuser:
      return "Superuser"
    else:
      return self.user.groups.all()[0]
  
  class Meta:
    verbose_name = "Profile"
    verbose_name_plural = "Profiles"
    ordering = ('created_at', )

class Option(CommonInfo):
  app_name = models.CharField('Application Name', max_length=255, default='App Name', null=False, blank=False, )
  app_brand = models.CharField('Application Brand', max_length=100, default='App Brand', null=False, blank=False, )
  app_description = models.TextField('Application Description', default=None, null=True, blank=True, )
  app_logo = models.ImageField('Application Logo', default='logo/default-logo.png', upload_to='logo', null=True, blank=True, )
  theme = models.CharField('Theme', max_length=100, default='dark', null=False, blank=False, )
  theme_color = models.CharField('Theme Color', max_length=100, default='navy', null=False, blank=False, )
  upload_max_size = models.IntegerField('Upload Max Size', default=0, null=False, blank=False, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_option', )
  
  class Meta:
    verbose_name = "Option"
    verbose_name_plural = "Options"
    ordering = ('created_at', )