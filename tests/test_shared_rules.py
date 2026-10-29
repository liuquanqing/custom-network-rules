import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('renderer', ROOT / 'tools/render_rules.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SharedRules(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'rules/aigc-shared.json').read_text())

    def test_public_export_is_current_and_shared_rules_have_no_group_name(self):
        rules = module.shared_rules(self.data)
        output = module.render(self.data, (ROOT / 'rules/AI.legacy.list').read_bytes())
        self.assertEqual(output, (ROOT / 'AI.list').read_bytes())
        self.assertTrue(all(policy in ('aigc', 'grok') for _, _, policy in rules))
        actual = [x for x in output.decode().splitlines() if x.startswith(('DOMAIN', 'IP-'))]
        for kind, domain, _ in rules:
            self.assertEqual(actual.count(kind + ',' + domain), 1)

    def test_rejects_credentials_urls_groups_and_invalid_domains(self):
        for value in ('https://example.com', '127.0.0.1', 'example.com,OTHER', '*.example.com', 'bad..example', 'Bad.example'):
            bad = copy.deepcopy(self.data)
            bad['sections'][0]['domains'][0] = value
            with self.assertRaises(ValueError):
                module.shared_rules(bad)
        for key, value in (('policy', 'DIRECT'), ('type', 'DOMAIN-KEYWORD')):
            bad = copy.deepcopy(self.data)
            bad['sections'][0][key] = value
            with self.assertRaises(ValueError):
                module.shared_rules(bad)

    def test_removal_and_addition_flow_through_export(self):
        old_rule = self.data['sections'][0]['domains'].pop()
        self.data['sections'][0]['domains'].append('new.example.com')
        output = module.render(self.data, (ROOT / 'rules/AI.legacy.list').read_bytes()).decode()
        self.assertNotIn('DOMAIN,' + old_rule + '\r\n', output)
        self.assertIn('DOMAIN,new.example.com', output)

    def test_duplicate_rules_or_legacy_shadow_copy_are_rejected(self):
        bad = copy.deepcopy(self.data)
        bad['sections'][0]['domains'].append(bad['sections'][0]['domains'][0])
        with self.assertRaises(ValueError):
            module.shared_rules(bad)
        with self.assertRaises(ValueError):
            module.render(self.data, b'DOMAIN,accounts.x.ai\n')

    def test_source_references_cannot_publish_credential_urls(self):
        credential_example = 'https://' + 'example-user:example-value' + '@example.org/docs'
        for value in (credential_example, 'https://example.org/docs?token=example'):
            bad = copy.deepcopy(self.data)
            bad['sources'] = [value]
            with self.assertRaises(ValueError):
                module.shared_rules(bad)

    def test_new_section_is_exported_without_renderer_changes(self):
        self.data['sections'].append({'name': 'future', 'policy': 'aigc', 'type': 'DOMAIN', 'domains': ['new.example.com']})
        output = module.render(self.data, (ROOT / 'rules/AI.legacy.list').read_bytes()).decode()
        self.assertIn('DOMAIN,new.example.com', output)

    def test_cross_policy_suffix_cannot_shadow_login_exceptions(self):
        self.data['sections'] = [self.data['sections'][-1]] + self.data['sections'][:-1]
        with self.assertRaises(ValueError):
            module.shared_rules(self.data)


if __name__ == '__main__':
    unittest.main()
