import abc
import numpy as np


class Channel(object):
    v = None

    def __init__(self):
        self._times = []
        self._currents = []
        self._conductancy = []

    def compute(self, v, steps, step_size=0.01):
        Channel.v = v
        t_eval = np.arange(start=0, stop=steps, step=step_size)
        time, current, conductancy = self._compute(v, steps, step_size, t_eval)

        self._times.extend(time)
        self._currents.extend(current)
        self._conductancy.extend(conductancy)

    @abc.abstractmethod
    def _compute(self, v, steps, step_size, t_eval):
        raise NotImplementedError()

    def get_time(self):
        return np.array(self._times)

    def get_current(self):
        return np.array(self._currents)

    def get_conductance(self):
        return np.array(self._conductancy)