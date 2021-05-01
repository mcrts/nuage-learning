# coding: utf-8

"""Simple Gradient Descent (SGD) classifier model implementation."""

import inspect

import numpy as np
import sklearn
from sklearn.linear_model import SGDClassifier

from src.model import FederatedModel

class FederatedSGDClassifier(FederatedModel):
    """Simple Gradient Descent (SGD) classifier model."""

    def __init__(
            self,
            n_classes,
            n_features,
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
        self.n_features = n_features
        self.model = SGDClassifier(
            loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio,
            fit_intercept=fit_intercept, epsilon=epsilon, n_jobs=n_jobs,
            learning_rate=learning_rate, eta0=eta0, power_t=power_t,
            class_weight=class_weight
        )

    def get_config(self):
        """Return a JSON-serializable dict enabling re-instantiation."""
        keys = inspect.signature(type(self)).parameters.keys()
        config = {'n_classes': self.n_classes, 'n_features': self.n_features}
        config.update({
            key: val for key, val in self.model.get_params() if key in keys
        })
        return config

    def get_weights(self):
        """Return the model's trainable parameters."""
        weights = {'coef_': getattr(self.model, 'coef_', None)}
        if self.model.fit_intercept:
            weights['intercept_'] = getattr(self.model, 'intercept_', None)
        return weights

    def set_weights(self, weights):
        """Update the model's trainable parameters to input values."""
        if 'coef_' not in weights:
            raise KeyError("Missing 'weights' key: 'coef_'")
        self.model.coef_ = weights['coef_']
        if self.model.fit_intercept:
            if 'intercept_' not in weights:
                raise KeyError("Missing 'weights' key: 'intercept_'")
            self.model.intercept_ = weights['intercept_']

    def generate_weights(self, random=True, seed=None):
        if random:
            rng = np.random.default_rng(seed=seed)
            get_weights = lambda size: rng.normal(size=size).astype(np.float32)
        else:
            get_weights = lambda size: np.zeros(shape=size, dtype=np.float32)

        weights = {'coef_': get_weights((self.n_features, self.n_classes))}

        if self.model.fit_intercept:
            weights['intercept_'] = get_weights((self.n_classes,))
        return weights

    def run_training_epoch(self, X, y, sample_weight=None):
        """Train the model on a given dataset for one epoch."""
        classes = list(range(self.n_classes))
        self.model.partial_fit(X, y, classes, sample_weight)

    def evaluate(self, X, y, sample_weight=None):
        """Evaluate the model on a given dataset."""
        accuracy = self.model.score(X, y, sample_weight)
        logloss = sklearn.metrics.log_loss(
            y, self.model.predict_proba(X), sample_weight=sample_weight
        )
        return {'accuracy': accuracy, 'logloss': logloss, 'nsamples': len(y)}

    def aggregate_weights(self, dataset_sizes, partial_weights):
        total = sum(dataset_sizes)
        data = (dataset_sizes, partial_weights)
        coef = np.sum([n * w['coef_'] for n, w in zip(data)], axis=0)
        weights = {'coef': coef / total}
        if self.model.fit_intercept:
            bias = np.sum([n * w['intercept_'] for n, w in zip(data)], axis=0)
            weights['intercept_'] = bias / total
        return weights
