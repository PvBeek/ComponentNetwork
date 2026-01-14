from abc import ABC, abstractmethod
from typing import Callable

class ConnectionInterface(ABC):
    """Abstract base class for handling connections between components."""

    def __init__(self, bidirectional: bool) -> None:
        """Messages are replied to the sender if bidirectional is True.
        Initialize the Connection.
        
        Args:
            port: The port number for the connection.
        """
        self.bidirectional = bidirectional

    @abstractmethod
    def listen(self, handler: Callable[[str], str]) -> None:
        """
        Abstract method to listen to and process the connection.
        
        Args:
            handler: A callable function that takes a string and returns a string.
            connection: An optional Connection object.
        """
        pass

    @abstractmethod
    def send(self, data: str) -> str:
        """
        Abstract method to send data through the connection.
        
        Args:
            data: The data to be sent as a string.
            wait_for_response: A boolean flag to indicate whether to wait for a response. Defaults to False.
        
        Returns:
            The data that was sent as a string.
        """
        pass
