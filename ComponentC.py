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
                          Expected connections: 'connection_forward', 'connection_feedback'.
                          
        Example:
            component = ComponentC(connection_forward=conn_forward, connection_feedback=conn_feedback)
        """
        super().__init__(**connections)
        
        # Associate feedback forwarder method with both connections
        # This single method handles listening and forwarding
        if 'connection_forward' in connections:
            self.add_method_with_connections(self.feedback_forwarder, 'connection_forward', 'connection_feedback')

    def feedback_forwarder(self, connection_forward=None, connection_feedback=None) -> None:
        """
        Feedback forwarder method that listens to forwarded data and sends it back to ComponentA.
        
        Args:
            connection_forward: The connection for receiving forwarded messages from ComponentB.
            connection_feedback: The connection for sending feedback back to ComponentA.
        """
        def message_handler(data: str) -> str:
            print(f"ComponentC: received forwarded '{data}'")
            print(f"ComponentC: sending feedback '{data}'")
            # Forward the data back to ComponentA via feedback connection
            if connection_feedback:
                connection_feedback.send(data)
            return ""
        
        connection_forward.listen(message_handler)


