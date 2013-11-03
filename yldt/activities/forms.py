#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

import models


class NewActivityForm(forms.ModelForm):
    class Meta:
        model = models.Activity