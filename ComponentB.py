from Component import Component
from ConnectionInterface import ConnectionInterface
from Log import Log


class ComponentB(Component):
    """
    Intermediary component that receives messages from ComponentA, forwards to ComponentC (bidirectional),
    and handles responses from ComponentC.
    
    Flow:
    - Receives messages from ComponentA on connection_in (unidirectional)
    - Forwards to ComponentC on connection_forward (bidirectional) and receives response
    
    Methods:
    - receiver: Listens to ComponentA, forwards to ComponentC, handles responses
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentB with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Required: 'connection_in' (unidirectional from ComponentA), 'connection_forward' (bidirectional with ComponentC)
                          Optional: 'log_connection' (for logging)
                          
        Example:
            component = ComponentB(connection_in=conn_in, connection_forward=conn_bc, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Associate receiver method
        if 'connection_in' in connections:
            self.add_method(self.receiver)

    def receiver(self) -> None:
        """
        Receives messages from ComponentA, forwards to ComponentC, and handles responses.
        
        Flow:
        1. Listens on connection_in for messages from ComponentA (already serialized)
        2. Forwards data as-is to ComponentC (no serialization/deserialization)
        3. Receives response and returns it as-is
        """
        def message_handler(data: str) -> str:
            Log.send(f"received: {data}", self.log_connection)
            
            # Forward the data to ComponentC and get response (bidirectional connection)
            if 'connection_forward' in self.connections:
                Log.send(f"forwards: {data}", self.log_connection)
                response = self.connections['connection_forward'].send(data)
                Log.send(f"received: {response}", self.log_connection)
                return response
            
            return ""
        
        self.connections['connection_in'].listen(message_handler)
