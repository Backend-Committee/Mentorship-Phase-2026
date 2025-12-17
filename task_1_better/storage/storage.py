from abc import ABC, abstractmethod


class Storage(ABC):
    """Abstract storage interface"""

    @abstractmethod
    def init(self):
        """Initialize storage."""
        pass