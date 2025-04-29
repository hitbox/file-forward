import logging
import mimetypes
import os

from collections import namedtuple

from .base import LidoBase

logger = logging.getLogger(__name__)

class Document(
    namedtuple(
        'Document',
        field_names = [
            'doc_key',
            'file_name',
            'media_type',
        ],
    ),
    LidoBase,
):
    """
    :param doc_key:
        Unique document identifier in scope of briefing package
    :param file_name:
        File name of the document in the ZIP archive
    :param media_type:
        Media type of the document. Supported types are: "text/plain",
        "application/pdf"
    """

    rename_fields = {
        'doc_key': 'docKey',
        'file_name': 'fileName',
        'media_type': 'mediaType',
    }

    @classmethod
    def from_source_result(
        cls,
        source_result,
        doc_key = 'LCB',
        media_type = None,
    ):
        """
        LCB -> Load Control Briefing

        :param media_type:
            If None, guess media type.
        """
        filename = os.path.basename(source_result.path)

        if media_type is None:
            media_type, _ = mimetypes.guess_type(filename)
            if media_type is None:
                raise ValueError(
                    f'Could not guess MIME type for: {filename}')

        return cls(doc_key, filename, media_type)
