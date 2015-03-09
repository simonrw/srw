from astropy.io import fits
from astropy import units as u
import argparse
import numpy as np
import IPython

from .logs import get_logger
from .constants import pixel_scale
from .lightcurve import Lightcurve

logger = get_logger(__name__)


def sort_by_distance(ra, dec):
    def __inner(lc):
        return np.sqrt(
                (lc.ra - ra) ** 2 +
                (lc.dec - dec) ** 2)


def find_object(filename, ra, dec, toler=5 * u.pix, best_only=False):
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

    objects = [Lightcurve.from_file(filename, obj_id=value)
            for value in obj_id[ind]]
    if best_only:
        return sorted(objects, key=sort_by_distance(ra, dec))[0]
    else:
        return objects


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-r', '--ra', required=True, type=float)
    parser.add_argument('-d', '--dec', required=True, type=float)
    parser.add_argument('--best-only', required=False, action='store_true',
            default=False, help='Only fetch the closest match')
    return parser.parse_args()


def main():
    args = get_args()
    if args.best_only:
        lc = find_object(args.filename, args.ra, args.dec, best_only=True)
    else:
        objects = find_object(args.filename, args.ra, args.dec)
    IPython.embed()

