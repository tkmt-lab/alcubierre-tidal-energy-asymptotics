"""Offline distribution integrity, claim metadata and PDF inspection."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
IGNORED={'.git','build','.check-tmp','__pycache__'}
def require(ok,message):
    if not ok: raise RuntimeError(message)
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
        and not any(x in IGNORED for x in p.relative_to(ROOT).parts)
        and p.name not in ('MANIFEST.sha256','.DS_Store') and p.suffix!='.pyc')
def manifest():return ''.join(sha(p)+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files())
def env():
    e=os.environ.copy();e.pop('PYTHONOPTIMIZE',None)
    e.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    return e
def temporary_root():
    p=ROOT/'.check-tmp';p.mkdir(exist_ok=True);return p
def main(write=False):
    require(__debug__,'optimized Python is refused')
    require(all(not p.is_symlink() for p in files()),'symlink is not allowed')
    if write:
        (ROOT/'MANIFEST.sha256').write_text(manifest());return {'status':'MANIFEST_WRITTEN','files':len(files())}
    require((ROOT/'MANIFEST.sha256').read_text()==manifest(),'distribution file membership/hash mismatch')
    for item in load(ROOT/'provenance.json')['exported_inputs']:
        p=ROOT/item['path'];require(p.stat().st_size==item['exported_bytes'] and sha(p)==item['exported_sha256'],'export provenance: '+item['path'])
    pattern=re.compile('|'.join(r'/'+x+r'/' for x in ('Users','Volumes','home','root'))+
                       r'|[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}|BEGIN '+r'(?:RSA |OPENSSH )?PRIVATE KEY|\.ts\.net\b')
    for p in files():
        if p.suffix!='.pdf':require(not pattern.search(p.read_text()),'private/local identifier in '+p.name)
    pdftext=subprocess.check_output(['pdftotext',str(ROOT/'paper.pdf'),'-'],text=True,timeout=30)
    pdfinfo=subprocess.check_output(['pdfinfo',str(ROOT/'paper.pdf')],text=True,timeout=30)
    require(not pattern.search(pdftext+pdfinfo),'private/local identifier in PDF')
    require('(version 1.2)' in pdftext,'PDF version mismatch')
    require(re.search(r'Pages:\s+9\b',pdfinfo),'PDF page-count mismatch')
    require('61000' in pdftext and 'existential error constants' in pdftext,'PDF claim or Lean qualifier missing')
    c=load(ROOT/'claims.json')
    require(c['paper_version']=='1.2','claim version')
    require(c['explicit_error_constants']=={'eta_0':128,'B_minus':5,'B_plus':61000},'claim constants')
    require(c['model']=='Stationary comoving Alcubierre metric, one-component shift, v=1/10','fixed model')
    require(c['parameters']['R']=='[3/2,3]' and c['parameters']['eta']=='>=128','claim parameter range')
    require(not c['formalization']['theorem_formally_proved'] and not c['human_peer_review'],'assurance metadata')
    require(not c['formalization']['explicit_constants_in_lean_statement'],'Lean strength metadata')
    for name in c['evidence']:require((ROOT/name).is_file(),'missing evidence '+name)
    prior=load(ROOT/'lean-check.json')
    require(prior['statement_sha256']==sha(ROOT/'MainStatement.lean') and prior['returncode']==0,'prior Lean record')
    cite=load(ROOT/'cite-check.json')
    require(cite['summary']=={'一致':15,'不一致':0,'解決できない':0},'saved bibliography check')
    require(cite['input']['sha256']==sha(ROOT/'REFERENCES.md'),'citation input hash')
    require(load(ROOT/'.zenodo.json')['version']=='1.2','deposit metadata version')
    require('version: "1.2"' in (ROOT/'CITATION.cff').read_text(),'CFF version')
    require((ROOT/'paper.tex').read_text().count('VERIFICATION-RECORD.md')==1,'verification-record reference')
    return {'status':'PASS','files':len(files()),'pdf_pages':9,'saved_citations':15,
            'formal_proof':False,'fresh_Lean_run':False}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write-manifest',action='store_true');a=ap.parse_args()
    print(json.dumps(main(a.write_manifest),indent=2))
