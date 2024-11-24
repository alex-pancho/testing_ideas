import unittest
from endless_array import EndlessAray


"""
a.set(1, "a")
a.get(1) # a
a.get(1000) # None

a.set_all("b")
a.set(2, "c")

a.get(1) # b
a.get(2) # c
a.get(1000000000000000000000000) # b
"""

class TestEndlessAray(unittest.TestCase):
    """Test for EndlessAray class"""

    def setUp(self) -> None:
        """Setup class to self variable"""
        self.ea = EndlessAray()
    
    def test_01_set_val(self):
        """Set and check one value"""
        expeced_value = "a"
        self.ea.set(1, expeced_value)
        actual_value = self.ea.get(1)
        self.assertEqual(actual_value, expeced_value, f"Unexpeced value:{actual_value}")

    def test_02_get_unset_val(self):
        """Get unexsist value"""
        actual_value = self.ea.get(100)
        self.assertIsNone(actual_value, f"Unexpeced value:{actual_value}")

    def test_03_set_all(self):
        """Set all check"""
        all_values = "b"
        one_value = "c"
        self.ea.set_all(all_values)
        self.ea.set(2, one_value)
        actual_value_1 = self.ea.get(1)
        self.assertEqual(actual_value_1, all_values, f"Unexpeced value:{actual_value_1}")
        actual_value_2 = self.ea.get(2)
        self.assertEqual(actual_value_2, one_value, f"Unexpeced value:{actual_value_1}")
        actual_value_3 = self.ea.get(1000000000000000)
        self.assertEqual(actual_value_3, all_values, f"Unexpeced value:{actual_value_1}")

if __name__ == '__main__':
    unittest.main(verbosity=2)