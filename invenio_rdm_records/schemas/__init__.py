# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM record schemas."""

from marshmallow import INCLUDE, EXCLUDE, Schema, fields, missing

from .access import AccessSchemaV1
from .communities import CommunitiesSchemaV1
from .files import FilesSchemaV1
from .metadata import MetadataSchemaV1
from .pids import PIDSSchemaV1
from .relations import RelationsSchemaV1
from .stats import StatsSchemaV1
from invenio_records_rest.schemas.fields import GenFunction


# NOTE: Use this one for system fields only
class AttributeAccessorFieldMixin:
    """Marshmallow field mixin for attribute-based serialization."""

    def get_value(self, obj, attr, accessor=None, default=missing):
        """Return the value for a given key from an object attribute."""
        attribute = getattr(self, "attribute", None)
        check_key = attr if attribute is None else attribute
        return getattr(obj, check_key, default)


class NestedAttribute(fields.Nested, AttributeAccessorFieldMixin):
    """Nested object attribute field."""



# NOTE: Explicitly use this at the top level of schemas that contain system
# fields (e.g. `record.files`) and even some of their nested values, e.g.
# `record.files.count`
class AttrSchema(_Schema):

    def get_attribute(self, obj, attr, default):
        return get_value(obj, attr, default)

# .vs

# NOTE: Use this one for system fields only
class NestedAttributeField(fields.Nested):

    def get_value(self, obj, attr, accessor=None, default=missing):
        attribute = getattr(self, "attribute", None)
        check_key = attr if attribute is None else attribute
        return get_value(obj, check_key, default)


class RDMRecordSchemaV1(Schema):
    """Record schema."""

    class Meta:
        unknown = EXCLUDE

    field_load_permissions = {
        'files': 'update',
    }

    field_dump_permissions = {
        'files': 'read_files',
    }

    # schema_version = fields.Interger(dump_only=True)
    revision = fields.Integer(attribute='revision_id', dump_only=True)
    id = fields.Str(attribute='recid', dump_only=True)
    concept_id = fields.Str(attribute='conceptrecid', dump_only=True)
    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)

    # status = fields.Str(dump_only=True)

    metadata = NestedAttribute(MetadataSchemaV1)
    access = NestedAttribute(AccessSchemaV1)
    # files = NestedAttribute(FilesSchemaV1, dump_only=True)
    # communities = NestedAttribute(CommunitiesSchemaV1)
    # pids = NestedAttribute(PIDSSchemaV1)
    # stats = NestedAttribute(StatsSchemaV1, dump_only=True)
    # relations = NestedAttribute(RelationsSchemaV1, dump_only=True)


__all__ = (
    'RDMRecordSchemaV1',
)