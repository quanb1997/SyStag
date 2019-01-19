from __future__ import unicode_literals
from django.db import models

# from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser

from backend.managers import SystagUserManager

# Tristan: these are for the usergroup admin field
MEMBER = 0
ADMIN = 1
OWNER = 2
MYSYSTEMS = 3


# system model
class System(models.Model):
    serialnumber = models.IntegerField(db_column='serialNumber', primary_key=True)
    companyname = models.TextField(db_column='companyName', blank=True, null=True)
    systemname = models.TextField(db_column='systemName', blank=True, null=True)
    productfamily = models.IntegerField(db_column='productFamily', blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    osversion = models.TextField(db_column='osVersion', blank=True, null=True)
    patches = models.TextField(blank=True, null=True)
    cpgcount = models.IntegerField(db_column='cpgCount', blank=True, null=True)
    recommended_osversion = models.TextField(db_column='recommended.osVersion', blank=True,
        null=True)
    location_region = models.TextField(db_column='location.region', blank=True, null=True)
    location_country = models.TextField(db_column='location.country', blank=True,
        null=True)
    installdate = models.TextField(db_column='installDate', blank=True, null=True)
    updated = models.TextField(blank=True, null=True)
    capacity_total_freepct = models.FloatField(db_column='capacity.total.freePct',
        blank=True, null=True)
    capacity_total_freetib = models.FloatField(db_column='capacity.total.freeTiB',
        blank=True, null=True)
    capacity_total_sizetib = models.FloatField(db_column='capacity.total.sizeTiB',
        blank=True, null=True)
    capacity_total_deduperatio = models.TextField(db_column='capacity.total.dedupeRatio',
        blank=True, null=True)
    nodes_nodecount = models.IntegerField(db_column='nodes.nodeCount', blank=True,
        null=True)
    nodes_nodecountoffline = models.IntegerField(db_column='nodes.nodeCountOffline',
        blank=True, null=True)
    disks_total_diskcount = models.IntegerField(db_column='disks.total.diskCount',
        blank=True, null=True)
    disks_total_diskcountnormal = \
        models.IntegerField(db_column='disks.total.diskCountNormal',blank=True, null=True)
    disks_total_diskcountdegraded = \
        models.TextField(db_column='disks.total.diskCountDegraded', blank=True, null=True)
    disks_total_diskcountfailed = models.TextField(db_column='disks.total.diskCountFailed',
        blank=True, null=True)
    contractstartdate = models.TextField(db_column='contractStartDate', blank=True,
        null=True)
    contractenddate = models.TextField(db_column='contractEndDate', blank=True, null=True)
    batteryexpiry = models.TextField(db_column='batteryExpiry', blank=True, null=True)
    sp_spversion = models.TextField(db_column='sp.spVersion', blank=True, null=True)
    vvcount = models.IntegerField(db_column='vvCount', blank=True, null=True)
    tpvvcount = models.IntegerField(db_column='tpvvCount', blank=True, null=True)
    vvcountfull = models.IntegerField(db_column='vvCountFull', blank=True, null=True)
    tdvvsizetib = models.TextField(db_column='tdvvSizeTiB', blank=True, null=True)
    performance_portbandwidthdata_total_dataratekbpsavg = \
        models.FloatField(db_column='performance.portBandwidthData.total.dataRateKBPSAvg',
            blank=True, null=True)
    performance_portbandwidthdata_total_iopsavg = \
        models.IntegerField(db_column='performance.portBandwidthData.total.iopsAvg', blank=True,
            null=True)
    performance_portbandwidthdata_total_iopsmax = \
        models.FloatField(db_column='performance.portBandwidthData.total.iopsMax',
            blank=True,null=True)
    performance_summary_portinfo_totalservicetimemillis = \
        models.FloatField(db_column='performance.summary.portInfo.totalServiceTimeMillis',
            blank=True, null=True)
    performance_summary_portinfo_readservicetimemillis = \
        models.FloatField(db_column='performance.summary.portInfo.readServiceTimeMillis',
            blank=True, null=True)
    performance_summary_portinfo_writeservicetimemillis = \
        models.FloatField(db_column='performance.summary.portInfo.writeServiceTimeMillis',
            blank=True, null=True)
    performance_summary_delackpct = \
        models.TextField(db_column='performance.summary.delAckPct',blank=True, null=True)
    performance_summary_vvinfo_vvsbytype_ssd_readbandwidthmbps = \
        models.TextField(db_column= \
            'performance.summary.vvInfo.vvsByType.ssd.readBandwidthMBPS',
            blank=True, null=True)
    performance_summary_vvinfo_vvsbytype_ssd_writebandwidthmbps = \
        models.TextField(db_column= \
            'performance.summary.vvInfo.vvsByType.ssd.writeBandwidthMBPS',
            blank=True, null=True)
    performance_summary_vvinfo_vvsbytype_ssd_readservicetimemillis = \
        models.TextField(db_column= \
            'performance.summary.vvInfo.vvsByType.ssd.readServiceTimeMillis',
            blank=True, null=True)
    performance_summary_vvinfo_vvsbytype_ssd_writeservicetimemillis = \
        models.TextField(db_column= \
            'performance.summary.vvInfo.vvsByType.ssd.writeServiceTimeMillis',
            blank=True, null=True)
    nodes_cpuavgmax = models.IntegerField(db_column='nodes.cpuAvgMax',
        blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'db'


# Tristan: user class, extends django's abstract base user class
class User(AbstractBaseUser):
    userid = models.AutoField(db_column='UserID', primary_key=True)
    username = models.CharField(db_column='Username', max_length=45, unique=True)
    password = models.CharField(db_column='Password', max_length=45)
    last_login = models.DateTimeField(db_column='Dateoflogin', blank=True, null=True)
    objects = SystagUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = ''
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'users'


# Tristan: group class
class Group(models.Model):
    groupid = models.AutoField(db_column='GroupID', primary_key=True)
    groupname = models.CharField(db_column='GroupName', max_length=45)
    users = models.ManyToManyField(get_user_model(), through='GroupUsers',
        related_name='groups')
    systems = models.ManyToManyField(System, through='GroupSystems', related_name='groups')

    class Meta:
        managed = False
        db_table = 'groups'


# Tristan: tag class
class Tag(models.Model):
    tagid = models.AutoField(db_column='TagID', primary_key=True)
    tagname = models.CharField(db_column='TagName', max_length=45)
    public = models.IntegerField(db_column='Public', blank=True, null=True)
    systems = models.ManyToManyField(System, through='TagRelations', related_name='tags')
    groups = models.ManyToManyField(Group, through='TagRelations', related_name='tags')
    users = models.ManyToManyField(get_user_model(), through='TagRelations',
        related_name='tags')

    class Meta:
        managed = False
        db_table = 'tags'


# Tristan: tag relations class
class TagRelations(models.Model):
    generalmanagerid = models.AutoField(db_column='GeneralManagerID', primary_key=True)
    userid = models.ForeignKey(get_user_model(), db_column='UserID', 
        on_delete=models.CASCADE, related_name='tag_rel')
    groupid = models.ForeignKey(Group, db_column='GroupID',
        on_delete=models.CASCADE, related_name='tag_rel')
    serialnumber = models.ForeignKey(System, db_column='serialNumber',
        on_delete=models.CASCADE, related_name='tag_rel')
    tagid = models.ForeignKey(Tag, db_column='TagID',
        on_delete=models.CASCADE, related_name='tag_rel')

    class Meta:
        managed = False
        db_table = 'generalmanagement'


# Tristan: group and user relations class
class GroupUsers(models.Model):
    groupmanagementid = models.AutoField(db_column='GroupSystemID', primary_key=True)
    userid = models.ForeignKey(get_user_model(), db_column='UserID',
        on_delete=models.CASCADE, related_name='groupusers')
    groupid = models.ForeignKey(Group, db_column='GroupID', on_delete=models.CASCADE,
        related_name='groupusers')
    # 0: no privileges; 1: add/remove priviliges; 2: owner; 3: mysystems
    admin = models.IntegerField(db_column='AdminID',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupsystem'


# Tristan: group and system relations class
class GroupSystems(models.Model):
    groupsystemsid = models.AutoField(db_column='GroupManagementID', primary_key=True)
    serialnumber = models.ForeignKey(System, db_column='serialNumber',
        on_delete=models.CASCADE, related_name='groupsystems')
    groupid = models.ForeignKey(Group, db_column='GroupID', on_delete=models.CASCADE,
        related_name='groupsystems')

    class Meta:
        managed = False
        db_table = 'groupmanagement'


# Tristan: don't know what this does, but it was in the database
class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'