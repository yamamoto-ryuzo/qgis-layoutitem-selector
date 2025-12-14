#!/usr/bin/env python3
"""
Compile Qt .ts translation files to .qm using lrelease.

By default this script uses:
  C:\Qt\linguist_6.9.1\lrelease.exe

It looks for .ts files under the `i18n/` directory next to this script
and writes corresponding .qm files into the same directory.
"""
import os
import subprocess
import sys


DEFAULT_LRELEASE = r"C:\Qt\linguist_6.9.1\lrelease.exe"


def compile_ts_files(lrelease_path=None, i18n_dir=None):
    if lrelease_path is None:
        lrelease_path = DEFAULT_LRELEASE
    if i18n_dir is None:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        i18n_dir = os.path.join(repo_dir, 'geo_report', 'i18n')

    if not os.path.exists(lrelease_path):
        print(f"lrelease not found: {lrelease_path}")
        return 2

    if not os.path.isdir(i18n_dir):
        print(f"i18n directory not found: {i18n_dir}")
        return 3

    ts_files = [f for f in os.listdir(i18n_dir) if f.endswith('.ts')]
    if not ts_files:
        print("No .ts files found in i18n/")
        return 0

    rc = 0
    for ts in ts_files:
        ts_path = os.path.join(i18n_dir, ts)
        qm_name = os.path.splitext(ts)[0] + '.qm'
        qm_path = os.path.join(i18n_dir, qm_name)
        print(f"Compiling {ts_path} -> {qm_path}")
        try:
            subprocess.check_call([lrelease_path, ts_path, '-qm', qm_path])
        except subprocess.CalledProcessError as e:
            print(f"lrelease failed for {ts_path}: {e}")
            rc = 4
    return rc


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description='Compile .ts -> .qm using lrelease')
    p.add_argument('--lrelease', help='Path to lrelease executable', default=None)
    p.add_argument('--i18n', help='Path to i18n directory', default=None)
    args = p.parse_args()

    exit_code = compile_ts_files(args.lrelease, args.i18n)
    sys.exit(exit_code)
