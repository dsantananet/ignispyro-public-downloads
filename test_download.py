import tempfile,pathlib,unittest,unittest.mock as mock
import download
class Tests(unittest.TestCase):
 def response(self,payload):
  response=mock.MagicMock();response.__enter__.return_value.read.return_value=payload
  opener=mock.MagicMock();opener.open.return_value=response;return opener
 def test_valid_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as folder, mock.patch('urllib.request.build_opener',return_value=self.response(b'{"data":[]}')):
   path=pathlib.Path(folder)/'data.json';result=download.fetch('stations',path)
   self.assertEqual(result['bytes'],11);self.assertEqual(len(result['sha256']),64)
   with self.assertRaises(FileExistsError):download.fetch('stations',path)
 def test_invalid_json_not_written(self):
  with tempfile.TemporaryDirectory() as folder, mock.patch('urllib.request.build_opener',return_value=self.response(b'<html>error')):
   path=pathlib.Path(folder)/'data.json'
   with self.assertRaises(ValueError):download.fetch('stations',path)
   self.assertFalse(path.exists())
 def test_limit(self):
  with mock.patch('urllib.request.build_opener',return_value=self.response(b'x'*(download.LIMIT+1))):
   with self.assertRaises(ValueError):download.fetch('stations','unused.json')
 def test_redirect_refused(self):
  with self.assertRaises(ValueError):download.NoRedirect().redirect_request(None,None,None,None,None,None)
 def test_source_allowlist(self):
  with self.assertRaises(KeyError):download.fetch('http://localhost','unused.json')
if __name__=='__main__':unittest.main()
