from typing import Literal
from ConnectionInterface import ConnectionInterface
from QueueConnection import QueueConnection


class Connection:
    """
    Factory class that creates and manages different types of connections.
    The connection type is determined at initialization.
    """

    def __new__(cls, connection_type: Literal['queue', 'fastapi'] = 'queue', bidirectional: bool = True, contract=None, port: int = 5000, handler_id: str = None) -> ConnectionInterface:
        """
        Create and return a connection of the specified type.
        
        Args:
            connection_type: The type of connection to create. Options: 'queue', 'fastapi'. Defaults to 'queue'.
            bidirectional: Whether messages are replied to the sender. Defaults to True.
            contract: Optional DataContract for serialization/deserialization. Defaults to None.
            port: Port for fastapi connections. Defaults to 5000.
            handler_id: Unique identifier for fastapi handler. Defaults to None.
        
        Returns:
            A ConnectionInterface instance of the specified type.
            
        Raises:
            ValueError: If the connection type is not supported.
        """
        if connection_type == 'queue':
            return QueueConnection(bidirectional, contract)
        elif connection_type == 'fastapi':
            from FastAPIConnection import FastAPIConnection
            return FastAPIConnection(bidirectional, contract, port, handler_id)
        else:
            raise ValueError(f"Unsupported connection type: {connection_type}. Supported types: 'queue', 'fastapi'")
