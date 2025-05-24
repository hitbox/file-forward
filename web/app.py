from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def test():
        return 'Hello!'

    # TODO
    # - Yet another web app
    # - Display my database info
    # - Probably need another load that associates files to messages
    # - Maybe missing other relevant info
    # - Need sent_at datetime for messages that can be none
    # - Add database step to LCBOutput class

    return app
