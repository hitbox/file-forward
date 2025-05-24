from contextvars import ContextVar

session_context = ContextVar('session_context')

extra_data = ContextVar('extra_data')

def set_session_context(session):
    session_context.set(session)

def get_session_context():
    return session_context.get(None)
