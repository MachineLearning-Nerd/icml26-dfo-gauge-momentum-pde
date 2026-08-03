import json, pathlib
# J maps parameter velocity to function velocity; null(J) is gauge freedom.
J=((1.,0.,0.),(0.,1.,0.)); residual=(1.,-2.); momentum=(3.,4.,5.)
# minimum-norm DF velocity and exact projection of momentum to null(J)=span(e3)
v_df=(1.,-2.,0.); p_null=(0.,0.,5.); v_dfo=tuple(a+b for a,b in zip(v_df,p_null))
assert tuple(sum(J[i][k]*v_dfo[k] for k in range(3)) for i in range(2))==residual
out={'J':J,'residual':residual,'df_velocity':v_df,'momentum':momentum,'nullspace_momentum':p_null,'dfo_velocity':v_dfo,'df_residual_norm':0.0,'dfo_residual_norm':0.0,'verdict':'toy','scope':'finite exact gauge-projection identity only'}
pathlib.Path('outputs/claim1_gauge_toy').mkdir(parents=True,exist_ok=True)
json.dump(out,open('outputs/claim1_gauge_toy/summary.json','w'),indent=2)
