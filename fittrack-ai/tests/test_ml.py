import unittest,tempfile,csv
from pathlib import Path
from PIL import Image
from ml.manifest import validate
from ml.evaluate import evaluate
class MLTests(unittest.TestCase):
 def test_metrics(self):
  r=evaluate([{'true':0,'probabilities':[.8,.2]},{'true':1,'probabilities':[.7,.3]}],['a','b']);self.assertEqual(r['top1'],.5);self.assertEqual(r['confusion_matrix'],[[1,0],[1,0]])
 def test_invalid_probabilities(self):
  with self.assertRaises(ValueError):evaluate([{'true':0,'probabilities':[float('nan')]}],['a'])
 def test_duplicates_and_grouping(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);Image.new('RGB',(30,30),'red').save(root/'a.png');Image.new('RGB',(30,30),'red').save(root/'b.png');Image.new('RGB',(30,30),'blue').save(root/'c.png')
   m=root/'input.csv'
   with m.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['path','label','source_url','license','group_id','consent_reference'])
    for name in ['a','b','c']:w.writerow([name+'.png','test_fixture','local:test','OWN-CONSENT','same-session','consent:test'])
   rows=validate(m,root);self.assertEqual(len(rows),2);self.assertEqual(len({r['split'] for r in rows}),1)
 def test_unlicensed_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   m=Path(d)/'input.csv';m.write_text('path,label,source_url,license,group_id,consent_reference\na.png,test,local,unknown,g,none\n')
   with self.assertRaises(ValueError):validate(m,d)

 def test_duplicate_bridges_sessions(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);Image.new('RGB',(30,30),'red').save(root/'a.png');Image.new('RGB',(30,30),'red').save(root/'duplicate.png')
   im=Image.new('RGB',(9,8));im.putdata([(255 if (x+y)%2 else 0,)*3 for y in range(8) for x in range(9)]);im.save(root/'b.png')
   m=root/'manifest.csv'
   with m.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['path','label','source_url','license','group_id','consent_reference'])
    for path,group in [('a.png','session-a'),('duplicate.png','session-b'),('b.png','session-b')]:w.writerow([path,'test','local','OWN-CONSENT',group,'consent:test'])
   rows=validate(m,root);self.assertEqual(len(rows),2);self.assertGreater((rows[0]['dhash']^rows[1]['dhash']).bit_count(),4);self.assertEqual(rows[0]['split'],rows[1]['split'])
