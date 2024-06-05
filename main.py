#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sys import argv
import requests
import yaml

class SGParser():
    ERR  = "ERR"
    INFO = "INFO"

    def _log(self, t, msg) -> None:
        print(f"{datetime.now().strftime('%H:%M:%S')} [{t}] {msg}")

    def __init__(self, token: str = None, ruleset: str = None, output: str = None):
        if not token or not output or not ruleset:
            raise SyntaxError
        
        self.output = output
        self.ruleset = ruleset
        self.token = token
        if self.token.startswith("Bearer "):
            self.token = self.token[7:]

    def _parse_ruleset(self) -> list:
        r = requests.get('https://semgrep.dev/api/registry/rulesets/{}'.format(self.ruleset), params={
            'definition':   '1',
            'test_cases':   '1',
        }, headers={
            'authority':        'semgrep.dev',
            'accept':           'application/json',
            'authorization':    f'Bearer {self.token}',
            'user-agent':       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
        if r.status_code == 200:
            return r.json()["rules"]
        self._log(self.ERR, f"failed to parse ruleset (code {r.status_code}): {r.text}")
        return []
    
    def _save_rule(self, rule: dict, init: bool = False) -> None:
        if init:
            with open(self.output, 'w') as f:
                f.write("rules:\n")
            return
        
        with open(self.output, 'a') as f:
            yaml.safe_dump([rule], f)

    def download(self):
        self._save_rule({}, True)
        rules = self._parse_ruleset()
        for i in range(len(rules)):
            self._log(self.INFO, f"saving rule #{i + 1}")
            self._save_rule(rules[i]["definition"]["rules"][0])
        self._log(self.INFO, f"ruleset \"{self.ruleset}\" saved to {self.output}")

def str_presenter(dumper, data):
    if data.count('\n') > 0:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

def main() -> None:
    token   = ""
    ruleset = ""
    output  = ""

    if len(argv) == 4:
        token, ruleset, output = argv[1], argv[2], argv[3]
    
    if len(ruleset) == 0 or len(token) == 0 or len(output) == 0:
        print("Pass parameters in this order: semgrep account token, ruleset name, output file\nExample: python3 main.py eyJ...OnE golang rules.yml\nor change them in code")
        return

    sg = SGParser(
        token   = token,
        ruleset = ruleset,
        output  = output
    )
    sg.download()

if __name__ == "__main__":
    main()