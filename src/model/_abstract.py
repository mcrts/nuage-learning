# coding: utf-8

"""Abstract class defining federated models' API."""

from abc import ABCMeta, abstractmethod


class FederatedModel(metaclass=ABCMeta):
    """Abstract class defining federated models' API."""

    @abstractmethod
    def get_config(self):
        """Return a JSON-serializable dict enabling re-instantiation."""
        return NotImplemented

    @classmethod
    def from_config(cls, config):
        """Instantiate a FederatedModel from its configuration dict."""
        return cls(**config)

    @abstractmethod
    def get_weights(self):
        """Return the model's trainable parameters."""
        return NotImplemented

    @abstractmethod
    def set_weights(self, weights):
        """Update the model's trainable parameters to input values."""
        return NotImplemented

    @abstractmethod
    def run_training_epoch(self, X, y, sample_weight=None):
        """Train the model on a given dataset for one epoch."""
        return NotImplemented

    @abstractmethod
    def evaluate(self, X, y, sample_weight=None):
        """Evaluate the model on a given dataset."""
        return NotImplemented
