# coding: utf-8

"""Simple implementation of metric-based early stopping."""

class EarlyStoping:
    """Simple implementation of metric-based early stopping."""

    def __init__(
            self,
            tolerance=1e-3,
            patience=5,
            decrease=True
        ):
        """Instantiate the early stopping criterion.

        tolerance   : float, improvement value below which the
                      epoch is deemed to be non-improving
        patience    : int, number of consecutive non-improving
                      epochs that will trigger early stopping
        decrease    : whether the monitored metric is supposed
                      to decrease or increase with training
        """
        self.tolerance = tolerance
        self.patience = patience
        self.decrease = decrease
        self._best_metric = None
        self._n_iter_stuck = 0

    def keep_running(self, metric):
        """Update the early stopping decision based on a new value.

        metric : value of the monitored metric at the current epoch

        Return a bool indicating whether training should continue.
        """
        # Case when the input metric is the first to be received.
        if self._best_metric is None:
            self._best_metric = metric
            return True
        # Otherwise, compute the metric's improvement and act consequently.
        diff = (metric - self._best_metric) * (-1 if self.decrease else 1)
        if diff < 0:
            self._best_metric = metric
        if (diff + self.tolerance) > 0:
            self._n_iter_stuck += 1
        else:
            self._n_iter_stuck = 0
        return self._n_iter_stuck < self.patience
