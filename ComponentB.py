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
                          Expected connections: 'connection_in', 'connection_forward', and optionally 'log_connection'.
                          
        Example:
            component = ComponentB(connection_in=conn_in, connection_forward=conn_forward, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Associate receiver method
        if 'connection_in' in connections:
            self.add_method(self.receiver_method)

    def receiver_method(self) -> None:
        """
        Receiver method that listens and forwards received data to another connection.
        """
        def message_handler(data: str) -> str:
            if 'log_connection' in self.connections:
                formatted_msg = f"ComponentB::receiver_method - received '{data}'"
                self.connections['log_connection'].send(formatted_msg)
            
            # Forward the data to another connection if provided
            if 'connection_forward' in self.connections:
                self.connections['connection_forward'].send(data)
                if 'log_connection' in self.connections:
                    formatted_msg = f"ComponentB::receiver_method - forwarded '{data}'"
                    self.connections['log_connection'].send(formatted_msg)
            
            # Return acknowledgement
            ack_msg = f"{data}"
            return ack_msg
        
        self.connections['connection_in'].listen(message_handler)
