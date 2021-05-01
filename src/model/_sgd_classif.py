# coding: utf-8

"""Simple Gradient Descent (SGD) classifier model implementation."""

import inspect
from abc import ABCMeta, abstractmethod

import sklearn
from sklearn.linear_model import SGDClassifier


class FederatedSGDClassifier(metaclass=ABCMeta):
    """Simple Gradient Descent (SGD) classifier model."""

    def __init__(
            self,
            n_classes,
            loss='log',
            penalty='l2',
            alpha=1e-4,
            l1_ratio=.15,
            fit_intercept=True,
            epsilon=0.1,
            n_jobs=None,
            learning_rate='optimal',
            eta0=.0,
            power_t=.5,
            class_weight=None
        ):
        """Instantiate the SGD-based classifier model."""
        self.n_classes = n_classes
        self.model = SGDClassifier(
            loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio,
            fit_intercept=fit_intercept, epsilon=epsilon, n_jobs=n_jobs,
            learning_rate=learning_rate, eta0=eta0, power_t=power_t,
            class_weight=class_weight
        )

    @abstractmethod
    def get_config(self):
        """Return a JSON-serializable dict enabling re-instantiation."""
        keys = inspect.signature(type(self)).parameters.keys()
        config = {'n_classes': self.n_classes}
        config.update({
            key: val for key, val in self.model.get_params() if key in keys
        })
        return config

    @abstractmethod
    def get_weights(self):
        """Return the model's trainable parameters."""
        weights = {'coef_': getattr(self.model, 'coef_', None)}
        if self.model.fit_intercept:
            weights['intercept_'] = getattr(self.model, 'intercept_', None)
        return weights

    @abstractmethod
    def set_weights(self, weights):
        """Update the model's trainable parameters to input values."""
        if 'coef_' not in weights:
            raise KeyError("Missing 'weights' key: 'coef_'")
        self.model.coef_ = weights['coef_']
        if self.model.fit_intercept:
            if 'intercept_' not in weights:
                raise KeyError("Missing 'weights' key: 'intercept_'")
            self.model.intercept_ = weights['intercept_']

    @abstractmethod
    def run_training_epoch(self, X, y, sample_weight=None):
        """Train the model on a given dataset for one epoch."""
        classes = list(range(self.n_classes))
        self.model.partial_fit(X, y, classes, sample_weight)

    @abstractmethod
    def evaluate(self, X, y, sample_weight=None):
        """Evaluate the model on a given dataset."""
        accuracy = self.model.score(X, y, sample_weight)
        logloss = sklearn.metrics.log_loss(
            y, self.model.predict_proba(X), sample_weight=sample_weight
        )
        return {'accuracy': accuracy, 'logloss': logloss, 'nsamples': len(y)}
