import csv
from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from five import grok
from plone.app.event.base import default_timezone
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from plone.namedfile.field import NamedFile
from z3c.form import field
from z3c.form.button import buttonAndHandler

from seantis.dir.base.fieldmap import get_map
from seantis.dir.base.xlsimport import add_defaults
from seantis.dir.events.interfaces import IEventsDirectory


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


class IImportDirectorySchema(form.Schema):
    """ Define fields used on the form """
    csv_file = NamedFile(title=u"CSV file")


class Import(form.Form):
    label = u'Import events from existing Zug events directory'
    fields = field.Fields(IImportDirectorySchema)

    grok.context(IEventsDirectory)
    grok.require('cmf.ManagePortal')
    grok.name('import_zug')

    ignoreContext = True

    @buttonAndHandler(u'Import', name='import')
    def import_csv(self, action):

        # Extract form field values and errors from HTTP request
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Delete all existing events
        self.context.manage_delObjects(self.context.objectIds())

        workflow_tool = getToolByName(self.context, 'portal_workflow')
        fieldmap = get_map(self.context)

        io = StringIO(data['csv_file'].data)
        reader = unicode_csv_reader(io, delimiter=';', quotechar='"')

        # Skip header line
        reader.next()
        counter = 0
        for row in reader:

            # The key does not exist, create a new object
            attributes = dict()
            for attr, ix in fieldmap.fieldmap.items():
                if not attr in fieldmap.readonly:
                    value = row[ix]
                    unwrapped = fieldmap.get_unwrapper(ix=ix)(value)
                    attributes[attr] = unwrapped

            # Unmapped fields are filled with defaults
            add_defaults(attributes, fieldmap)

            # TODO:
            # We cannot properly decode the coordinates (because of nested ").
            attributes['coordinates_json'] = None

            attributes['timezone'] = default_timezone()

            event = createContentInContainer(
                self.context, fieldmap.typename, **attributes
            )

            workflow_tool.doActionFor(event, 'submit')
            workflow_tool.doActionFor(event, 'publish')
            counter += 1

        self.status = u'Imported %s events' % counter
