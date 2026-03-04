from django.db import models
from django.contrib.auth.models import User
from general.models import *
from orders.models import *
import uuid
from django.utils import timezone
from datetime import date

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

class SOA(CommonInfo):
  soa = models.CharField(verbose_name='SOA', unique=True, max_length=255, null=False, blank=False, )
  description = models.CharField(verbose_name='Description', max_length=255, default=None, null=True, blank=True, )
  is_effective = models.BooleanField(verbose_name='Effectiveness', default=False )
  with_unit = models.BooleanField(verbose_name='With Carrying Unit?', default=False )
  reporting = models.BooleanField(verbose_name='Reporting', default=False )
  is_school = models.BooleanField(verbose_name='School', default=False )
  is_medical = models.BooleanField(verbose_name='Medical Facility', default=False )
  is_outside = models.BooleanField(verbose_name='Outside Organization', default=False )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_soa', )
  
  def __str__(self):
    return self.soa
  
  class Meta:
    verbose_name = "Status of Assignment"
    verbose_name_plural = "Status of Assignment"
    ordering = ('created_at', )

class Position(CommonInfo):
  position = models.CharField(verbose_name='Position', unique=True, max_length=255, null=False, blank=False, )
  description = models.CharField(verbose_name='Description', max_length=255, default=None, null=True, blank=True, )
  parenthetical = models.CharField(verbose_name='Parenthetical', max_length=255, default=None, null=True, blank=True, )
  grade = models.IntegerField(verbose_name='Grade', default=None, null=True, blank=True, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_position', )
  
  def __str__(self):
    str = self.position
    if self.parenthetical and self.position != self.parenthetical:
      str += f" ({self.parenthetical})"
    return str
  
  class Meta:
    verbose_name = "CHR Position"
    verbose_name_plural = "CHR Positions"
    ordering = ('created_at', )

class OutsideUnit(CommonInfo):
  CATEGORY_CHOICES = (
    ('Government Agencies/Personalities', 'Government Agencies/Personalities'),
    ('Non-Government Agencies/Personalities', 'Non-Government Agencies/Personalities'),
    ('Department of National Defense', 'Department of National Defense'),
    ('PKOC', 'PKOC'),
  )
  outside_unit = models.CharField(verbose_name='Name', unique=True, max_length=255, null=False, blank=False, )
  category = models.CharField(verbose_name='Category', max_length=255, default=None, null=True, blank=True, choices=CATEGORY_CHOICES, )
  authority = models.CharField('Authority', max_length=255, default=None, null=True, blank=True, )
  auth_officer = models.IntegerField(verbose_name='Authorized Officer', default=None, null=True, blank=True,  )
  auth_ep = models.IntegerField(verbose_name='Authorized EP', default=None, null=True, blank=True,  )
  auth_chr = models.IntegerField(verbose_name='Authorized CHR', default=None, null=True, blank=True,  )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_outsideunit', )
  
  def __str__(self):
    return self.outside_unit
  
  class Meta:
    verbose_name = "Outside Unit"
    verbose_name_plural = "Outside Units"
    ordering = ('created_at', )

def custom_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.unique_id, filename)

class Report(CommonInfo):
  unique_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
  date = models.DateField(verbose_name='Report Date', null=False, blank=False, )
  office = models.ForeignKey(Office, verbose_name='Office/Unit', null=False, blank=False, related_name='report_office', on_delete=models.RESTRICT, )
  created_by = models.ForeignKey(User, verbose_name='Created By', null=True, blank=True, default=None, on_delete=models.RESTRICT, related_name='createdby_user_report', )
  approved_by = models.ForeignKey(User, verbose_name='Approved By', null=True, blank=True, default=None, on_delete=models.RESTRICT, related_name='approvedby_user_report', )
  is_submitted = models.BooleanField(verbose_name='Is Submitted?', default=False, )
  is_approved = models.BooleanField(verbose_name='Is Approved?', default=False, )
  file = models.FileField('Report (Organic)', upload_to=custom_directory_path, default=None, null=True, blank=True, )
  file_ds = models.FileField('Report (DS)', upload_to=custom_directory_path, default=None, null=True, blank=True, )
  file_subunits = models.FileField('Report (Subunits)', upload_to=custom_directory_path, default=None, null=True, blank=True, )
  file_students = models.FileField('Report (Students)', upload_to=custom_directory_path, default=None, null=True, blank=True, )
  file_patients = models.FileField('Report (Patients)', upload_to=custom_directory_path, default=None, null=True, blank=True, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_report', )
  
  def __str__(self):
    return f"{self.office} ({self.date})"
  
  class Meta:
    verbose_name = "Report"
    verbose_name_plural = "Reports"
    ordering = ('created_at', )
    unique_together = ('date', 'office', )

class Personnel(CommonInfo):
  PROFILE_CHOICES = (
    ('Officer', 'Officer'),
    ('EP', 'EP'),
    ('CHR', 'CHR'),
  )
  profile = models.CharField('Profile', max_length=20, null=False, blank=False, choices=PROFILE_CHOICES, )
  rank = models.ForeignKey(Rank, verbose_name='Rank', null=False, blank=False, related_name='personnel_rank', on_delete=models.RESTRICT, )  
  first_name = models.CharField('First Name', max_length=150, null=False, blank=False, )
  middle_name = models.CharField('Middle Name', max_length=100, default=None, null=True, blank=True, )
  last_name = models.CharField('Last Name', max_length=150, null=False, blank=False, )
  ext_name = models.CharField('Extension Name', max_length=100, default=None, null=True, blank=True, )
  afpsn = models.CharField(verbose_name='AFPSN', unique=True, max_length=20, default=None, null=True, blank=True, )
  bos = models.ForeignKey(BOS, verbose_name='BOS', null=False, blank=False, related_name='personnel_bos', on_delete=models.RESTRICT, )
  office = models.ForeignKey(Office, verbose_name='Office/Unit', null=False, blank=False, related_name='personnel_office', on_delete=models.RESTRICT, )
  fos = models.CharField('FOS/MOS', max_length=100, default=None, null=True, blank=True, )
  daghq = models.DateField(verbose_name='DAGHQ', default=None, null=True, blank=True, )
  dapda = models.DateField(verbose_name='DAPDA', default=None, null=True, blank=True, )
  status_assignment = models.ForeignKey(SOA, verbose_name='SOA', default=None, null=True, blank=True, related_name='personnel_soa', on_delete=models.RESTRICT, )
  rrfcd = models.CharField('RRFCD', max_length=255, default=None, null=True, blank=True, )
  desig = models.CharField('Designation', max_length=255, default=None, null=True, blank=True, )
  position = models.ForeignKey(Position, verbose_name='Position Title', default=None, null=True, blank=True, related_name='personnel_position', on_delete=models.RESTRICT, )
  item_no = models.CharField('Plantilla Item No', unique=True, max_length=255, default=None, null=True, blank=True, )
  skills = models.CharField('Skills', max_length=255, default=None, null=True, blank=True, )
  dot = models.DateField(verbose_name='DOT', default=None, null=True, blank=True, )
  doc = models.DateField(verbose_name='DOC', default=None, null=True, blank=True, )
  dob = models.DateField(verbose_name='DOB', null=False, blank=False, )
  dolp = models.DateField(verbose_name='DOLP', default=None, null=True, blank=True, )
  hcc = models.CharField('HCC', max_length=255, default=None, null=True, blank=True, )
  soc = models.CharField('SOC', max_length=255, default=None, null=True, blank=True, )
  doret = models.DateField(verbose_name='DORET', default=None, null=True, blank=True, )  
  SEX_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = models.CharField(verbose_name='Sex', max_length=2, choices=SEX_CHOICES, null=False, blank=False, )
  auth = models.CharField('AUTH', max_length=255, default=None, null=True, blank=True, )
  act = models.CharField('ACT', max_length=255, default=None, null=True, blank=True, )
  vacant = models.CharField('Vacant', max_length=255, default=None, null=True, blank=True, )
  cti = models.CharField('CTI', max_length=255, default=None, null=True, blank=True, )
  remarks = models.TextField('Remarks', default=None, null=True, blank=True, )
  ds_unit = models.ForeignKey(Office, verbose_name='Temporary Unit', default=None, null=True, blank=True, related_name='personnel_ds_unit', on_delete=models.RESTRICT, )
  outside_unit = models.ForeignKey(OutsideUnit, verbose_name='Outside Unit', default=None, null=True, blank=True, related_name='personnel_outsideunit', on_delete=models.RESTRICT, )
  is_active = models.BooleanField(verbose_name='Is Active?', default=True )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_personnel', )
  
  # FIELDS_TO_CHECK = ["office", "ds_unit", "status_assignment"]
  
  def __str__(self):
    str = ""
    if self.rank:
      str += self.rank.rank + " "
    if self.first_name:
      str += self.first_name + " "
    if self.middle_name:
      initials = ''.join(name[0].upper() for name in self.middle_name.split())
      str += initials + " "
    if self.last_name:
      str += self.last_name + " "
    if self.ext_name:
      str += self.ext_name + " "
    if self.bos:
      str += self.bos.bos + " "
    if self.rank and self.rank.type == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  @property
  def age(self):
    if self.dob:
      today = date.today()
      dob = self.dob
      
      age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
      return age
    return None
  
  @property
  def doret2(self):  
    if not self.dob or self.bos is None or self.profile == 'CHR':
      return None
    bos = self.bos.bos
    retirement_age = 60 if any(str(bos).startswith(pref) for pref in ('MC', 'JAGS', 'CHS', 'PROF', )) else 57
    try:
      return self.dob.replace(year=self.dob.year + retirement_age)
    except ValueError:
      return date(self.dob.year + retirement_age, 2, 28)
  
  @property
  def length_service(self):
    if self.doc:
      today = date.today()
      doc = self.doc
      
      length_service = today.year - doc.year - ((today.month, today.day) < (doc.month, doc.day))
      return length_service
    return None
  
  def get_orders(self):
    return OrderPersonnel.objects.filter(personnel=self).order_by('-updated_at')
    
  class Meta:
    verbose_name = "Personnel"
    verbose_name_plural = "Personnel"
    ordering = ('created_at', )    
    unique_together = ('first_name', 'last_name', 'dob', )

class PersonnelHist(CommonInfo):
  report = models.ForeignKey(Report, verbose_name='Report', null=False, blank=False, related_name='personnelhist_report', on_delete=models.CASCADE, )
  id_pers = models.PositiveBigIntegerField()
  profile = models.CharField('Profile', max_length=20, null=False, blank=False, )
  rank = models.CharField('Rank', max_length=100, null=False, blank=False, )
  first_name = models.CharField('First Name', max_length=150, null=False, blank=False, )
  middle_name = models.CharField('Middle Name', max_length=100, default=None, null=True, blank=True, )
  last_name = models.CharField('Last Name', max_length=150, null=False, blank=False, )
  ext_name = models.CharField('Extension Name', max_length=100, default=None, null=True, blank=True, )
  afpsn = models.CharField(verbose_name='AFPSN', max_length=20, default=None, null=True, blank=True, )
  bos = models.CharField('BOS', max_length=100, null=False, blank=False, )
  office = models.CharField('Office/Unit', max_length=255, null=False, blank=False, )
  fos = models.CharField('FOS/MOS', max_length=100, default=None, null=True, blank=True, )
  daghq = models.DateField(verbose_name='DAGHQ', default=None, null=True, blank=True, )
  dapda = models.DateField(verbose_name='DAPDA', default=None, null=True, blank=True, )
  status_assignment = models.CharField('SOA', max_length=255, default=None, null=True, blank=True, )
  rrfcd = models.CharField('RRFCD', max_length=255, default=None, null=True, blank=True, )
  desig = models.CharField('Designation', max_length=255, default=None, null=True, blank=True, )
  position = models.CharField('Position Title', max_length=255, default=None, null=True, blank=True, )
  item_no = models.CharField('Plantilla Item No', max_length=255, default=None, null=True, blank=True, )
  skills = models.CharField('Skills', max_length=255, default=None, null=True, blank=True, )
  dot = models.DateField(verbose_name='DOT', default=None, null=True, blank=True, )
  doc = models.DateField(verbose_name='DOC', default=None, null=True, blank=True, )
  dob = models.DateField(verbose_name='DOB', null=False, blank=False, )
  dolp = models.DateField(verbose_name='DOLP', default=None, null=True, blank=True, )
  hcc = models.CharField('HCC', max_length=255, default=None, null=True, blank=True, )
  soc = models.CharField('SOC', max_length=255, default=None, null=True, blank=True, )
  doret = models.DateField(verbose_name='DORET', default=None, null=True, blank=True, )  
  SEX_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = models.CharField(verbose_name='Sex', max_length=2, choices=SEX_CHOICES, null=False, blank=False, )
  auth = models.CharField('AUTH', max_length=255, default=None, null=True, blank=True, )
  act = models.CharField('ACT', max_length=255, default=None, null=True, blank=True, )
  vacant = models.CharField('Vacant', max_length=255, default=None, null=True, blank=True, )
  cti = models.CharField('CTI', max_length=255, default=None, null=True, blank=True, )
  remarks = models.TextField('Remarks', default=None, null=True, blank=True, )
  ds_unit = models.CharField('Temporary Unit', max_length=255, default=None, null=True, blank=True, )
  outside_unit = models.CharField('Outside Unit', max_length=255, default=None, null=True, blank=True, )
  is_active = models.BooleanField(verbose_name='Is Active?', default=True )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_personnelhist', )
  
  def __str__(self):
    str = ""
    if self.rank:
      str += self.rank + " "
    if self.first_name:
      str += self.first_name + " "
    if self.middle_name:
      initials = ''.join(name[0].upper() for name in self.middle_name.split())
      str += initials + " "
    if self.last_name:
      str += self.last_name + " "
    if self.ext_name:
      str += self.ext_name + " "
    if self.bos:
      str += self.bos + " "
    if self.rank and self.profile == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  class Meta:
    verbose_name = "Personnel History"
    verbose_name_plural = "Personnel History"
    ordering = ('created_at', )

class Student(CommonInfo):  
  personnel = models.OneToOneField(Personnel, verbose_name='Personnel', related_name='student_personnel', on_delete=models.CASCADE, )
  office = models.ForeignKey(Office, verbose_name='Office/Unit', null=False, blank=False, related_name='student_office', on_delete=models.RESTRICT, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_student', )
  
  def __str__(self):
    str = ""
    if self.personnel.rank:
      str += self.personnel.rank.rank + " "
    if self.personnel.first_name:
      str += self.personnel.first_name + " "
    if self.personnel.middle_name:
      initials = ''.join(name[0].upper() for name in self.personnel.middle_name.split())
      str += initials + " "
    if self.personnel.last_name:
      str += self.personnel.last_name + " "
    if self.personnel.ext_name:
      str += self.personnel.ext_name + " "
    if self.personnel.bos:
      str += self.personnel.bos.bos + " "
    if self.personnel.rank and self.personnel.rank.type == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  class Meta:
    verbose_name = "Student"
    verbose_name_plural = "Students"
    ordering = ('created_at', )

class StudentHist(CommonInfo):
  report = models.ForeignKey(Report, verbose_name='Report', null=False, blank=False, related_name='studenthist_report', on_delete=models.CASCADE, )
  id_pers = models.PositiveBigIntegerField()
  profile = models.CharField('Profile', max_length=20, null=False, blank=False, )
  rank = models.CharField('Rank', max_length=100, null=False, blank=False, )
  first_name = models.CharField('First Name', max_length=150, null=False, blank=False, )
  middle_name = models.CharField('Middle Name', max_length=100, default=None, null=True, blank=True, )
  last_name = models.CharField('Last Name', max_length=150, null=False, blank=False, )
  ext_name = models.CharField('Extension Name', max_length=100, default=None, null=True, blank=True, )
  afpsn = models.CharField(verbose_name='AFPSN', max_length=20, default=None, null=True, blank=True, )
  bos = models.CharField('BOS', max_length=100, null=False, blank=False, )
  office = models.CharField('Office/Unit', max_length=255, null=False, blank=False, )
  fos = models.CharField('FOS/MOS', max_length=100, default=None, null=True, blank=True, )
  daghq = models.DateField(verbose_name='DAGHQ', default=None, null=True, blank=True, )
  dapda = models.DateField(verbose_name='DAPDA', default=None, null=True, blank=True, )
  status_assignment = models.CharField('SOA', max_length=255, default=None, null=True, blank=True, )
  rrfcd = models.CharField('RRFCD', max_length=255, default=None, null=True, blank=True, )
  desig = models.CharField('Designation', max_length=255, default=None, null=True, blank=True, )
  position = models.CharField('Position Title', max_length=255, default=None, null=True, blank=True, )
  item_no = models.CharField('Plantilla Item No', max_length=255, default=None, null=True, blank=True, )
  skills = models.CharField('Skills', max_length=255, default=None, null=True, blank=True, )
  dot = models.DateField(verbose_name='DOT', default=None, null=True, blank=True, )
  doc = models.DateField(verbose_name='DOC', default=None, null=True, blank=True, )
  dob = models.DateField(verbose_name='DOB', null=False, blank=False, )
  dolp = models.DateField(verbose_name='DOLP', default=None, null=True, blank=True, )
  hcc = models.CharField('HCC', max_length=255, default=None, null=True, blank=True, )
  soc = models.CharField('SOC', max_length=255, default=None, null=True, blank=True, )
  doret = models.DateField(verbose_name='DORET', default=None, null=True, blank=True, )  
  SEX_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = models.CharField(verbose_name='Sex', max_length=2, choices=SEX_CHOICES, null=False, blank=False, )
  auth = models.CharField('AUTH', max_length=255, default=None, null=True, blank=True, )
  act = models.CharField('ACT', max_length=255, default=None, null=True, blank=True, )
  vacant = models.CharField('Vacant', max_length=255, default=None, null=True, blank=True, )
  cti = models.CharField('CTI', max_length=255, default=None, null=True, blank=True, )
  remarks = models.TextField('Remarks', default=None, null=True, blank=True, )
  ds_unit = models.CharField('Temporary Unit', max_length=255, default=None, null=True, blank=True, )
  outside_unit = models.CharField('Outside Unit', max_length=255, default=None, null=True, blank=True, )
  is_active = models.BooleanField(verbose_name='Is Active?', default=True )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_studenthis', )
  
  def __str__(self):
    str = ""
    if self.rank:
      str += self.rank + " "
    if self.first_name:
      str += self.first_name + " "
    if self.middle_name:
      initials = ''.join(name[0].upper() for name in self.middle_name.split())
      str += initials + " "
    if self.last_name:
      str += self.last_name + " "
    if self.ext_name:
      str += self.ext_name + " "
    if self.bos:
      str += self.bos + " "
    if self.rank and self.profile == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  class Meta:
    verbose_name = "Student History"
    verbose_name_plural = "Student History"
    ordering = ('created_at', )

class Patient(CommonInfo):  
  personnel = models.OneToOneField(Personnel, verbose_name='Personnel', related_name='patienthist_personnel', on_delete=models.CASCADE, )
  office = models.ForeignKey(Office, verbose_name='Office/Unit', null=False, blank=False, related_name='patient_office', on_delete=models.RESTRICT, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_patient', )
  
  def __str__(self):
    str = ""
    if self.personnel.rank:
      str += self.personnel.rank.rank + " "
    if self.personnel.first_name:
      str += self.personnel.first_name + " "
    if self.personnel.middle_name:
      initials = ''.join(name[0].upper() for name in self.personnel.middle_name.split())
      str += initials + " "
    if self.personnel.last_name:
      str += self.personnel.last_name + " "
    if self.personnel.ext_name:
      str += self.personnel.ext_name + " "
    if self.personnel.bos:
      str += self.personnel.bos.bos + " "
    if self.personnel.rank and self.personnel.rank.type == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  class Meta:
    verbose_name = "Patient"
    verbose_name_plural = "Patients"
    ordering = ('created_at', )

class PatientHist(CommonInfo):
  report = models.ForeignKey(Report, verbose_name='Report', null=False, blank=False, related_name='patienthist_report', on_delete=models.CASCADE, )
  id_pers = models.PositiveBigIntegerField()
  profile = models.CharField('Profile', max_length=20, null=False, blank=False, )
  rank = models.CharField('Rank', max_length=100, null=False, blank=False, )
  first_name = models.CharField('First Name', max_length=150, null=False, blank=False, )
  middle_name = models.CharField('Middle Name', max_length=100, default=None, null=True, blank=True, )
  last_name = models.CharField('Last Name', max_length=150, null=False, blank=False, )
  ext_name = models.CharField('Extension Name', max_length=100, default=None, null=True, blank=True, )
  afpsn = models.CharField(verbose_name='AFPSN', max_length=20, default=None, null=True, blank=True, )
  bos = models.CharField('BOS', max_length=100, null=False, blank=False, )
  office = models.CharField('Office/Unit', max_length=255, null=False, blank=False, )
  fos = models.CharField('FOS/MOS', max_length=100, default=None, null=True, blank=True, )
  daghq = models.DateField(verbose_name='DAGHQ', default=None, null=True, blank=True, )
  dapda = models.DateField(verbose_name='DAPDA', default=None, null=True, blank=True, )
  status_assignment = models.CharField('SOA', max_length=255, default=None, null=True, blank=True, )
  rrfcd = models.CharField('RRFCD', max_length=255, default=None, null=True, blank=True, )
  desig = models.CharField('Designation', max_length=255, default=None, null=True, blank=True, )
  position = models.CharField('Position Title', max_length=255, default=None, null=True, blank=True, )
  item_no = models.CharField('Plantilla Item No', max_length=255, default=None, null=True, blank=True, )
  skills = models.CharField('Skills', max_length=255, default=None, null=True, blank=True, )
  dot = models.DateField(verbose_name='DOT', default=None, null=True, blank=True, )
  doc = models.DateField(verbose_name='DOC', default=None, null=True, blank=True, )
  dob = models.DateField(verbose_name='DOB', null=False, blank=False, )
  dolp = models.DateField(verbose_name='DOLP', default=None, null=True, blank=True, )
  hcc = models.CharField('HCC', max_length=255, default=None, null=True, blank=True, )
  soc = models.CharField('SOC', max_length=255, default=None, null=True, blank=True, )
  doret = models.DateField(verbose_name='DORET', default=None, null=True, blank=True, )  
  SEX_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
  )
  sex = models.CharField(verbose_name='Sex', max_length=2, choices=SEX_CHOICES, null=False, blank=False, )
  auth = models.CharField('AUTH', max_length=255, default=None, null=True, blank=True, )
  act = models.CharField('ACT', max_length=255, default=None, null=True, blank=True, )
  vacant = models.CharField('Vacant', max_length=255, default=None, null=True, blank=True, )
  cti = models.CharField('CTI', max_length=255, default=None, null=True, blank=True, )
  remarks = models.TextField('Remarks', default=None, null=True, blank=True, )
  ds_unit = models.CharField('Temporary Unit', max_length=255, default=None, null=True, blank=True, )
  outside_unit = models.CharField('Outside Unit', max_length=255, default=None, null=True, blank=True, )
  is_active = models.BooleanField(verbose_name='Is Active?', default=True )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_patienthis', )
  
  def __str__(self):
    str = ""
    if self.rank:
      str += self.rank + " "
    if self.first_name:
      str += self.first_name + " "
    if self.middle_name:
      initials = ''.join(name[0].upper() for name in self.middle_name.split())
      str += initials + " "
    if self.last_name:
      str += self.last_name + " "
    if self.ext_name:
      str += self.ext_name + " "
    if self.bos:
      str += self.bos + " "
    if self.rank and self.profile == "Officer":
      str = str.upper()
    return f"{str.strip()}"
  
  class Meta:
    verbose_name = "Patient History"
    verbose_name_plural = "Patient History"
    ordering = ('created_at', )

class ReportComment(CommonInfo):
  report = models.ForeignKey(Report, verbose_name='Report', null=False, blank=False, related_name='reportcomment_report', on_delete=models.CASCADE, )
  comment = models.TextField('Comment', null=False, blank=False, )
  is_active = models.BooleanField(verbose_name='Is Active?', default=True, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_reportcomment', )
  
  def __str__(self):
    return f"{self.report} ({self.comment[:30]}...)"
  
  class Meta:
    verbose_name = "Report Comment"
    verbose_name_plural = "Report Comments"
    ordering = ('created_at', )

class PersonnelMovement(models.Model):  
  created_at = models.DateTimeField('Created At', null=False, blank=False, auto_now_add=True, )
  updated_at = models.DateTimeField('Updated At', null=False, blank=False, auto_now=True, )
  personnel = models.ForeignKey(Personnel, verbose_name='Personnel', null=False, blank=False, related_name='personnel_movement', on_delete=models.CASCADE, )
  date = models.DateTimeField(verbose_name='Date', null=False, blank=False, )
  soa1 = models.ForeignKey(SOA, verbose_name='Old SOA', null=True, blank=True, default=None, related_name='personnelmovement_soa_old', on_delete=models.RESTRICT, )
  office1 = models.ForeignKey(Office, verbose_name='Old Office/Unit', null=True, blank=True, default=None, related_name='personnelmovement_office_old', on_delete=models.RESTRICT, )
  temp_office1 = models.ForeignKey(Office, verbose_name='Old Temp Office/Unit', null=True, blank=True, default=None, related_name='personnelmovement_temp_office_old', on_delete=models.RESTRICT, )
  soa2 = models.ForeignKey(SOA, verbose_name='New SOA', null=True, blank=True, default=None, related_name='personnelmovement_soa_new', on_delete=models.RESTRICT, )
  office2 = models.ForeignKey(Office, verbose_name='New Office/Unit', null=True, blank=True, default=None, related_name='personnelmovement_office_new', on_delete=models.RESTRICT, )
  temp_office2 = models.ForeignKey(Office, verbose_name='New Temp Office/Unit', null=True, blank=True, default=None, related_name='personnelmovement_temp_office_new', on_delete=models.RESTRICT, )
  updated_by = models.ForeignKey(User, verbose_name='Updated By', null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='updatedby_user_personnelmovement', )
  
  def __str__(self):
    return f"{self.personnel} from [{self.office1} ({self.soa1})] to [{self.office2} ({self.soa2})]"
  
  class Meta:
    verbose_name = "Personnel Movement"
    verbose_name_plural = "Personnel Movements"
    ordering = ('created_at', )