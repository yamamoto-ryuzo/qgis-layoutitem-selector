#!/usr/bin/env python3
"""
Update or create Qt .ts translation files using lupdate.

Defaults:
  lupdate: C:\Qt\linguist_6.9.1\lupdate.exe
  project: geo_report.pro (in repo root)
  i18n dir: ./i18n

This script will run lupdate against the project to update each target
TS file. If lupdate is not found, it will create minimal .ts files as a
fallback so translators can start editing.
"""
import os
import subprocess
import sys

DEFAULT_LUPDATE = r"C:\Qt\linguist_6.9.1\lupdate.exe"

TARGET_LANGS = {
    'en': 'en',
    'fr': 'fr',
    'de': 'de',
    'es': 'es',
    'it': 'it',
    'pt': 'pt',
    'ja': 'ja',
    'zh': 'zh_CN',
    'ru': 'ru',
    'hi': 'hi'
}


def create_minimal_ts(ts_path, lang_code):
    content = f'''<?xml version="1.0" encoding="utf-8"?>
<TS version="2.1" language="{lang_code}">
  <context>
    <name>geo_report</name>
  </context>
</TS>
'''
    with open(ts_path, 'w', encoding='utf-8') as fh:
        fh.write(content)


def update_ts(lupdate_path=None, pro_file=None, i18n_dir=None):
    if lupdate_path is None:
        lupdate_path = DEFAULT_LUPDATE
    if pro_file is None:
        pro_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geo_report.pro')
    if i18n_dir is None:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        i18n_dir = os.path.join(repo_dir, 'geo_report', 'i18n')

    os.makedirs(i18n_dir, exist_ok=True)

    lupdate_exists = os.path.exists(lupdate_path)

    rc = 0
    for short, lang_code in TARGET_LANGS.items():
        ts_name = f'geo_report_{short}.ts'
        ts_path = os.path.join(i18n_dir, ts_name)
        if lupdate_exists:
            print(f'Running lupdate for {ts_name}...')
            try:
                # Use the .pro file if available, otherwise scan current dir
                if os.path.exists(pro_file):
                    subprocess.check_call([lupdate_path, pro_file, '-ts', ts_path])
                else:
                    subprocess.check_call([lupdate_path, '.', '-ts', ts_path])
            except subprocess.CalledProcessError as e:
                print(f'lupdate failed for {ts_name}: {e}')
                rc = 2
        else:
            if os.path.exists(ts_path):
                print(f'{ts_name} already exists; skipping lupdate fallback creation')
            else:
                print(f'lupdate not found, creating minimal {ts_name}')
                create_minimal_ts(ts_path, lang_code)

    return rc


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description='Generate/update .ts translation files')
    p.add_argument('--lupdate', help='Path to lupdate executable', default=None)
    p.add_argument('--pro', help='Path to .pro project file', default=None)
    p.add_argument('--i18n', help='Path to i18n directory', default=None)
    args = p.parse_args()

    rc = update_ts(args.lupdate, args.pro, args.i18n)
    sys.exit(rc)
