from Component import Component
from ConnectionInterface import ConnectionInterface
import inspect
from datetime import datetime


class Log(Component):
    """
    Logging component that listens to log messages from other components and prints them.
    
    Provides a static send() method for components to log messages with automatic component and method name detection.
    Supports full call stack tracking to show parent methods in the log output.
    
    Methods:
    - listener: Listens to incoming log messages and prints them
    - send (static): Static method for components to send log messages
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize Log with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Expected connections: 'connection_log' for listening to incoming messages.
                          
        Example:
            component = Log(connection_log=conn_log)
        """
        super().__init__(**connections)
        
        # Associate listener method
        if 'connection_log' in connections:
            self.add_method(self.listener)

    def listener(self) -> None:
        """
        Listener method that receives and logs all incoming messages.
        """
        def message_handler(data: str) -> str:
            print(data)
            return ""
        
        self.connections['connection_log'].listen(message_handler)

    @staticmethod
    def send(message: str, connection_log: ConnectionInterface = None) -> None:
        """
        Send a formatted log message to the log connection.
        
        This static method can be called by other components to send log messages.
        The component name and method names are automatically deduced from the calling context.
        The message will be prefixed with the component name and the full method call chain.
        
        Args:
            message: The message string to log.
            connection_log: The connection to send the log message through. If None, the message is not sent.
            
        Example:
            Log.send("Processing started", log_connection)
            # Output: [LOG] ComponentA::sender_method - Processing started
            # Or if called from nested function:
            # Output: [LOG] ComponentA::sender_method::message_handler - Processing started
        """
        # Check if connection_log is provided
        if connection_log is None:
            return
        
        # Inspect the call stack to get caller information
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        
        # Get the component name from the 'self' variable in the caller's context
        component_name = "Unknown"
        if 'self' in caller_frame.f_locals:
            component_name = caller_frame.f_locals['self'].__class__.__name__
        
        # Build the method call chain by walking up the stack
        method_chain = []
        current_frame = caller_frame
        
        # Collect all method names in the call stack until we reach a point that's not in a component
        while current_frame is not None:
            method_name = current_frame.f_code.co_name
            # Skip special methods and module-level code
            if not method_name.startswith('_') and method_name != '<module>':
                method_chain.append(method_name)
            current_frame = current_frame.f_back
        
        # Reverse to get the call order from outermost to innermost
        method_chain.reverse()
        
        # Build the formatted message
        if method_chain:
            method_path = '::'.join(method_chain)
            formatted_message = f"{component_name}::{method_path} - {message}"
        else:
            formatted_message = f"{component_name} - {message}"
        
        # Add timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format: YYYY-MM-DD HH:MM:SS.mmm
        formatted_message = f"[{timestamp}] {formatted_message}"        
        connection_log.send(formatted_message)
