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
    # Create a unidirectional queue connection for sending data from A to B
    connection_a_to_b = Connection('queue', bidirectional=False)
    
    # Create a bidirectional queue connection for two-way communication between B and C
    connection_b_c = Connection('queue', bidirectional=True)
    
    # Create a unidirectional queue connection for feedback from C back to A
    feedback_connection = Connection('queue', bidirectional=False)
    
    # Create a unidirectional queue connection for logging
    log_connection = Connection('queue', bidirectional=False)
    
    print("Creating ComponentA (sender), ComponentB (bidirectional with C), ComponentC (bidirectional with B), and Log component...")
    
    # Create the Log component with log connection for listening to log messages
    component_log = Log(connection_log=log_connection)
    
    # Create ComponentA with connection_out for sending to B and connection_feedback for receiving feedback from C
    component_a = ComponentA(connection_out=connection_a_to_b, connection_feedback=feedback_connection, log_connection=log_connection)
    
    # Create ComponentB with connection_in for receiving from A and connection_bc for bidirectional communication with C
    component_b = ComponentB(connection_in=connection_a_to_b, connection_forward=connection_b_c, log_connection=log_connection)
    
    # Create ComponentC with connection_bc for bidirectional communication with B and connection_feedback for sending feedback to A
    component_c = ComponentC(connection_forward=connection_b_c, connection_feedback=feedback_connection, log_connection=log_connection)
    
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
