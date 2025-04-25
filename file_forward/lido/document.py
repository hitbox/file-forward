import json

class Document:

    def __init__(self, doc_key, file_name, media_type):
        """
        :param doc_key:
            Unique document identifier in scope of briefing package
        :param file_name:
            File name of the document in the ZIP archive
        :param media_type:
            Media type of the document. Supported types are: "text/plain",
            "application/pdf"
        """
        self.doc_key = doc_key
        self.file_name = file_name
        self.media_type = media_type

    @classmethod
    def from_source_result(cls, source_result):
        return cls(
            doc_key = 'LCB',
            file_name = source_result.filename,
            media_type = 'application/pdf',
        )

    def as_dict(self):
        return {
            'docKey': self.doc_key,
            'fileName': self.file_name,
            'mediaType': self.media_type,
        }

    def as_json_string(self):
        """
        """
        return json.dumps(self.as_dict())
