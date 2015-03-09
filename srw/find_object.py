from astropy.io import fits
from astropy import units as u

from .logging import get_logger
from .constants import pixel_scale
from .lightcurve import Lightcurve

logger = get_logger(__name__)


def find_object(filename, ra, dec, toler=5 * u.pix):
    '''
    Find an object from a campaign file, with a given position in ra, dec
    and tolerence in pixels.
    '''
    catalogue = fits.getdata(filename, 'catalogue')
    ra_arr, dec_arr, obj_id = (catalogue['ra'], catalogue['dec'],
            catalogue['obj_id'])
    toler_degrees = (toler * pixel_scale).to(u.degree).value

    ra_ind = (ra_arr > ra - toler_degrees) & (ra_arr < ra + toler_degrees)
    dec_ind = (dec_arr > dec - toler_degrees) & (dec_arr < dec + toler_degrees)
    ind = ra_ind & dec_ind

    return [Lightcurve.from_file(filename, obj_id=value)
            for value in obj_id[ind]]
