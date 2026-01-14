from queue import Queue
from typing import Callable
from ConnectionInterface import ConnectionInterface


class QueueConnection(ConnectionInterface):
    """Implementation of Connection that uses queues for communication."""

    def __init__(self, bidirectional: bool = True) -> None:
        """
        Initialize the QueueConnection.
        
        Args:
            bidirectional: Whether messages are replied to the sender. Defaults to True.
        """
        super().__init__(bidirectional)
        self.down_queue: Queue = Queue()
        self.down_queue.name = "down_queue"
        self.up_queue: Queue = Queue()
        self.up_queue.name = "up_queue"

    def listen(self, handler: Callable[[str], str]) -> None:
        """
        Listen to the down queue and process incoming data with the handler function.
        
        Args:
            handler: A callable function to process incoming data.
        """
        while True:
            data = self.down_queue.get()
            if data is None:  # Sentinel value to stop listening
                break
            reply = handler(data)
            if reply:
                self.up_queue.put(reply)

    def send(self, data: str) -> str:
        """
        Send data through the down queue.
        
        Args:
            data: The data to be sent as a string.
            
        Returns:
            The data that was sent.
        """
        self.down_queue.put(data)
        if self.bidirectional:
            reply = self.up_queue.get()
            return reply
        return data

    def stop_listening(self) -> None:
        """
        Stop the listening process by putting a sentinel value in the down queue.
        """
        self.down_queue.put(None)
