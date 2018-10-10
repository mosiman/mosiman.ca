# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DtInfractions(models.Model):
    osm_id = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    fine = models.IntegerField(blank=True, null=True)
    loc = models.TextField(blank=True, null=True)
    datetime = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dt_infractions'


class SqliteStat1(models.Model):
    tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
    idx = models.TextField(blank=True, null=True)  # This field type is a guess.
    stat = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sqlite_stat1'


class Streetsegmentinfraction(models.Model):
    osm_id = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    fine = models.IntegerField(blank=True, null=True)
    loc = models.TextField(blank=True, null=True)
    datetime = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'streetsegmentinfraction'


class Streetsegments(models.Model):
    osm_id = models.IntegerField(unique=True, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    slat = models.FloatField(blank=True, null=True)
    nlat = models.FloatField(blank=True, null=True)
    wlng = models.FloatField(blank=True, null=True)
    elng = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'streetsegments'
