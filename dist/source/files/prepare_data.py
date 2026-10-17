"""Rebuild the demo data from the challenge ZIP (Python 3, standard library)."""
import argparse
import collections
import csv
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('dataset_zip', type=Path, help='Path to the original synthetic microbiology ZIP')
parser.add_argument('--output', type=Path, default=ROOT / 'dist' / 'data.json')
args = parser.parse_args()
with zipfile.ZipFile(args.dataset_zip) as archive:
    def read(name):
        matches = [n for n in archive.namelist() if n.rsplit('/', 1)[-1] == name + '.csv']
        if len(matches) != 1:
            raise ValueError('Expected exactly one ' + name + '.csv')
        return list(csv.DictReader(io.TextIOWrapper(archive.open(matches[0]), encoding='utf-8')))
    cultures, isolates, ast, patients, wards, antibiotics = [read(n) for n in
        ['cultures', 'isolates', 'susceptibility', 'patients', 'wards', 'antibiotics']]
    culture_by_id = {r['culture_id']: r for r in cultures}
    patient_by_id = {r['patient_id']: r for r in patients}
    tests = collections.defaultdict(dict)
    for row in ast:
        if row['result'] not in ('S', 'R'):
            raise ValueError('This prototype only supports the supplied S/R dataset')
        code = row['antibiotic_code']
        if code in tests[row['isolate_id']]:
            raise ValueError('Duplicate antibiotic result for isolate ' + row['isolate_id'])
        tests[row['isolate_id']][code] = int(row['result'] == 'R')
    organisms = sorted({r['organism'] for r in isolates})
    rows = []
    for isolate in isolates:
        culture = culture_by_id[isolate['culture_id']]
        patient = patient_by_id[culture['patient_id']]
        rows.append([isolate['isolate_id'], culture['patient_id'], culture['sample_date'],
            culture['ward_code'], organisms.index(isolate['organism']), culture['specimen'],
            patient['sex'], int(culture['age_years']), tests[isolate['isolate_id']],
            int(isolate['esbl']), int(isolate['mrsa']), culture['culture_id'], isolate['quantity'], int(isolate['vre']), int(isolate['cpe']), culture['admission_date'], patient['home_area'], culture['institution'], culture['ward_type'], culture['result']])
    rows.sort(key=lambda r: (r[2], r[11], r[0]))
    output = {'meta': {'patients': len(patients), 'cultures': len(cultures),
        'isolates': len(isolates), 'tests': len(ast),
        'start': min(r['sample_date'] for r in cultures),
        'end': max(r['sample_date'] for r in cultures)},
        'organisms': organisms, 'wards': wards, 'antibiotics': antibiotics, 'rows': rows}
    rawdir = args.output.parent / 'datasets'
    rawdir.mkdir(parents=True, exist_ok=True)
    for name, records in zip(['cultures','isolates','susceptibility','patients','wards','antibiotics'], [cultures,isolates,ast,patients,wards,antibiotics]):
        columns = list(records[0])
        batches = [records[:len(records)//2], records[len(records)//2:]] if name == 'susceptibility' else [records]
        for index, batch in enumerate(batches, 1):
            filename = f'{name}.part{index}.json' if name == 'susceptibility' else name + '.json'
            (rawdir / filename).write_text(json.dumps({'columns':columns,'rows':[[r[c] for c in columns] for r in batch]},separators=(',',':')),encoding='utf-8')
        with (rawdir / (name + '.csv')).open('w',newline='',encoding='utf-8') as out:
            writer=csv.DictWriter(out,fieldnames=columns);writer.writeheader();writer.writerows(records)
    (rawdir / 'README.md').write_text((ROOT / 'DATA_README.md').read_text(),encoding='utf-8')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, separators=(',', ':')), encoding='utf-8')
print('Prepared', len(rows), 'isolates in', args.output)
