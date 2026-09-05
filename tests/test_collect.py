import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Collector(unittest.TestCase):
    def test_legacy_adapter_scope_and_counts(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'plugins').mkdir()
            (root/'plugins/installed_plugins.json').write_text(json.dumps({'version':2,'plugins':{'a':[],'b':[]}}))
            (root/'settings.json').write_text(json.dumps({'hooks':{'PostToolUse':[{'hooks':[{'type':'command'},{'type':'command'}]}]}}))
            (root/'skills/demo').mkdir(parents=True)
            (root/'skills/demo/SKILL.md').write_text('demo')
            result=subprocess.check_output(['bash',str(ROOT/'collect.sh')],cwd=root,env={**os.environ,'CLAUDE_DIR':str(root)},text=True)
            value=json.loads(result)
            self.assertEqual(value['scope'],'claude-configuration-only')
            self.assertEqual(value['skills']['count'],1)
            self.assertEqual(value['plugins']['count'],2)
            self.assertEqual(value['hooks']['total_entries'],2)
            self.assertFalse(value['headless']['cron_observed'])
            self.assertTrue(value['limitations'])

if __name__=='__main__':
    unittest.main()
