import unittest
from PyQt4.QTest import QTest

import reg

# new test for self.adjust in ImgGraph class

class ShapeSumbitFunctions(unittest.TestCase):
    def setUp(self):
        """ points in this format = [ '1,1,1','0.2,123' ]
        """
        self.points_set_true= [
                    ['1,1,1','2,2,2','3,3,3','4,4,4','5,5,5','6,6,6',
                     '7,7,7','8,8,8']
                    ]
    def test_submit( self, submit =None):
        fields =None
        for points in points_set_true:
            for field, point in zip(fields,points):
                # QTest.keyClick(mywidget,str key)
                QTest.keyClick(field,point)
        # click (sumbit_btn)
        QTest.mouseClick(sumbit,Qt.LeftButton)
    def test_sumbit_false(self):
        pass
