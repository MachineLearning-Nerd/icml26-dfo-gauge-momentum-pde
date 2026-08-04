"""Finite algebraic audit of Proposition A.1, not a wave-PDE solver."""
import json, math
from pathlib import Path

def row(tau):
    q=[1.,-1.,1.,-1.]; df=[0.,0.,1.,-1.]; xi=[1.,-1.,0.,0.]
    a=1-math.exp(-2/tau)
    lam=1/a
    mem=[a*x for x in q]
    proj=[a*x for x in xi]
    dfo=[df[i]+lam*proj[i] for i in range(4)]
    return {'tau':tau,'lambda':lam,'memory_factor':a,'dfo_velocity':dfo,'max_abs_error_vs_q':max(abs(dfo[i]-q[i]) for i in range(4))}
if __name__=='__main__':
 out=Path('outputs/claim2_proposition_a1_toy');out.mkdir(parents=True,exist_ok=True)
 rows=[row(t) for t in (.25,.5,1.,2.)]
 summary={'verdict':'toy','scope':'Finite algebraic check of the Proposition A.1 collision identity only; not a PDE solve or theorem verification.','source':'main.tex:649-714','rows':rows,'all_exact':all(r['max_abs_error_vs_q']<1e-14 for r in rows)}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
