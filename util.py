from bbox import BBox2D
from bbox.box_modes import XYXY


class CBBox2D(BBox2D):
    def __init__(self, x, mode=XYXY):
        super().__init__(x, mode)

    def __contains__(self, item: BBox2D):
        check_x1 = self.x1 >= item.x1
        check_x2 = self.x2 <= item.x2
        check_y1 = self.y1 >= item.y1
        check_y2 = self.y2 <= item.y2
        return all([check_x1, check_x2, check_y1, check_y2])

    def area(self):
        return self._w * self._h
