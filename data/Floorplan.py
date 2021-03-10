from data.Module import *


class Floorplan:
    def __init__(self, modules: list[Module]):
        self.modules: list[Module] = modules
        self.aspect_ratio: Interval = self.compute_aspect_ratio_interval()

    def compute_aspect_ratio_interval(self) -> Interval:
        min_ar = sys.float_info.max
        max_ar = sys.float_info.min
        for module in self.modules:
            ar = module.dimensions.height / module.dimensions.width
            min_ar = min(min_ar, ar)
            max_ar = max(max_ar, ar)

        return Interval(min_ar, max_ar)

    def __str__(self):
        return "Floorplan: \n" + "\n".join([str(m) for m in self.modules])
