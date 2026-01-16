from Component import Component
from ConnectionInterface import ConnectionInterface
import inspect


class Log(Component):
    """
    Implementation of Component that listens to a connection and logs all incoming messages.
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
            self.add_method(self.listener_method)

    def listener_method(self) -> None:
        """
        Listener method that receives and logs all incoming messages.
        """
        def message_handler(data: str) -> str:
            print(f"[LOG] {data}")
            return ""
        
        self.connections['connection_log'].listen(message_handler)

    def send_log(self, message: str, connection_log: ConnectionInterface) -> None:
        """
        Send a formatted log message to the log connection.
        
        This method can be called by other components to send log messages.
        The component name and method name are automatically deduced from the calling context.
        The message will be prefixed with the component name and calling method.
        
        Args:
            message: The message string to log.
            connection_log: The connection to send the log message through.
            
        Example:
            log_component.send_log("Processing started", log_connection)
            # Output: [LOG] ComponentA::sender_method - Processing started
        """
        # Inspect the call stack to get caller information
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        
        # Get the calling method name
        method_name = caller_frame.f_code.co_name
        
        # Get the component name from the 'self' variable in the caller's context
        if 'self' in caller_frame.f_locals:
            component_name = caller_frame.f_locals['self'].__class__.__name__
        else:
            component_name = "Unknown"
        
        formatted_message = f"{component_name}::{method_name} - {message}"
        connection_log.send(formatted_message)
