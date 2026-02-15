from abc import ABC, abstractmethod

class DataContract(ABC):
    """
    Abstract base class for data contracts that handle serialization/deserialization.
    """

    @abstractmethod
    def serialize(self, data: any) -> str:
        """
        Serialize data to a string.
        
        Args:
            data: The data to serialize (can be dict, object, etc.)
            
        Returns:
            Serialized string representation
        """
        pass

    @abstractmethod
    def deserialize(self, data: str) -> any:
        """
        Deserialize a string back to data.
        
        Args:
            data: Serialized string
            
        Returns:
            Deserialized data
        """
        pass

