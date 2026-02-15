from Connection import Connection
from ComponentWeb import ComponentWeb
from Log import Log
import time


def main():
    """
    Main entry point for the ComponentNetwork web application.
    Uses FastAPI connection to receive messages from the web frontend.
    """
    # Create a FastAPI connection for web communication
    web_connection = Connection('fastapi', bidirectional=False, port=5000, handler_id="web_handler")
    
    # Create a unidirectional queue connection for logging
    log_connection = Connection('queue', bidirectional=False)
    
    print("Creating ComponentWeb for web frontend communication...")
    
    # Create the Log component with log connection for listening to log messages
    component_log = Log(connection_log=log_connection)
    
    # Create ComponentWeb to handle web requests
    component_web = ComponentWeb(web_connection=web_connection, log_connection=log_connection)
    
    print("Running all components...")
    print("FastAPI server is running on http://localhost:5000")
    print("Open web/index.html in your browser to interact with the ComponentNetwork")
    
    # Run all components (methods will run in separate threads)
    component_log.run()
    component_web.run()
    
    print("All components are running. Press Ctrl+C to stop.")
    
    try:
        # Keep the main thread alive with a loop that can be interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all components...")
        component_log.stop()
        component_web.stop()
        print("All components stopped.")

if __name__ == '__main__':
    main()
