import unittest
from valuation.yield_curve import YieldCurve

#yc = YieldCurve()

class TestYieldCurve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("start")

    @classmethod
    def tearDownClass(cls):
        print("\nend")

    def test_PV(self):
        file_name: str = f"cad_ois.json"
        yc: YieldCurve = YieldCurve(file_name)
        msg: str = ""
        test_cnt: int = 0
        face_value: int = 1000

        # Case1: tenor == 1d
        test_cnt += 1
        yield_rate: float = 0.045297189150003
        tenor: int = 1
        case_result: float = yc.present_value(face_value,'1d')
        answer: float = face_value/((1 + yield_rate/365)**tenor)
        msg = f"Present value discount test {test_cnt}: function result = {case_result}, answer = {answer}"
        print(msg)
        self.assertEqual(case_result, answer)

        # Case2: tenor == 18263d
        yield_rate: float = 0.027498531006902804
        tenor: int = 18263
        case_result: float = yc.present_value(face_value,'18263d')
        answer: float = face_value/((1 + yield_rate/365)**tenor)
        msg = f"Present value discount test {test_cnt}: function result = {case_result}, answer = {answer}"
        print(msg)
        self.assertEqual(case_result, answer)