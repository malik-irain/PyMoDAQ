from abc import ABCMeta
from typing import Callable

from bayes_opt.acquisition import AcquisitionFunction

from pymodaq_gui.managers.parameter_manager import ParameterManager
from pymodaq_utils.factory import ObjectFactory
from pymodaq_utils.logger import set_logger, get_module_name

logger = set_logger(get_module_name(__file__))

class AcquisitionFunctionBase(ParameterManager, metaclass=ABCMeta):
    _usual_name : str
    _function : AcquisitionFunction

    def init_function(self, **kwargs):
        raise NotImplementedError

    def base_acq(self, *args, **kwargs):
        raise NotImplementedError

    def suggest(self, gaussian_process, target_space, n_random = 1000, n_l_bfgs_b = 10, fit_gp = True):
        raise NotImplementedError

    def decay_exploration(self):
        raise NotImplementedError

    @property
    def tradeoff(self):
        raise NotImplementedError
    

# TODO: Remove inheritance
class AcquisitionFunctionFactory(ObjectFactory):
    @classmethod
    def register(cls) -> Callable:
        """ To be used as a decorator

        Register in the class registry a new scanner class using its 2 identifiers: scan_type and scan_sub_type
        """

        def inner_wrapper(wrapped_class: AcquisitionFunctionBase) -> Callable:
            if cls.__name__ not in cls._builders:
                cls._builders[cls.__name__] = {}
            key = wrapped_class._usual_name

            if key not in cls._builders[cls.__name__]:
                cls._builders[cls.__name__][key] = wrapped_class
            else:
                logger.warning(f'The {cls.__name__}/{key} builder is already registered. Replacing it')
            return wrapped_class

        return inner_wrapper


    def get(self, key : str) -> AcquisitionFunctionBase:
        builder = self._builders[self.__name__].get(key)
        if not builder:
            raise ValueError(key)
        return builder


    def create(self, key, **kwargs) -> AcquisitionFunctionBase:
        return self.get(key)(**kwargs)


