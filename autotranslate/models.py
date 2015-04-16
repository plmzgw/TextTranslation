#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class UploadFile(models.Model):
    filename = models.CharField(max_length=50L,null=True)
    file = models.FileField(upload_to = 'uploadfiles/%Y%m%d')
    upload_time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __unicode__(self):
        return self.filename
    
class TranslatedFile(models.Model):
    filename = models.CharField(max_length=50L,null=True)
    trans_lang = models.CharField(max_length=30L,null=True)
    path = models.CharField(max_length=100L,null=True)
    trans_time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __unicode__(self):
        return u'%s %s' %(self.filename, self.path)
    
class Language(models.Model):
    language=models.CharField(max_length=50L, null=True)
    language_chinese = models.CharField(max_length=50L, null=True)
    language_code = models.CharField(max_length=30L, null=True)
    
    def __unicode__(self):
        return u'%s %s %s' %(self.language, self.language_chinese, self.language_code)
