from Component import Component
from ConnectionInterface import ConnectionInterface
from collections import deque
from Log import Log


class ComponentA(Component):
    """
    Sender component that sends incrementing messages to ComponentB and receives feedback from ComponentC.
    
    Methods:
    - sender: Sends incrementing messages through connection_out
    - receiver: Receives feedback from ComponentC and verifies messages
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentA with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Required: 'connection_out' (unidirectional to ComponentB), 'connection_feedback' (unidirectional from ComponentC)
                          Optional: 'log_connection' (for logging)
                          
        Example:
            component = ComponentA(connection_out=conn_out, connection_feedback=conn_feedback, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Store sent messages to verify feedback
        self.sent_messages = deque(maxlen=100)  # Keep last 100 messages
        
        # Associate sender method
        if 'connection_out' in connections:
            self.add_method(self.sender)
        
        # Associate listener method for feedback from ComponentC
        if 'connection_feedback' in connections:
            self.add_method(self.receiver)

    def sender(self) -> None:
        """
        Sends incrementing messages to ComponentB.
        
        Generates messages in format 'message N' and sends them through connection_out.
        Logs each sent message using Log.send().
        """
        counter = 0
        while True:
            counter += 1
            message = f"message {counter}"
            self.sent_messages.append(message)  # Store the sent message
            Log.send(f"sent: {message}", self.log_connection)
            self.connections['connection_out'].send(message)
            import time
            time.sleep(3)

    def receiver(self) -> None:
        """
        Receives feedback messages from ComponentC and verifies they match sent messages.
        
        Listens on connection_feedback for feedback messages. When received, checks if the message
        was previously sent (stored in self.sent_messages). Logs whether verification succeeded or failed.
        """
        def message_handler(data: str) -> str:
            if data in self.sent_messages:
                self.sent_messages.remove(data)  # Remove after verification
                Log.send(f"received: {data} ✓ VERIFIED", self.log_connection)
            else:
                Log.send(f"received: {data} ✗ NOT FOUND", self.log_connection)
            return ""
        
        self.connections['connection_feedback'].listen(message_handler)
