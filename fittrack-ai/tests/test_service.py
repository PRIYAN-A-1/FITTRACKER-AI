import unittest,io,tempfile
from PIL import Image
from ml.service import decode_image,Runtime
class ServiceTests(unittest.TestCase):
 def test_valid_png(self):
  stream=io.BytesIO();Image.new('RGB',(10,10),'red').save(stream,format='PNG');self.assertEqual(decode_image(stream.getvalue()).size,(10,10))
 def test_invalid_image(self):
  with self.assertRaises((ValueError,OSError)):decode_image(b'not-an-image')
 def test_empty_rejected(self):
  with self.assertRaises(ValueError):decode_image(b'')
 def test_missing_model_not_fake(self):
  with tempfile.TemporaryDirectory() as d:self.assertIsNone(Runtime(d).infer(Image.new('RGB',(1,1))))
