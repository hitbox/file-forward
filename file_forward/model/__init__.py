from . import lido
from .database import AircraftRegistration
from .database import Airline
from .database import Airport
from .database import Base
from .database import Credential
from .database import DocumentModel
from .database import File
from .database import LCBHeaderModel
from .database import LCBMessageFilter
from .database import LCBMessageModel
from .database import LCBPropertiesModel
from .database import LegIdentifierModel
from .database import LidoMetaPropertyModel
from .database import MessageCommitted
from .database import OFPVersion
from .database import ProcessingState
from .database import Rowifier
from .database import SSLKeyRepository
from .database import Server
from .database import SourceResult

def get_models():
    from inspect import isclass

    return {
        name: obj for name, obj in globals().items()
        if isclass(obj) and obj is not Base and issubclass(obj, Base)
    }
