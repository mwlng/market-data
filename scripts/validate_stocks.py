#!/usr/bin/env python3
"""
Validate sql/insert_stocks.sql for common metadata issues:
- parse inserts and extract (symbol, exchange, currency, industry, sector, short_name, description)
- report duplicate symbols
- report short_names reused across multiple symbols
- report identical descriptions used by multiple symbols
- report rows where short_name is not mentioned in description (heuristic)

Run from repo root: python3 scripts/validate_stocks.py
"""
from pathlib import Path
import re
import sys
from collections import defaultdict

SQL_PATH = Path(__file__).resolve().parents[1] / 'sql' / 'insert_stocks.sql'

INSERT_RE = re.compile(r"insert into stocks\s*\(([^)]+)\)\s*values\s*\((.*?)\)\s*;", re.I | re.S)
QUOTE_RE = re.compile(r"'((?:[^']|'')*)'")


def parse_sql(path: Path):
    text = path.read_text()
    matches = INSERT_RE.findall(text)
    rows = []
    for cols, vals in matches:
        parts = QUOTE_RE.findall(vals)
        parts = [p.replace("''", "'") for p in parts]
        rows.append(parts)
    return rows


def analyze(rows):
    parsed = []
    for parts in rows:
        if len(parts) < 7:
            parsed.append({'ok': False, 'parts': parts})
            continue
        symbol = parts[0]
        exchange = parts[1]
        currency = parts[2]
        industry = parts[3]
        sector = parts[4]
        short_name = parts[5]
        description = parts[6]
        parsed.append({'ok': True, 'symbol': symbol, 'exchange': exchange, 'currency': currency,
                       'industry': industry, 'sector': sector, 'short_name': short_name, 'description': description})

    symbols = [p['symbol'] for p in parsed if p['ok']]
    dup_symbols = sorted([s for s in set(symbols) if symbols.count(s) > 1])

    short_map = defaultdict(list)
    desc_map = defaultdict(list)
    for p in parsed:
        if not p['ok']:
            continue
        short_map[p['short_name']].append(p['symbol'])
        desc_map[p['description']].append(p['symbol'])

    reused_shorts = {k: v for k, v in short_map.items() if len(v) > 1}
    reused_descs = {k: v for k, v in desc_map.items() if len(v) > 1}

    mismatch = []
    for p in parsed:
        if not p['ok']:
            continue
        sh = p['short_name'].lower()
        desc = p['description'].lower()
        if sh not in desc:
            mismatch.append((p['symbol'], p['short_name']))

    return {
        'total': len(parsed),
        'distinct_symbols': len(set(symbols)),
        'duplicate_symbols': dup_symbols,
        'reused_shorts': reused_shorts,
        'reused_descs': reused_descs,
        'mismatch_short_in_desc': mismatch,
        'parsed': parsed,
    }


def print_report(r):
    print('Validation report for', SQL_PATH)
    print('Total inserts parsed:', r['total'])
    print('Distinct symbols:', r['distinct_symbols'])
    print('Duplicate symbols:', r['duplicate_symbols'])
    print('\nShort names used by multiple symbols:')
    for sh, syms in r['reused_shorts'].items():
        print(f"- {sh}: {syms}")
    print('\nDescriptions reused by multiple symbols (showing symbol lists):')
    for desc, syms in r['reused_descs'].items():
        print(f"- {syms[:10]}... (count {len(syms)})")
    print('\nSymbols where short_name not found in description (heuristic):')
    for s, sh in r['mismatch_short_in_desc']:
        print(f"- {s}: {sh}")


if __name__ == '__main__':
    if not SQL_PATH.exists():
        print('Could not find', SQL_PATH, file=sys.stderr)
        sys.exit(2)
    rows = parse_sql(SQL_PATH)
    report = analyze(rows)
    print_report(report)
    # exit status 0 if no duplicates and no reused shorts, otherwise 1
    if report['duplicate_symbols'] or report['reused_shorts']:
        sys.exit(1)
    sys.exit(0)
