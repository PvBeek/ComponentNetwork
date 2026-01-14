from typing import Literal
from ConnectionInterface import ConnectionInterface
from QueueConnection import QueueConnection


class Connection:
    """
    Factory class that creates and manages different types of connections.
    The connection type is determined at initialization.
    """

    def __new__(cls, connection_type: Literal['queue', 'restapi'] = 'queue', bidirectional: bool = True) -> ConnectionInterface:
        """
        Create and return a connection of the specified type.
        
        Args:
            connection_type: The type of connection to create. Options: 'queue', 'restapi'. Defaults to 'queue'.
            bidirectional: Whether messages are replied to the sender. Defaults to True.
        
        Returns:
            A ConnectionAdapter instance of the specified type.
            
        Raises:
            ValueError: If the connection type is not supported.
        """
        if connection_type == 'queue':
            return QueueConnection(bidirectional)
        elif connection_type == 'restapi':
            # TODO: Import and return RestApiConnection once implemented
            raise NotImplementedError("RestAPI connection is not yet implemented")
        else:
            raise ValueError(f"Unsupported connection type: {connection_type}. Supported types: 'queue', 'restapi'")
