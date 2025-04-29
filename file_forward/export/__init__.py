from .json_message import JSONMessage
from .xml_message import XMLMessage

export_flat_json = JSONMessage(style='flat')
export_nested_json = JSONMessage(style='nested')
export_flat_xml = XMLMessage(style='flat')
export_nested_xml = XMLMessage(style='nested')
