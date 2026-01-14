import threading
from typing import List, Callable, Dict, Tuple
from ConnectionInterface import ConnectionInterface


class Component:
    """
    Class that manages running multiple methods in separate threads.
    Each method receives connections as keyword arguments.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize the Component.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          The key represents the connection name/identifier,
                          and the value is a ConnectionInterface instance.
        """
        self.methods: List[Tuple[Callable, Dict[str, ConnectionInterface]]] = []
        self.connections: Dict[str, ConnectionInterface] = connections
        self.threads: List[threading.Thread] = []


    def add_method_with_connections(self, method: Callable, *connection_names: str) -> None:
        """
        Add a method with specific connections to be passed to it.
        
        Args:
            method: The method to execute in a thread.
            *connection_names: Names of the connections to pass to this method.
        """
        method_connections = self.get_connections(*connection_names)
        self.methods.append((method, method_connections))

    def run(self) -> None:
        """
        Run all methods in the list in separate threads.
        Each method receives only its associated connections as keyword arguments.
        """
        for method, method_connections in self.methods:
            # Create a thread for each method, passing only its associated connections as kwargs
            thread = threading.Thread(target=method, kwargs=method_connections, daemon=True)
            self.threads.append(thread)
            # Start the thread
            thread.start()

    def get_connections(self, *connection_names: str) -> Dict[str, ConnectionInterface]:
        """
        Get a subset of connections by name.
        
        Args:
            *connection_names: Names of the connections to retrieve.
            
        Returns:
            A dictionary containing only the requested connections.
        """
        return {name: self.connections[name] for name in connection_names if name in self.connections}

    def stop(self) -> None:
        """
        Stop all running threads (for daemon threads, they will stop when main thread exits).
        """
        self.threads.clear()
