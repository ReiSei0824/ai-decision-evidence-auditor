import importlib.util, unittest
from pathlib import Path
P=Path(__file__).parents[1]/'scripts'/'audit_claims.py'
s=importlib.util.spec_from_file_location('audit_claims',P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class TestAudit(unittest.TestCase):
    def row(self,**kw):
        x={'id':'C1','claim':'A claim','impact':'low','source_url':'https://example.com/a','published_at':'2026-09-18T00:00:00Z','accessed_at':'2026-09-19T00:00:00Z','support':'direct','confidence':0.9}; x.update(kw); return x
    def test_direct_pass(self): self.assertEqual(m.audit([self.row()])[0][0]['status'],'PASS')
    def test_missing_blocks(self): self.assertEqual(m.audit([self.row(support='missing')])[0][0]['status'],'BLOCK')
    def test_high_partial_review(self):
        r=m.audit([self.row(impact='high',support='partial')])[0][0]
        self.assertEqual(r['status'],'REVIEW'); self.assertTrue(r['issues'])
    def test_contradicted_blocks(self): self.assertEqual(m.audit([self.row(support='contradicted')])[0][0]['status'],'BLOCK')
    def test_duplicate_url_reported(self):
        _,d=m.audit([self.row(),self.row(id='C2')]); self.assertIn('https://example.com/a',d)
    def test_duplicate_id_review(self):
        r=m.audit([self.row(),self.row(source_url='https://example.com/b')])[0][1]
        self.assertIn('duplicate id',r['issues'])
if __name__=='__main__': unittest.main()
