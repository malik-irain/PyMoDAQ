from bayes_opt.acquisition import UpperConfidenceBound
from pymodaq.extensions.bayesian.acquisition import AcquisitionFunctionBase


class UCB(AcquisitionFunctionBase):
    _usual_name = "Upper Confidence Bound"

    def __init__(self, random_state = None):
        self._random_state = random_state
        self.params = {

        }

        super().__init__()


    def init_acquisition_function(self, **kwargs):
        self._function = UpperConfidenceBound(self._random_state, kwargs)

    def base_acq(mean, std):
        return self._function.base_acq(mean, std)

    def decay_exploration(self):
        self._function.decay_exploration()

    @property
    def tradeoff(self):
        return self._function.kappa

    @property.setter
    def tradeoff(self, tradeoff):
        self._function.kappa = tradeoff

    def suggest(self, gaussian_process, target_space, n_random = 1000, n_l_bfgs_b = 10, fit_gp = True):
        return self._function.suggest(gaussian_process, target_space, n_random, n_l_bfgs_b, fit_gp)