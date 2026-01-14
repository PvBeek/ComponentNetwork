from Component import Component
from ConnectionInterface import ConnectionInterface
from collections import deque


class ComponentA(Component):
    """
    Implementation of Component that manages sender methods.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentA with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Expected connections: 'connection_out' and optionally 'connection_feedback'.
                          
        Example:
            component = ComponentA(connection_out=conn_out, connection_feedback=conn_feedback)
        """
        super().__init__(**connections)
        
        # Store sent messages to verify feedback
        self.sent_messages = deque(maxlen=100)  # Keep last 100 messages
        
        # Associate sender method with its connection
        if 'connection_out' in connections:
            self.add_method_with_connections(self.sender_method, 'connection_out')
        
        # Associate listener method for feedback from ComponentC
        if 'connection_feedback' in connections:
            self.add_method_with_connections(self.listener_method, 'connection_feedback')

    def sender_method(self, connection_out=None) -> None:
        """
        Sender method that sends incrementing messages through the connection.
        
        Args:
            connection_out: The output connection for sending messages.
        """
        counter = 0
        while True:
            counter += 1
            message = f"Message {counter}"
            self.sent_messages.append(message)  # Store the sent message
            print(f"ComponentA: sends '{message}'")
            response = connection_out.send(message)
            print(f"ComponentA: received acknowledged '{response}'")
            import time
            time.sleep(3)

    def listener_method(self, connection_feedback=None) -> None:
        """
        Listener method that receives feedback from ComponentC and verifies it matches sent messages.
        
        Args:
            connection_feedback: The connection for receiving feedback messages.
        """
        def message_handler(data: str) -> str:
            if data in self.sent_messages:
                self.sent_messages.remove(data)  # Remove after verification
                print(f"ComponentA: received feedback: '{data}' ✓ VERIFIED")
            else:
                print(f"ComponentA: received feedback: '{data}' ✗ NOT FOUND")
            return ""
        
        connection_feedback.listen(message_handler)
