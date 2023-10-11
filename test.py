import unittest
import main
from io import BytesIO

class TestPdfMerge(unittest.TestCase):

    def test_pdf_merge(self):
        with open("test_res/dummy_1.pdf", "rb") as fh:
            dummy_1_stream = BytesIO(fh.read())
        with open("test_res/dummy_2.pdf", "rb") as fh:
            dummy_2_stream = BytesIO(fh.read())
            
        merge_io = main.do_pdf_merge(dummy_1_stream, dummy_2_stream)
        
        self.assertTrue(merge_io != None)

if __name__ == '__main__':
    unittest.main()
