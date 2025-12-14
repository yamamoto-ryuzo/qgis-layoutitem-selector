#!/usr/bin/env python3
"""
Compare <source> messages across TS files under geo_report/i18n.
Usage: python scripts/compare_ts_messages.py
"""
import xml.etree.ElementTree as ET
from pathlib import Path

I18N = Path('geo_report') / 'i18n'
files = sorted(I18N.glob('*.ts'))
data = {}
for f in files:
    try:
        tree = ET.parse(f)
        root = tree.getroot()
        sources = [s.text or '' for s in root.findall('.//source')]
        data[f.name] = sources
    except Exception as e:
        print(f'Failed to parse {f}: {e}')

if not data:
    print('No .ts files found in', I18N)
    raise SystemExit(1)

# reference - choose english if present, else first
ref_name = 'geo_report_en.ts' if 'geo_report_en.ts' in data else next(iter(data))
ref = data[ref_name]
ref_set = set(ref)

print(f'Reference: {ref_name} ({len(ref)} messages)')
print()
for name, sources in data.items():
    sset = set(sources)
    extra = sset - ref_set
    missing = ref_set - sset
    print(f'{name}: total={len(sources)} unique={len(sset)} extra={len(extra)} missing={len(missing)}')
    if extra:
        print('  Extra sample (up to 10):')
        for x in list(extra)[:10]:
            print('   -', x)
    if missing:
        print('  Missing sample (up to 10):')
        for x in list(missing)[:10]:
            print('   -', x)
    print()

print('Summary: files with differing message counts:', [n for n,v in data.items() if len(v)!=len(ref)])
