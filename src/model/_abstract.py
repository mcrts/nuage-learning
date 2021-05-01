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
    def generate_weights(self, random=True, seed=None):
        """Return zero-valued or random weights that match the model's specs.

        random : bool, whether to generate random weights (drawn from a
                 normal distribution) rather than zero-valued ones
        seed   : optional int, seed to the RNG used if 'random' is True

        Return a dict associating numpy arrays of weights to string keys.
        """
        return NotImplemented

    @abstractmethod
    def run_training_epoch(self, X, y, sample_weight=None):
        """Train the model on a given dataset for one epoch."""
        return NotImplemented

    @abstractmethod
    def evaluate(self, X, y, sample_weight=None):
        """Evaluate the model on a given dataset."""
        return NotImplemented
