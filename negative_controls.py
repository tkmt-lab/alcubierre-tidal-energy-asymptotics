"""Reject altered table cells/rows and rational data without using hashes."""
from pathlib import Path
from decimal import Decimal
import json,re,shutil,subprocess,sys,tempfile
from check_packet import ROOT,require,env,temporary_root
DATA=('rational-intervals.json','FINITE-EXAMPLES.md','table.tex','constant-check.json','bibliography.tex','REFERENCES.md')
def call(data):
    return subprocess.run([sys.executable,'-B',str(ROOT/'verify.py'),'--data-dir',str(data)],env=env(),capture_output=True,text=True,timeout=60)
def main():
    require(__debug__,'optimized Python is refused');out=[]
    with tempfile.TemporaryDirectory(prefix='negative-',dir=temporary_root()) as td:
        d=Path(td)
        for name in DATA:shutil.copyfile(ROOT/name,d/name)
        table=(ROOT/'table.tex').read_text()
        bad,n=re.subn(r'(&\s*)(\d+\.\d+)',lambda m:m[1]+str(Decimal(m[2])+1),table,count=1)
        require(n==1,'negative control could not locate decimal cell')
        (d/'table.tex').write_text(bad)
        r=call(d);require(r.returncode!=0 and 'table.tex differs' in r.stderr,'changed decimal cell accepted')
        out.append({'case':'changed_table_decimal','rejected':True})
        lines=table.splitlines(True);idx=next(i for i,s in enumerate(lines) if ' & 128 & ' in s)
        (d/'table.tex').write_text(''.join(lines[:idx]+lines[idx+1:]))
        r=call(d);require(r.returncode!=0 and 'table.tex differs' in r.stderr,'missing table row accepted')
        out.append({'case':'missing_table_row','rejected':True})
        (d/'table.tex').write_text(table)
        j=json.loads((ROOT/'rational-intervals.json').read_text());j['rows'][0]['scaled_infimum_hi']='0'
        (d/'rational-intervals.json').write_text(json.dumps(j,indent=2)+'\n')
        r=call(d);require(r.returncode!=0 and 'rational-intervals.json differs' in r.stderr,'changed rational bound accepted')
        out.append({'case':'changed_rational_bound','rejected':True})
    r=subprocess.run([sys.executable,'-O',str(ROOT/'verify.py')],env=env(),capture_output=True,text=True,timeout=60)
    require(r.returncode!=0 and 'optimized Python is refused' in r.stderr,'optimized Python accepted')
    out.append({'case':'optimized_Python','rejected':True})
    return {'status':'PASS','cases':out,'corrupt_data_cases':3,'hash_manifest_used_for_rejection':False}
if __name__=='__main__':print(json.dumps(main(),indent=2))
