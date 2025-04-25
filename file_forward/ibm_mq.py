import pymqi

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
        user_id = None,
        cipher_spec = None,
        queue_options = None,
        confirm_query_manager = None,
    ):
        self.host = host
        self.port = port
        self.channel = channel
        self.queue_manager_name = queue_manager_name
        self.queue_name = queue_name
        self.ssl_key_repository = ssl_key_repository
        self.certificate_label = certificate_label
        self.user_id = user_id
        self.cipher_spec = cipher_spec
        self.queue_options = queue_options
        self.confirm_query_manager = confirm_query_manager

        self._queue = None
        self._queue_manager = None

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
        )

        if self.cipher_spec:
            channel_definition.SSLCipherSpec = self.cipher_spec.encode()

        if self.user_id:
            channel_definition.UserIdentifier = self.user_id.encode()

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

    def inquire(self, queue_manager):
        keys = [
            # Server's platform.
            'pymqi.CMQC.MQIA_PLATFORM',
            # Queue manager's name.
            'pymqi.CMQC.MQCA_Q_MGR_NAME',
            # Default dead letter queue.
            'pymqi.CMQC.MQCA_DEAD_LETTER_Q_NAME',
            # Max message length.
            'pymqi.CMQC.MQIA_MAX_MSG_LENGTH',
            # Command level (supported features) basically the version.
            'pymqi.CMQC.MQIA_COMMAND_LEVEL',
        ]
        def _inquire(key):
            value = queue_manager.inquire(eval(key))
            if isinstance(value, bytes):
                value = value.decode().strip()
            return value
        result = {key: _inquire(key) for key in keys}
        return result

    def raise_for_query_manager(self, queue_manager):
        # Inquire query manager to confirm assumptions.
        results = {}
        for attribute, expect in self.confirm_query_manager.items():
            if isinstance(attribute, str):
                attribute_value = eval(attribute)
            else:
                attribute_value = attribute
            result = queue_manager.inquire(attribute_value)
            if isinstance(expect, str):
                result = result.decode().strip()
            results[attribute] = result

        for key, expect in self.confirm_query_manager.items():
            # Raise for unexpected result.
            if results[key] != expect:
                raise ValueError(
                    f'Query manager confirmation failed for {key}, expected'
                    f' {expect}, got {results[key]!r}.')

    def get_queue_manager(self, channel_definition=None, ssl_config_options=None):
        """
        QueueManager object.
        """
        if channel_definition is None:
            channel_definition = self.get_channel_definition()

        if ssl_config_options is None:
            ssl_config_options = self.get_ssl_config_options()

        # Defer connect with name = None.
        queue_manager = pymqi.QueueManager(name=None)

        queue_manager.connect_with_options(
            self.queue_manager_name,
            cd = channel_definition,
            sco = ssl_config_options,
        )

        if self.confirm_query_manager:
            self.raise_for_query_manager(queue_manager)

        return queue_manager

    def get_queue(self, queue_manager=None):
        if queue_manager is None:
            queue_manager = self._queue_manager

        args = [self.queue_name]
        if self.queue_options is not None:
            args.append(self.queue_options)

        queue = pymqi.Queue(queue_manager, *args)
        return queue

    def connect(self):
        """
        Connect to queue from configuration. Return None.
        """
        self._queue_manager = self.get_queue_manager()
        self._queue = self.get_queue()

    def __enter__(self):
        """
        Enter context manager.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit context manager, closing everything.
        """
        if self._queue:
            self._queue.close()
        if self._queue_manager:
            self._queue_manager.disconnect()

    def put(self, message, msg_desc=None, put_opts=None):
        """
        Put a message on the connected queue.
        """
        if msg_desc is None:
            # Fresh message descriptor if not given one.
            msg_desc = pymqi.MD()
            if self.user_id:
                msg_desc.UserIdentifier = self.user_id.encode()

        if put_opts is None:
            # Put Message Options
            put_opts = pymqi.PMO()

        self._queue.put(message, msg_desc, put_opts)
        return msg_desc

    def commit(self):
        """
        Commit writes.
        """
        self._queue_manager.commit()
