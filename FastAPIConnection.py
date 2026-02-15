from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable, Optional
from threading import Thread
import uvicorn
from ConnectionInterface import ConnectionInterface


class FastAPIConnection(ConnectionInterface):
    """
    FastAPI implementation of ConnectionInterface for HTTP-based communication.
    Uses a singleton pattern to ensure the server starts only once.
    Assumes the opposite endpoint is handled by a webpage client.
    """
    
    _instance: Optional['FastAPIConnection'] = None
    _app: Optional[FastAPI] = None
    _server_thread: Optional[Thread] = None
    _handlers: dict = {}
    
    def __new__(cls, bidirectional: bool = True, contract=None, port: int = 5000, handler_id: str = None):
        """
        Singleton pattern to ensure only one FastAPI server instance.
        
        Args:
            bidirectional: Whether messages are replied to the sender.
            contract: Optional DataContract for serialization/deserialization.
            port: Port to run the FastAPI server on. Defaults to 5000.
            handler_id: Unique identifier for this handler.
        """
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
            instance._init_app(port)
        return cls._instance
    
    def __init__(self, bidirectional: bool = True, contract=None, port: int = 5000, handler_id: str = None):
        """
        Initialize the FastAPIConnection.
        
        Args:
            bidirectional: Whether messages are replied to the sender.
            contract: Optional DataContract for serialization/deserialization.
            port: Port to run the FastAPI server on.
            handler_id: Unique identifier for this handler.
        """
        super().__init__(bidirectional, contract)
        self.port = port
        self.handler_id = handler_id or "default"
    
    @classmethod
    def _init_app(cls, port: int = 5000):
        """Initialize the FastAPI app and start the server (only once)."""
        if cls._app is not None:
            return  # App already initialized
        
        cls._app = FastAPI(title="ComponentNetwork FastAPI")
        
        # Add CORS middleware to allow requests from the web frontend
        cls._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @cls._app.post("/api/send")
        async def receive_message(request_data: dict):
            """
            Receive a message from the web frontend or another client.
            Routes the message to registered handlers.
            """
            if not cls._handlers:
                raise HTTPException(status_code=503, detail="No handlers registered")
            
            # Get the first registered handler
            handler_id = list(cls._handlers.keys())[0]
            handler, bidirectional = cls._handlers[handler_id]
            
            try:
                # Call the handler directly with the message
                reply = handler(str(request_data))
                
                # Only return a response if bidirectional is True
                if bidirectional and reply:
                    return {"status": "success", "response": reply}
                elif bidirectional:
                    return {"status": "success"}
                else:
                    # Unidirectional: process message but don't send response
                    return {"status": "received"}
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        # Start the server in a background thread
        cls._server_thread = Thread(
            target=lambda: uvicorn.run(cls._app, host="127.0.0.1", port=port, log_level="error"),
            daemon=True
        )
        cls._server_thread.start()
        
        import time
        time.sleep(1)  # Give server time to start
    
    def listen(self, handler: Callable[[str], str]) -> None:
        """
        Register a handler to process incoming messages from the web endpoint.
        The handler is called directly when messages arrive via HTTP.
        
        Args:
            handler: A callable function to process incoming data.
        """
        # Register the handler with its bidirectional flag
        FastAPIConnection._handlers[self.handler_id] = (handler, self.bidirectional)
    
    def send(self, data: str) -> str:
        """
        Send data. Since the opposite endpoint is the web client (which initiates requests),
        this method stores the data for the next request from the client.
        
        Args:
            data: The data to be sent as a string.
            
        Returns:
            The sent data.
        """
        # In a web-based model, the server doesn't initiate requests to clients
        # The client (webpage) makes requests and receives responses from handlers
        return data

