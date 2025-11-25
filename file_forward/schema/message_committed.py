from marshmallow import Schema
from marshmallow import post_load
from marshmallow import validate
from marshmallow.fields import Date
from marshmallow.fields import Integer
from marshmallow.fields import List
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import Time

from file_forward.model.lido import LegIdentifierField
from file_forward.model.lido.leg_identifier_field import SEP

from .field import SplitSchemaField
from .mixin import LogLineMixin

class DocumentSchema(Schema):

    docKey = String()
    fileName = String()
    mediaType = String()


class LegIdentifierFieldSchema(Schema):

    # TODO
    # - Database objects for these, or at least verify and normalize IATA/ICAO

    airline_code = String()
    flight_number = String()
    date_of_origin = Date(format='%d%b%y')
    departure_airport = String()
    destination_airport = String()
    operational_suffix = String()


class LidoMetaSchema(Schema):

    documents = List(Nested(DocumentSchema))
    legIdentifier = SplitSchemaField(
        SEP,
        LegIdentifierField._fields,
        LegIdentifierFieldSchema,
    )


class FieldsSchema(Schema):

    JMSExpiration = Integer(allow_none=True)
    JMSType = String(validate=validate.Equal('Byte'))
    LidoMeta = Nested(LidoMetaSchema)


class DataSchema(Schema):

    fields = Nested(FieldsSchema)
    host = String()
    queue = String()


class MessageCommittedSchema(LogLineMixin, Schema):
    """
    Data scraped from log lines for "message committed" messages.
    """

    data = Nested(DataSchema)
