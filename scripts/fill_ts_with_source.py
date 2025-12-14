#!/usr/bin/env python3
"""
Fill <translation> with the <source> text for TS files where translation is empty or marked unfinished.

Usage:
  python scripts/fill_ts_with_source.py i18n/*.ts

This script edits files in-place. It preserves other XML content and attempts
to remove the `type="unfinished"` attribute when filling translations.
"""
import re
import sys
from pathlib import Path


MSG_RE = re.compile(r"(<message\b.*?>)(.*?)(</message>)", re.DOTALL)
SRC_RE = re.compile(r"<source>(.*?)</source>", re.DOTALL)
TRANS_RE = re.compile(r"<translation( [^>]*)?>(.*?)</translation>", re.DOTALL)


def fill_file(path: Path):
    txt = path.read_text(encoding='utf-8')
    changed = False

    def repl(m):
        nonlocal changed
        head, body, tail = m.group(1), m.group(2), m.group(3)
        src_m = SRC_RE.search(body)
        if not src_m:
            return m.group(0)
        src_text = src_m.group(1)
        trans_m = TRANS_RE.search(body)
        if trans_m:
            trans_attrs = trans_m.group(1) or ''
            trans_text = trans_m.group(2)
            if (not trans_text.strip()) or 'unfinished' in trans_attrs:
                # replace translation with source text, remove unfinished flag
                new_trans = f'<translation>{src_text}</translation>'
                body2 = TRANS_RE.sub(new_trans, body, count=1)
                changed = True
                return head + body2 + tail
            else:
                return m.group(0)
        else:
            # no translation tag present; append one after source
            new_trans = f"\n      <translation>{src_text}</translation>"
            body2 = body.replace('</source>', '</source>' + new_trans, 1)
            changed = True
            return head + body2 + tail

    new_txt = MSG_RE.sub(repl, txt)
    if changed:
        path.write_text(new_txt, encoding='utf-8')
        print(f'Updated: {path}')
    else:
        print(f'No changes: {path}')


def main():
    if len(sys.argv) < 2:
        print('Usage: fill_ts_with_source.py <ts-files>')
        sys.exit(2)
    for pattern in sys.argv[1:]:
        for p in Path('.').glob(pattern):
            if p.is_file():
                fill_file(p)


if __name__ == '__main__':
    main()
