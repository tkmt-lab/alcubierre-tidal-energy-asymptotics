"""Identical offline checks for users, CI and the clean-clone preflight."""
import json,subprocess,sys
from check_packet import ROOT,require,env

def main():
    require(__debug__,'optimized Python is refused');out=[]
    for name in ('check_packet.py','verify.py','negative_controls.py','check_packet.py'):
        r=subprocess.run([sys.executable,'-B',str(ROOT/name)],cwd=ROOT,env=env(),capture_output=True,text=True,timeout=120)
        require(r.returncode==0,name+' failed:\n'+r.stdout[-1500:]+r.stderr[-3000:])
        out.append({'check':name,'result':json.loads(r.stdout)})
    return {'status':'PASS','checks':out,'network_requests':0,'new_symbolic_or_Lean_run':False}
if __name__=='__main__':print(json.dumps(main(),indent=2))
