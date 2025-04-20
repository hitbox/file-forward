class MQOutput:
    """
    Write message to IBM MQ queue.
    """

    def __init__(self, client):
        self.client = client

    def run(self):
        with self.client as mq:
            message_descriptor = mq.put('Hello from file-forward.')
            mq.commit()
            print(message_descriptor)
