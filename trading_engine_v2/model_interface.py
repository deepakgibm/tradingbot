from abc import ABC, abstractmethod
import pandas as pd

class ModelInterface(ABC):
    """
    An abstract base class for machine learning models.
    Defines a consistent interface for training and prediction.
    """

    @abstractmethod
    def train(self, data: pd.DataFrame):
        """
        Trains the model on the given data.
        """
        pass

    @abstractmethod
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Makes predictions on the given data.
        """
        pass
