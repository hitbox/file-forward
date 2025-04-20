import pymqi

from file_forward.util import bitwise_or

class MQClient:
    """
    IBM MQ Client.
    """

    def __init__(self,
        host,
        port,
        channel,
        queue_manager_name,
        queue_name,
        ssl_key_repository,
        certificate_label,
        cipher,
        queue_options,
    ):
        self.host = host
        self.port = port
        self.channel = channel
        self.queue_manager_name = queue_manager_name
        self.queue_name = queue_name
        self.ssl_key_repository = ssl_key_repository
        self.certificate_label = certificate_label
        self.cipher = cipher
        self.queue_options = queue_options

        self.queue = None
        self.queue_manager = None

    def connection_info(self):
        """
        Connection string.
        """
        return f'{self.host}({self.port})'

    def get_channel_definition(self):
        """
        Channel definition object.
        """
        conn_info = self.connection_info()
        channel_definition = pymqi.CD(
            ChannelName = self.channel.encode(),
            ConnectionName = conn_info.encode(),
            ChannelType = pymqi.CMQC.MQCHT_CLNTCONN,
            TransportType = pymqi.CMQC.MQXPT_TCP,
            SSLCipherSpec = self.cipher.encode(),
        )
        return channel_definition

    def get_ssl_config_options(self):
        """
        SSL Configuration object.
        """
        ssl_config_options = pymqi.SCO(
            KeyRepository = self.ssl_key_repository.encode(),
            CertificateLabel = self.certificate_label.encode(),
        )
        return ssl_config_options

    def get_queue_manager(self, channel_definition=None, ssl_config_options=None):
        """
        QueueManager object.
        """
        if channel_definition is None:
            channel_definition = self.get_channel_definition()
        if ssl_config_options is None:
            ssl_config_options = self.get_ssl_config_options()
        queue_manager = pymqi.QueueManager(None)
        queue_manager.connect_with_options(
            self.queue_manager_name,
            cd = channel_definition,
            sco = ssl_config_options,
        )
        return queue_manager

    def put(self, message, md=None):
        """
        Put a message on the connected queue.
        """
        if md is None:
            md = pymqi.MD()
        self.queue.put(message, md)
        return md

    def commit(self):
        self.queue_manager.commit()

    def get_queue(self, queue_manager=None):
        if queue_manager is None:
            queue_manager = self.queue_manager
        queue = pymqi.Queue(queue_manager, self.queue_name, self.queue_options)
        return queue

    def connect(self):
        """
        Connect to queue from configuration. Return None.
        """
        self.queue_manager = self.get_queue_manager()
        self.queue = self.get_queue()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.queue:
            self.queue.close()
        if self.queue_manager:
            self.queue_manager.disconnect()


def inquire_queue(queue_manager, queue_name):
    args = {
        pymqi.CMQC.MQCA_Q_NAME: queue_name,
        pymqi.CMQC.MQIA_CURRENT_Q_DEPTH: None,
        pymqi.CMQC.MQIA_MAX_MSG_LENGTH: None,
        pymqi.CMQC.MQIA_Q_TYPE: None,
        pymqi.CMQC.MQIA_INHIBIT_GET: None,
        pymqi.CMQC.MQIA_INHIBIT_PUT: None,
    }

    pcf = pymqi.PCFExecute(queue_manager)
    response = pcf.MQCMD_INQUIRE_Q(args)

    # There's usually only one result
    queue_info = response[0]
    for k, v in queue_info.items():
        print(f'{pymqi.CMQC.lookup(k)}: {v}')

def test_list_queue(queue):
    message_descriptor = pymqi.MD()
    get_message_options = pymqi.GMO()
    get_message_options.Options = pymqi.CMQC.MQGMO_BROWSE_FIRST + pymqi.CMQC.MQGMO_NO_WAIT
    while True:
        try:
            msg = queue.get()
            print("Message:", msg)
        except pymqi.MQMIError as e:
            if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                print("No more messages.")
                break
            else:
                raise

def test_watch_queue(queue):
    message_descriptor = pymqi.MD()
    get_message_options = pymqi.GMO()

    # NOTES:
    # - WAIT and BROWSE are different and incompatible.

    get_options_first = (
        pymqi.CMQC.MQGMO_WAIT
        | pymqi.CMQC.MQGMO_BROWSE_FIRST
        #| pymqi.CMQC.MQGMO_BROWSE_NEXT
        | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
        #| pymqi.CMQC.MQGMO_NO_WAIT
    )

    get_options_next = (
        pymqi.CMQC.MQGMO_WAIT
        | pymqi.CMQC.MQGMO_BROWSE_NEXT
        | pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING
    )

    get_message_options.Options = reduce(operator.or_, [
    ])
    get_message_options.WaitInterval = 1000 # 1 second

    # Apparently max_length = None, do *NOT* mean get any length.
    max_length = 4096
    while True:
        try:
            message = queue.get(max_length, message_descriptor, get_message_options)
            get_message_options.Options = get_options_next
        except pymqi.MQMIError as e:
            if e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                print('No messages.')
            else:
                raise
