from typing import Callable
class Border:
    def __init__(self, value_0:float, sens:float, func:Callable) -> None:
        self.value_0 = value_0
        self.sens = sens
        self.func = func
    def get_sigal(value:float)->float: #TODO: пороговая функция
        pass
