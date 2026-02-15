from abc import ABC, abstractmethod
from typing import Callable
from DataContract import DataContract

class ConnectionInterface(ABC):
    """Abstract base class for handling connections between components."""

    def __init__(self, bidirectional: bool, contract: DataContract = None) -> None:
        """Initialize the Connection.
        
        Args:
            bidirectional: Whether messages are replied to the sender.
            contract: Optional DataContract for serialization/deserialization.
        """
        self.bidirectional = bidirectional
        self.contract = contract

    @abstractmethod
    def listen(self, handler: Callable[[str], str]) -> None:
        """
        Abstract method to listen to and process the connection.
        
        Args:
            handler: A callable function that takes a string and returns a string.
        """
        pass

    @abstractmethod
    def send(self, data: str) -> str:
        """
        Abstract method to send data through the connection.
        
        Args:
            data: The data to be sent as a string.

        Returns:
            The data that was sent as a string.
        """
        pass
