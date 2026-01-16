from Component import Component
from ConnectionInterface import ConnectionInterface
from Log import Log


class ComponentC(Component):
    """
    Final component that receives forwarded messages from ComponentB (bidirectional),
    sends acknowledgments back to ComponentB, and forwards feedback to ComponentA.
    
    Flow:
    - Receives messages from ComponentB on connection_forward (bidirectional)
    - Sends acknowledgment response back to ComponentB on same connection
    - Sends feedback to ComponentA on connection_feedback (unidirectional)
    
    Methods:
    - receiver: Listens to ComponentB, sends acknowledgments, and forwards feedback to ComponentA
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentC with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Required: 'connection_forward' (bidirectional with ComponentB), 'connection_feedback' (unidirectional to ComponentA)
                          Optional: 'log_connection' (for logging)
                          
        Example:
            component = ComponentC(connection_forward=conn_bc, connection_feedback=conn_feedback, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Associate feedback forwarder method
        if 'connection_forward' in connections:
            self.add_method(self.receiver)

    def receiver(self) -> None:
        """
        Receives messages from ComponentB, sends acknowledgments, and forwards feedback to ComponentA.
        
        Flow:
        1. Listens on connection_forward (bidirectional) for messages from ComponentB
        2. Sends acknowledgment response back to ComponentB on the same connection
        3. Sends the message as feedback to ComponentA on connection_feedback
        """
        def message_handler(data: str) -> str:
            Log.send(f"received: {data}", self.log_connection)
            
            # Send acknowledgment back to ComponentB on the bidirectional connection
            ack_msg = f"ack {data}"
            Log.send(f"replying: {ack_msg}", self.log_connection)
            
            # Send feedback to ComponentA via feedback connection
            Log.send(f"forwards: {data}", self.log_connection)
            if 'connection_feedback' in self.connections:
                self.connections['connection_feedback'].send(data)
            
            # Return the acknowledgment to send back to ComponentB on the bidirectional connection
            return ack_msg
        
        self.connections['connection_forward'].listen(message_handler)


