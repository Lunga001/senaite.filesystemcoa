from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.content.bikasetup import BikaSetup
from bika.lims.fields import ExtStringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.public import *
from zope.component import adapts
from zope.interface import implements


class COAFolderField(ExtStringField):
    """
    """


class BikaSetupSchemaExtender(object):
    adapts(BikaSetup)
    implements(IOrderableSchemaExtender)

    fields = [
        COAFolderField(
            'COAFolder', 
           schemata="Results Reports",
            widget=StringWidget(
                label=_("COA Folder"),
                description=_("The folder on the filesystem where the COAs"
                            "will reside")
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
