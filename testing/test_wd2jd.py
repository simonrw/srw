import numpy as np

from srw import ctx

def test_reference():
    expected = 2453005.5
    assert np.isclose(ctx.wd2jd(0.), expected)
