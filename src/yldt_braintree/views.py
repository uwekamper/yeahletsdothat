#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def bla(request):
    return HttpResponse('Balbub')