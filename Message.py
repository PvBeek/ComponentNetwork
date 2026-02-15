from DataContract import DataContract
import re


class Message(DataContract):
    """
    Data contract for integer serialization.
    
    Serializes integers to format: "Message <integer>"
    Deserializes from "Message <integer>" back to integer.
    
    Example:
        contract = IntegerContract()
        serialized = contract.serialize(42)  # "Message 42"
        deserialized = contract.deserialize("Message 42")  # 42
    """

    def serialize(self, data: any) -> str:
        """
        Serialize an integer to "Message <integer>" format.
        
        Args:
            data: An integer to serialize
            
        Returns:
            Formatted string: "Message <integer>"
            
        Raises:
            TypeError: If data is not an integer
        """
        if not isinstance(data, int):
            raise TypeError(f"Expected int, got {type(data).__name__}")
        
        return f"Message {data}"

    def deserialize(self, data: str) -> int:
        """
        Deserialize "Message <integer>" format back to an integer.
        
        Args:
            data: Serialized string in format "Message <integer>"
            
        Returns:
            The extracted integer value
            
        Raises:
            TypeError: If data is not a string
            ValueError: If data doesn't match the expected format
        """
        if not isinstance(data, str):
            raise TypeError(f"Expected str, got {type(data).__name__}")
        
        match = re.match(r"Message\s+(-?\d+)", data.strip())
        if not match:
            raise ValueError(f"Data doesn't match 'Message <integer>' format: {data}")
        
        return int(match.group(1))
