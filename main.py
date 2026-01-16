from Connection import Connection
from ComponentA import ComponentA
from ComponentB import ComponentB
from ComponentC import ComponentC
from Log import Log
import time


def main():
    """
    Main entry point for the ComponentNetwork application.
    """
    # Create a bidirectional queue connection for two-way communication between A and B
    connection = Connection('queue', bidirectional=True)
    
    # Create a unidirectional queue connection for forwarding data from B to C
    forward_connection = Connection('queue', bidirectional=False)
    
    # Create a unidirectional queue connection for feedback from C back to A
    feedback_connection = Connection('queue', bidirectional=False)
    
    # Create a unidirectional queue connection for logging
    log_connection = Connection('queue', bidirectional=False)
    
    print("Creating ComponentA (sender), ComponentB (receiver with forward), ComponentC (listener with feedback), and Log component...")
    
    # Create the Log component with log connection for listening to log messages
    component_log = Log(connection_log=log_connection)
    
    # Create ComponentA with connection_out for sending and connection_feedback for receiving feedback from C
    component_a = ComponentA(connection_out=connection, connection_feedback=feedback_connection, log_connection=log_connection)
    
    # Create ComponentB with connection_in for receiving and connection_forward for forwarding
    component_b = ComponentB(connection_in=connection, connection_forward=forward_connection, log_connection=log_connection)
    
    # Create ComponentC with connection_forward for listening to forwarded data and connection_feedback for sending feedback
    component_c = ComponentC(connection_forward=forward_connection, connection_feedback=feedback_connection, log_connection=log_connection)
    
    print("Running all components...")
    
    # Run all components (methods will run in separate threads)
    component_log.run()
    component_a.run()
    component_b.run()
    component_c.run()
    
    print("All components are running. Press Ctrl+C to stop.")
    
    try:
        # Keep the main thread alive with a loop that can be interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all components...")
        component_log.stop()
        component_a.stop()
        component_b.stop()
        component_c.stop()
        print("All components stopped.")

if __name__ == '__main__':
    main()
