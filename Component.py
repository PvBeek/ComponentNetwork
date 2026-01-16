import threading
from typing import List, Callable, Dict, Tuple
from ConnectionInterface import ConnectionInterface


class Component:
    """
    Class that manages running multiple methods in separate threads.
    Methods can access connections through self.connections.
    """

    def __init__(self, **connections: ConnectionInterface) -> None:
        """
        Initialize the Component.
        
        Args:
            **connections: Connection objects passed as keyword arguments.
                          The key represents the connection name/identifier,
                          and the value is a ConnectionInterface instance.
        """
        self.methods: List[Callable] = []
        self.connections: Dict[str, ConnectionInterface] = connections
        self.threads: List[threading.Thread] = []


    def add_method(self, method: Callable) -> None:
        """
        Add a method to be executed in a thread.
        
        Args:
            method: The method to execute in a thread.
        """
        self.methods.append(method)

    def run(self) -> None:
        """
        Run all methods in the list in separate threads.
        Methods have access to self.connections.
        """
        for method in self.methods:
            # Create a thread for each method
            thread = threading.Thread(target=method, daemon=True)
            self.threads.append(thread)
            # Start the thread
            thread.start()

    def stop(self) -> None:
        """
        Stop all running threads (for daemon threads, they will stop when main thread exits).
        """
        self.threads.clear()
