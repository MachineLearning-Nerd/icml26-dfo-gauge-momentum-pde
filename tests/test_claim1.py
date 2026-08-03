import json,subprocess,sys
subprocess.check_call([sys.executable,'src/claim1_gauge_toy.py'])
x=json.load(open('outputs/claim1_gauge_toy/summary.json'));assert x['dfo_residual_norm']==0 and x['nullspace_momentum']==[0.,0.,5.]
