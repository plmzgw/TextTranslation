#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class UploadFileForm(forms.Form):
    myfile = forms.FileField(label='选择文件')