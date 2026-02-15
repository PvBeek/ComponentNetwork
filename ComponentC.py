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
        1. Listens on connection_forward (bidirectional) for messages from ComponentB (already serialized)
        2. Forwards data as-is to ComponentA feedback (no serialization/deserialization)
        3. Returns acknowledgment as-is
        """
        def message_handler(data: str) -> str:
            Log.send(f"received: {data}", self.log_connection)
            
            # Send feedback to ComponentA via feedback connection (data already serialized)
            if 'connection_feedback' in self.connections:
                Log.send(f"forwards: {data}", self.log_connection)
                self.connections['connection_feedback'].send(data)
            
            # Return acknowledgment to ComponentB (echo back the same data)
            Log.send(f"replying: {data}", self.log_connection)
            return data
        
        self.connections['connection_forward'].listen(message_handler)



