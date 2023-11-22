import torch
import numpy

from .scheduler import Scheduler


class SigmoidScheduler(Scheduler):
    """_summary_"""

    start: float
    end: float
    tau: float

    def __init__(
        self,
        start: float = -3.0,
        end: float = 3.0,
        tau: float = 1.0,
    ) -> None:
        """_summary_

        Parameters
        ----------
        start : float, optional
            _description_, by default -3.0
        end : float, optional
            _description_, by default 3.0
        tau : float, optional
            _description_, by default 1.0
        """
        self.start = start
        self.end = end
        self.tau = tau

    def __call__(self, t: torch.Tensor) -> torch.Tensor:
        """_summary_

        Parameters
        ----------
        x : torch.Tensor
            _description_

        Returns
        -------
        torch.Tensor
            _description_
        """
        assert torch.all(t >= 0.0) and torch.all(t <= 1.0)
        f = lambda x: 1.0 / (1.0 + numpy.exp(-x / self.tau))
        v_start = f(self.start)
        v_end = f(self.end)
        v_t = f(t * (self.end - self.start) + self.start)
        return (v_t - v_start) / (v_end - v_start)
