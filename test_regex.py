import unittest
from nose_parameterized import parameterized
import reg, main
valid_points= [
                '1,1,1','2,2,2','3,3,3','4,4,4','5,5,5','6,6,6',
                 '7,7,7','8,8,8','0.1,0.3,3.23'
                    ]
invalid_points = [
                ',1,2,3','3,2,1,',
                '0.1','a','1.123.113',
                "0.1,1.2323.32,123",
                ]
class RegExTest(unittest.TestCase):
    def setUp(self):
        self.regexpr= reg.match_nums
    def iter_string(self,points):
        return all(self.regexpr.exactMatch(point) for point in points)
    @parameterized.expand([
        ("regex accept",valid_points, True),
        ("regex reject",invalid_points, False)])
    def test_regex(self,name,points,expected):
        self.assertEqual(self.iter_string(points), expected)

