from sqlalchemy.orm import Session

from file_forward import context
from file_forward.configlib import engine_from_config
from file_forward.model import File
from file_forward.model import LCBMessageModel
from file_forward.util import load_pyfile

def load_from_schedule(args):
    """
    Load OptiClimb schedule PDF files as database objects.
    """
    appconfig = load_pyfile(args.config)
    engine = engine_from_config(appconfig)

    with Session(engine) as session:
        # Set ContextVar data for methods deep inside calls that need session.
        context.set_session_context(session)

        scanner = appconfig.local_schedule_pdf_scan

        for file_obj in scanner.generate_results():

            file_instance = File.from_source_result(file_obj)

            token = context.extra_data.set(file_obj.path_data)
            try:
                lcb_message_instance = LCBMessageModel.from_source_result(file_obj)
            finally:
                context.extra_data.reset(token)

            lcb_message_instance.file = file_instance

            session.add(lcb_message_instance)

        session.commit()
