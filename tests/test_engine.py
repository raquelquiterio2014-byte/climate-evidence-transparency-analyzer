import unittest
import pandas as pd
from engine import audit,to_tonnes,retrieve,file_sha256
class Tests(unittest.TestCase):
 def sample(self): return pd.DataFrame([dict(country='X',year=2023,sector='Energy',gas='CO2e',value=2,unit='MtCO2e',source_url='https://example.org')])
 def test_valid(self): self.assertEqual(audit(self.sample()).iloc[0].severity,'PASS')
 def test_conversion(self): self.assertEqual(to_tonnes(self.sample()).iloc[0].tonnes_co2e,2000000)
 def test_duplicate(self): self.assertTrue(all(audit(pd.concat([self.sample(),self.sample()],ignore_index=True)).severity=='REVIEW'))
 def test_url(self):
  x=self.sample();x.loc[0,'source_url']='';self.assertEqual(audit(x).iloc[0].severity,'REVIEW')
 def test_negative(self):
  x=self.sample();x.loc[0,'value']=-1;self.assertEqual(audit(x).iloc[0].severity,'REVIEW')
 def test_retrieve(self): self.assertEqual(len(retrieve('climate',[dict(title='A',text='climate')])) ,1)
 def test_hash(self): self.assertEqual(len(file_sha256(b'a')),64)
 def test_schema(self):
  with self.assertRaises(ValueError): audit(self.sample().drop(columns=['unit']))
