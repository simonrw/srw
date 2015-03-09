try:
    from unittest import mock
except ImportError:
    import mock
import pytest
from astropy.io import fits
import numpy as np

from srw.find_object import find_object


@pytest.fixture
def ra():
    return 2.3


@pytest.fixture
def dec():
    return 5.2


@pytest.fixture
def catalogue(ra, dec):
    catalogue = {
            'ra': np.array([ra - 1E-4, ]),
            'dec': np.array([dec + 1E-4, ]),
            'obj_id': np.array([1, ]),
            }
    return catalogue


@mock.patch('srw.find_object.Lightcurve')
@mock.patch('srw.find_object.fits.getdata')
def test_stuff(getdata, Lightcurve, catalogue, ra, dec):
    campaign_file = mock.MagicMock()
    getdata.return_value = catalogue

    objects = find_object(campaign_file, ra, dec)
    Lightcurve.from_file.return_value.obj_id = 1
    assert objects[0].obj_id == 1
