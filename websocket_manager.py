import abc
import websockets
import asyncio
import logging


class WSManager(object, metaclass=abc.ABCMeta):

    def __init__(self, inbound_queue, outbound_queue):
        self._logger = logging.getLogger('{}.{}'.format(__name__, type(self).__name__))
        self._websocket = None
        self._in_queue = inbound_queue
        self._out_queue = outbound_queue

        self._keep_writing = True
        self._keep_reading = True
        self._lock = asyncio.Lock()

        self._read_future = None
        self._write_future = None

    async def _spawn_websocket(self):
        websocket = None
        try:
            connect_url = self._build_ws_connect_url()
            headers_list = self._build_ws_connect_headers()
            subprotocols = self._build_ws_connect_subprotocols()
            if connect_url is not None:
                try:
                    websocket = await websockets.connect(connect_url, extra_headers=headers_list, subprotocols=subprotocols)
                except Exception as e:
                    print(e)
                #if websocket is not None:
                self._logger.info("Websocket connected!!")

        except Exception as e:
            self._logger.error("Exception is ws routine: " + str(e))

        return websocket

    async def _get_websocket(self):
        await self._lock.acquire()

        if self._websocket is None:
            self._websocket = await self._spawn_websocket()

        self._lock.release()

        return self._websocket

    async def _manage_write(self):
        try:
            websocket = await self._get_websocket()
            while websocket is not None and self._keep_writing:
                message = await self._out_queue.get()
                if message is None:
                    self._keep_writing = False
                else:
                    self._logger.debug("==WSS==> {}".format(message))
                    await websocket.send(message)
                self._out_queue.task_done()
        except Exception as e:
            self._logger.error("manage_write exception: " + str(e))

    async def _manage_read(self):
        try:
            websocket = await self._get_websocket()
            while websocket is not None and self._keep_reading:
                message = await websocket.recv()
                if message is not None:
                    # self._logger.debug("<==WSS== {}".format(message),extra=LoggerSubtypesDict.RECEIVING)
                    self._in_queue.put_nowait(message)
                else:
                    self._keep_reading = False
        except Exception as e:
            self._logger.error("manage_read exception: " + str(e))

    def start(self):
        self._write_future = asyncio.ensure_future(self._manage_write())
        self._read_future = asyncio.ensure_future(self._manage_read())

    def stop(self):
        if self._read_future is not None:
            self._read_future.cancel()
            self._read_future = None
        if self._write_future is not None:
            self._write_future.cancel()
            self._write_future = None
        if self._websocket is not None:
            self._websocket.close()
            self._websocket = None

    def restart(self):
        self.stop()
        self.start()

    @abc.abstractmethod
    def _build_ws_connect_url(self):
        ...

    @abc.abstractmethod
    def _build_ws_connect_headers(self):
        ...

    def _build_ws_connect_subprotocols(self):
        return []
