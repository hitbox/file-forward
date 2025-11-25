from marshmallow import Schema
from marshmallow import post_load
from marshmallow import validate
from marshmallow.fields import DateTime
from marshmallow.fields import Integer
from marshmallow.fields import Nested
from marshmallow.fields import String
from marshmallow.fields import Time



class LogLineSchema(LogLineMixin, Schema):

    pass
