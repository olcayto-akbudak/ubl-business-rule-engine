import unittest, tempfile, json, sqlite3, copy
from pathlib import Path
import app as c

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.config = json.loads((Path(__file__).resolve().parent / 'scenario.json').read_text(encoding='utf-8'))

    def test_valid(self):
        self.assertEqual(c.validate(self.config['documents'][0]['xml']), [])

    def test_total(self):
        self.assertTrue(c.validate(self.config['documents'][1]['xml']))

    def test_dtd(self):
        self.assertTrue(c.validate('<!DOCTYPE Invoice><Invoice/>'))

    def test_size(self):
        self.assertTrue(c.validate('x' * 100, max_bytes=20))

    def test_namespace(self):
        self.assertTrue(c.validate(self.config['documents'][0]['xml'].replace('Invoice-2', 'Invoice-9')))

    def test_decimal(self):
        self.assertTrue(c.validate(self.config['documents'][0]['xml'].replace('>50<', '>NaN<')))

    def test_date(self):
        self.assertTrue(c.validate(self.config['documents'][0]['xml'].replace('2026-01-01', '2026-99-99')))

    def test_root_tax(self):
        xml = self.config['documents'][0]['xml']
        pos = xml.index('</cac:InvoiceLine>')
        xml = xml[:pos] + xml[pos:].replace('>20<', '>21<', 1)
        self.assertTrue(any((f['rule'] == 'TAX_SUM' for f in c.validate(xml))))
if __name__ == '__main__':
    unittest.main()
