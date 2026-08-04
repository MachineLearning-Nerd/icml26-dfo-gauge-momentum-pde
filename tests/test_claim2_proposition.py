import sys
sys.path.insert(0,'src')
from claim2_proposition_a1_toy import row
def test_collision_identity():
 for tau in (.25,.5,1.,2.):
  assert row(tau)['max_abs_error_vs_q'] < 1e-14
