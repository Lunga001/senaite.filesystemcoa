# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from DateTime import DateTime
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import t
from bika.lims import logger
from bika.lims.subscribers import skip
from bika.lims.subscribers import doActionFor
from plone import api
import os

from bika.lims.browser import ulocalized_time

def AfterTransitionEventHandler(instance, event):

    if instance.portal_type != "AnalysisRequest":
        return

    state = api.content.get_state(instance)
    if state != "published":
        return

    folder = instance.bika_setup.COAFolder
    if len(folder) != 0:
        reports = instance.listFolderContents(
                                    contentFilter={'portal_type':'ARReport'})
        report = sorted(reports, key=lambda k: k.creation_date,reverse=True)
        report = report[0]
        pdf = report.getPdf()
        pdf_fn = pdf.filename
        csv = None
        if hasattr(report, 'CSV'):
            csv = report.CSV
            csv_fn = csv.filename

        client_path = '{}/{}/'.format(folder, instance.getClientID())
        if not os.path.exists(client_path):
            os.makedirs(client_path)

        today = ulocalized_time(DateTime(),
                                long_format=0,
                                context=instance)
        today_path = '{}{}/'.format(client_path, today)
        if not os.path.exists(today_path):
            os.makedirs(today_path)

        fname = '{}{}'.format(today_path, pdf_fn)
        f = open(fname, 'w')
        f.write(pdf.data)
        f.close()

        if csv:
            csvname = '{}{}'.format(today_path, csv_fn)
            fcsv = open(csvname, 'w')
            fcsv.write(csv.data)
            fcsv.close()
