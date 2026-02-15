from Component import Component
from ConnectionInterface import ConnectionInterface
from Log import Log


class ComponentA(Component):
    """
    Sender component that sends incrementing integer counter values to ComponentB and receives feedback from ComponentC.
    
    Uses IntegerContract to serialize/deserialize integer values in format 'Message <integer>'.
    
    Methods:
    - sender: Sends incrementing integer counter values through connection_out
    - receiver: Receives feedback integers from ComponentC and verifies they match sent values
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentA with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Required: 'connection_out' (unidirectional to ComponentB with IntegerContract), 
                                    'connection_feedback' (unidirectional from ComponentC with IntegerContract)
                          Optional: 'log_connection' (for logging)
                          
        Example:
            component = ComponentA(connection_out=conn_out, connection_feedback=conn_feedback, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Store sent counter values to verify feedback
        self.sent_counters = set()  # Store integer counter values
        
        # Associate sender method
        if 'connection_out' in connections:
            self.add_method(self.sender)
        
        # Associate listener method for feedback from ComponentC
        if 'connection_feedback' in connections:
            self.add_method(self.receiver)

    def sender(self) -> None:
        """
        Sends incrementing integer counter values to ComponentB.
        
        Generates integers (1, 2, 3, ...) and sends them through connection_out.
        Uses the connection's contract to serialize the integer (e.g., to 'Message <integer>' format).
        Logs each sent counter using Log.send().
        """
        counter = 0
        while True:
            counter += 1
            self.sent_counters.add(counter)  # Store the counter value
            Log.send(f"sent: {counter}", self.log_connection)
            
            # Serialize using connection's contract if available
            connection_out = self.connections['connection_out']
            if connection_out.contract:
                data_to_send = connection_out.contract.serialize(counter)
            else:
                data_to_send = counter
            
            connection_out.send(data_to_send)
            import time
            time.sleep(3)

    def receiver(self) -> None:
        """
        Receives feedback from ComponentC and verifies they match sent counter values.
        
        Listens on connection_feedback for feedback. Uses the connection's contract to 
        deserialize the data (e.g., from 'Message <integer>' format to integer).
        When received, checks if the integer was previously sent (stored in self.sent_counters).
        Logs whether verification succeeded or failed.
        """
        def message_handler(data: str) -> str:
            # Deserialize using connection's contract if available
            connection_feedback = self.connections['connection_feedback']
            if connection_feedback.contract:
                counter_value = connection_feedback.contract.deserialize(data)
            else:
                counter_value = int(data) if isinstance(data, str) else data
            
            if counter_value in self.sent_counters:
                self.sent_counters.remove(counter_value)  # Remove after verification
                Log.send(f"received: {counter_value} ✓ VERIFIED", self.log_connection)
            else:
                Log.send(f"received: {counter_value} ✗ NOT FOUND", self.log_connection)
            
            # Return serialized response
            if connection_feedback.contract:
                return connection_feedback.contract.serialize(counter_value)
            else:
                return str(counter_value)
        
        self.connections['connection_feedback'].listen(message_handler)
