from decimal import Decimal
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from collective.geo.settings.interfaces import IGeoSettings
from izug.seantis.dir.events.guard import groups


def setup_geo(site):
    registry = getUtility(IRegistry)

    # note, the weird way lists below are used is due to the fact that
    # they break if they are replaced, so all updates must be in-place
    # it's probably due to the settings being proxied

    # setup the types
    geo_settings = registry.forInterface(IGeoSettings)

    types = ('seantis.dir.events.directory', 'seantis.dir.events.item')
    for t in types:
        if t not in geo_settings.geo_content_types:
            geo_settings.geo_content_types.append(t)

    # setup the default map layers, removing the old ones first
    # (we need a copy for that)
    to_remove = [l for l in geo_settings.default_layers]
    for layer in to_remove:
        geo_settings.default_layers.remove(layer)

    layers = ('zugmap_orthofotoplus', 'zugmap_ortsplan', 'osm')
    for layer in layers:
        if layer not in geo_settings.default_layers:
            geo_settings.default_layers.append(layer)

    # set the location to Zug (a bit off for better zug map display)
    geo_settings.longitude = Decimal("8.534453365231585")
    geo_settings.latitude = Decimal("47.164210081887184")
    geo_settings.zoom = Decimal("11")


def setup_groups(site):

    group_tool = getToolByName(site, 'portal_groups')
    existing_groups = group_tool.listGroupIds()

    for group, title in groups.items():
        if group not in existing_groups:
            group_tool.addGroup(group, ['Reviewer'], [], title=title)


def custom_setup(context):

    if 'izug/seantis' in context._profile_path:
        setup_geo(context.getSite())
        setup_groups(context.getSite())
