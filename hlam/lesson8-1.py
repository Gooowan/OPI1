import unittest


def CheckTriangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "Not exist"
    if a >= abs(b-c) or b >= abs(c-a) or c >= abs(b-a):
        return "Not exist"
    return "Exist"


class TestTriangle(unittest.TestCase):

    def lower_zero(self):
        self.assertEqual(CheckTriangle(0, 0, 0), "Not exist")

    def bigger(self):
        self.assertEqual(CheckTriangle(1, 10, 20), "Not exist")

    def will_exist(self):
        self.assertEqual(CheckTriangle(1, 10, 20), "Exist")


unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestTriangle))
