import unittest


# def solve(a, b, c):
#     roots = []
#
#     discriminant = b*b - 4*a*c
#
#     if discriminant > 0:
#         roots.append((-b + discriminant**0.5) / (2*a))
#         roots.append((-b - discriminant ** 0.5) / (2 * a))
#     elif discriminant == 0:
#         roots.append(-b / (2*a))
#     else:
#         return "No real roots"
#
#     return roots
#
#
# class TestQuadraticSolver(unittest.TestCase):
#     def test_no_roots(self):
#         self.assertEqual(solve(1, 0, 1), "No real roots")
#
#     def test_one_root(self):
#         self.assertEqual(solve(1, 2, 1), [-1.0])
#
#     def test_two_roots(self):
#         self.assertEqual(solve(1, -3, 2), [2.0, 1.0])

def discounts(goods):
    goods.sort()
    if len(goods) == 0:
        return 0
    if len(goods) == 1:
        return goods[0]
    if len(goods) == 2:
        final_check = goods[0] * 0.8 + goods[1]
        return final_check
    if len(goods) > 2:
        final_check = goods[0] * 0.7 + goods[1] * 0.8 + sum(goods[2:])
        return final_check


# class TestDiscounts(unittest.TestCase):
#
#     def test_no_good(self):
#         self.assertEqual(discounts([]), 0)
#
#     def test_one_good(self):
#         self.assertEqual(discounts([10]), 10)
#
#     def test_two_good_order1(self):
#         self.assertEqual(discounts([100, 200]), 280)
#
#     def test_two_good_order2(self):
#         self.assertEqual(discounts([200, 100]), 280)
#
#     def test_three_good_order1(self):
#         self.assertEqual(discounts([100, 200, 300]), 530)
#
#     def test_three_good_order2(self):
#         self.assertEqual(discounts([200, 100, 300]), 530)
#
#     def test_four_good_order2(self):
#         self.assertEqual(discounts([200, 100, 300, 400]), 930)
#
#
# # unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestQuadraticSolver))
# unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestDiscounts))


import unittest

def CheckTriangleExist(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "Not exist"
    if a > abs(b + c) or b > abs(c + a) or c > abs(b + a):
        return "Not exist"
    return "Exist"

class TestTriangle(unittest.TestCase):

    def test_lower_zero(self):
        self.assertEqual(CheckTriangleExist(0, 0, 0), "Not exist")

    def test_bigger(self):
        self.assertEqual(CheckTriangleExist(1, 10, 20), "Not exist")

    def test_will_exist(self):
        self.assertEqual(CheckTriangleExist(5, 6, 7), "Exist")


if __name__ == '__main__':
    unittest.main()

