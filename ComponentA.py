from Component import Component
from ConnectionInterface import ConnectionInterface
from collections import deque
import inspect


class ComponentA(Component):
    """
    Implementation of Component that manages sender methods.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentA with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Expected connections: 'connection_out', 'connection_feedback', and 'log_connection'.
                          
        Example:
            component = ComponentA(connection_out=conn_out, connection_feedback=conn_feedback, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Store sent messages to verify feedback
        self.sent_messages = deque(maxlen=100)  # Keep last 100 messages
        
        # Associate sender method
        if 'connection_out' in connections:
            self.add_method(self.sender_method)
        
        # Associate listener method for feedback from ComponentC
        if 'connection_feedback' in connections:
            self.add_method(self.listener_method)

    def sender_method(self) -> None:
        """
        Sender method that sends incrementing messages through the connection.
        """
        counter = 0
        while True:
            counter += 1
            message = f"Message {counter}"
            self.sent_messages.append(message)  # Store the sent message
            if 'log_connection' in self.connections:
                formatted_msg = f"ComponentA::sender_method - sends '{message}'"
                self.connections['log_connection'].send(formatted_msg)
            response = self.connections['connection_out'].send(message)
            if 'log_connection' in self.connections:
                formatted_msg = f"ComponentA::sender_method - received acknowledged '{response}'"
                self.connections['log_connection'].send(formatted_msg)
            import time
            time.sleep(3)

    def listener_method(self) -> None:
        """
        Listener method that receives feedback from ComponentC and verifies it matches sent messages.
        """
        def message_handler(data: str) -> str:
            if data in self.sent_messages:
                self.sent_messages.remove(data)  # Remove after verification
                if 'log_connection' in self.connections:
                    formatted_msg = f"ComponentA::listener_method - received feedback: '{data}' ✓ VERIFIED"
                    self.connections['log_connection'].send(formatted_msg)
            else:
                if 'log_connection' in self.connections:
                    formatted_msg = f"ComponentA::listener_method - received feedback: '{data}' ✗ NOT FOUND"
                    self.connections['log_connection'].send(formatted_msg)
            return ""
        
        self.connections['connection_feedback'].listen(message_handler)
