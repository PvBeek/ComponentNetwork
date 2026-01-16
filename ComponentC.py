from Component import Component
from ConnectionInterface import ConnectionInterface


class ComponentC(Component):
    """
    Implementation of Component that manages listener methods for forwarded data.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentC with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Expected connections: 'connection_forward', 'connection_feedback', and optionally 'log_connection'.
                          
        Example:
            component = ComponentC(connection_forward=conn_forward, connection_feedback=conn_feedback, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Associate feedback forwarder method
        if 'connection_forward' in connections:
            self.add_method(self.feedback_forwarder)

    def feedback_forwarder(self) -> None:
        """
        Feedback forwarder method that listens to forwarded data and sends it back to ComponentA.
        """
        def message_handler(data: str) -> str:
            if 'log_connection' in self.connections:
                formatted_msg = f"ComponentC::feedback_forwarder - received forwarded '{data}'"
                self.connections['log_connection'].send(formatted_msg)
            
            if 'log_connection' in self.connections:
                formatted_msg = f"ComponentC::feedback_forwarder - sending feedback '{data}'"
                self.connections['log_connection'].send(formatted_msg)
            
            # Forward the data back to ComponentA via feedback connection
            if 'connection_feedback' in self.connections:
                self.connections['connection_feedback'].send(data)
            return ""
        
        self.connections['connection_forward'].listen(message_handler)


