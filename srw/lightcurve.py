from astropy.io import fits
import numpy as np

from .logging import get_logger


class Lightcurve(object):

    logger = get_logger('Lightcurve')

    def __init__(self):
        self.phase = None

    def compute_phase(self, period, epoch):
        self.phase = ((self.mjd - epoch) / period) % 1

    def __repr__(self):
        return "<Lightcurve obj_id={obj_id}>".format(
            obj_id=self.obj_id)

    def __str__(self):
        return repr(self)

    @classmethod
    def from_file(cls, filename, obj_id):
        with fits.open(filename) as infile:
            obj_id_arr = infile['catalogue'].data['obj_id']
        ind = np.where(obj_id_arr == obj_id)[0][0]
        self = cls._read_file_data(filename, index=ind)
        self.obj_id = obj_id
        return self

    @classmethod
    def _read_file_data(cls, filename, index, extra_imagelist_keys=[],
                        extra_catalogue_data=[]):

        self = cls()
        imagelist_keys = set(['airmass'] + extra_imagelist_keys)
        catalogue_keys = set(['ra', 'dec'] + extra_catalogue_data)

        with fits.open(filename) as infile:
            self.mjd = infile['hjd'].section[index]
            self.flux = infile['flux'].section[index]
            self.fluxerr = infile['fluxerr'].section[index]
            self.ccdx = infile['ccdx'].section[index]
            self.ccdy = infile['ccdy'].section[index]
            imagelist = infile['imagelist'].data
            catalogue = infile['catalogue'].data

        all_keys = ['mjd', 'flux', 'fluxerr', 'ccdx', 'ccdy']

        for key in imagelist_keys:
            try:
                setattr(self, key, imagelist[key])
            except KeyError:
                self.logger.warning(
                    'Cannot find key {} in imagelist'.format(key))
            else:
                all_keys.append(key)

        for key in catalogue_keys:
            try:
                setattr(self, key, catalogue[key])
            except KeyError:
                self.logger.warning(
                    'Cannot find key {} in catalogue'.format(key))
            else:
                all_keys.append(key)

        self.columns = all_keys

        return self

    def __getitem__(self, name):
        return getattr(self, name)
