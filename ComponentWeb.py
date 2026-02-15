from Component import Component
from ConnectionInterface import ConnectionInterface
from Log import Log


class ComponentWeb(Component):
    """
    Web component that listens to incoming messages via FastAPI connection
    and returns them as responses.
    
    This component acts as a simple echo endpoint for the web frontend,
    demonstrating how to integrate the ComponentNetwork with a web interface.
    
    Methods:
    - receiver: Listens to FastAPI connection and echoes received messages
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize ComponentWeb with connections.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          Required: 'web_connection' (FastAPI connection from webpage)
                          Optional: 'log_connection' (for logging)
                          
        Example:
            component = ComponentWeb(web_connection=fastapi_conn, log_connection=log_conn)
        """
        super().__init__(**connections)
        
        # Associate receiver method
        if 'web_connection' in connections:
            self.add_method(self.receiver)

    def receiver(self) -> None:
        """
        Listens to incoming messages from the web frontend via FastAPI connection.
        Logs the received message and returns it as a response.
        
        Flow:
        1. Listens on web_connection for messages from the web frontend
        2. Logs the received message with timestamp
        3. Returns the message as-is (echo behavior)
        """
        def message_handler(data: str) -> str:
            Log.send(f"received from web: {data}", self.log_connection)
            
            # Echo the message back to the web frontend
            Log.send(f"responding: {data}", self.log_connection)
            return data
        
        self.connections['web_connection'].listen(message_handler)
