import unittest
from get_infos import memorylist

class get_infos_Test_Case(unittest.TestCase):
    def test_memory(self):
        self.assertEqual(len(memorylist),6)
        i=0
        while(i<6):
            self.assertNotEqual(memorylist[i],0)
            i+=1
