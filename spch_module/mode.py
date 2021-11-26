from collections import namedtuple

from .formulas import dh, my_z, ob_raskh
from .limit import Limit

LIST_ITEMS_MODE = 't_in q_in p_in'
class Mode(namedtuple('Mode', LIST_ITEMS_MODE)):
    """Класс режима работы
    """
    def get_volume_rate(self, lim:Limit)->float:
        """Расчет обьемного расхода

        Args:
            lim (Limit): ПВТ-свойства

        Returns:
            float: Обьемный расход, м3/мин
        """
        return ob_raskh(self.q_in, self.p_in, self.t_in, lim.r_val, lim.plot_std)
