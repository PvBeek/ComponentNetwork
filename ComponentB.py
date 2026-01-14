from Component import Component
from ConnectionInterface import ConnectionInterface


class ComponentB(Component):
    """
    Implementation of Component that manages receiver methods.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentB with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Expected connections: 'connection_in' and optionally 'connection_forward'.
                          
        Example:
            component = ComponentB(connection_in=conn_in, connection_forward=conn_forward)
        """
        super().__init__(**connections)
        
        # Associate receiver method with its connections
        if 'connection_in' in connections:
            if 'connection_forward' in connections:
                self.add_method_with_connections(self.receiver_method, 'connection_in', 'connection_forward')
            else:
                self.add_method_with_connections(self.receiver_method, 'connection_in')

    def receiver_method(self, connection_in=None, connection_forward=None) -> None:
        """
        Receiver method that listens and forwards received data to another connection.
        
        Args:
            connection_in: The input connection for receiving messages.
            connection_forward: Optional connection to forward the received data to.
        """
        def message_handler(data: str) -> str:
            print(f"ComponentB: received '{data}'")
            
            # Forward the data to another connection if provided
            if connection_forward:
                connection_forward.send(data)
                print(f"ComponentB: forwarded '{data}'")
            
            # Return acknowledgement
            ack_msg = f"{data}"
            return ack_msg
        
        connection_in.listen(message_handler)
