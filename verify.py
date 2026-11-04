"""Recompute exact finite results in isolation and compare supplied data.
This checker deliberately does not consult the distribution hash manifest.
It verifies the table by regeneration, not by accepting a matching hash.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,shutil,subprocess,sys,tempfile
from check_packet import ROOT,require,load,env,temporary_root

def main(data_dir=ROOT):
    require(__debug__,'optimized Python is refused')
    data_dir=Path(data_dir).resolve()
    expected=['rational-intervals.json','FINITE-EXAMPLES.md','table.tex','constant-check.json','bibliography.tex','REFERENCES.md']
    with tempfile.TemporaryDirectory(prefix='reproduce-',dir=temporary_root()) as td:
        work=Path(td)
        for name in ('reproduce.py','constant_check.py','build_references.py','references.json'):
            shutil.copyfile(ROOT/name,work/name)
        for script in ('reproduce.py','constant_check.py','build_references.py'):
            r=subprocess.run([sys.executable,'-B',str(work/script)],cwd=work,env=env(),capture_output=True,text=True,timeout=60)
            require(r.returncode==0,script+' failed: '+r.stderr[-2000:])
        for name in expected:
            require((data_dir/name).read_bytes()==(work/name).read_bytes(),name+' differs from exact regeneration')
    # Additional arithmetic checks on the supplied rational record, without decimals.
    rows=load(data_dir/'rational-intervals.json')['rows']
    require(len(rows)==18,'expected 18 parameter pairs')
    pairs=set()
    for row in rows:
        d={k:F(v) for k,v in row.items()};R=d['R'];eta=d['eta'];K=d['K'];pairs.add((R,eta))
        require(d['C']==R/(R-1) and K==1/(3*R*(R-1)**3),'coefficient identity')
        lo=d['scaled_infimum_lo'];hi=d['scaled_infimum_hi']
        require(0<lo<K<hi,'finite bounds and coefficient ordering')
        require((K-lo)**2*eta<=25,'explicit lower remainder')
        require((hi-K)*eta<=61000,'explicit upper remainder')
        require(d['I_lo']<=d['I_hi']<=1 and d['family_J_lo']<=d['family_J_hi'],'enclosure ordering')
    require(pairs=={(R,F(eta)) for R in (F(3,2),F(2),F(3)) for eta in (128,512,2048,8192,32768,131072)},'parameter coverage')
    return {'status':'PASS','regenerated_files':expected,'exact_parameter_pairs':18,
            'constant_envelope_checks':15,'numerical_table_checked_without_manifest':True,
            'uniform_theorem_proved_by_this_program':False}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--data-dir',type=Path,default=ROOT);a=ap.parse_args()
    print(json.dumps(main(a.data_dir),indent=2))
