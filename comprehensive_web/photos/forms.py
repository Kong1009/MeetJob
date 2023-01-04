# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 18:32:42 2023

@author: DCT
"""

from django import forms
from .models import Photo

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', )
        widgets = {
            'images': forms.FileInput(attrs={'class': 'form-control-file'})
            }