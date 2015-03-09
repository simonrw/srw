import matplotlib.pyplot as plt
from astropy import units as u
from .logs import get_logger

logger = get_logger(__name__)

try:
    import ds9
except ImportError:
    logger.warning('No ds9 package available. '
                   'Related functions are not available')
    no_ds9 = True
else:
    no_ds9 = False


def plot_transiting(lc, period, epoch, ax=None, unit='mjd', colour=None):
    if unit.lower() == 'jd':
        epoch -= 2400000.5

    lc.compute_phase(period, epoch)

    if ax is None:
        ax = plt.gca()

    phase = lc.phase.copy()
    phase[phase > 0.8] -= 1.0

    ax.errorbar(phase, lc.flux, lc.fluxerr, ls='None', marker='None',
                capsize=0., alpha=0.3, color=colour)
    ax.plot(phase, lc.flux, '.', ms=2., color=colour)


def show_on_image(lc, filename, frame_index=0, radius=3 * u.pix):
    if no_ds9:
        raise NotImplementedError("Cannot find module ds9")

    d = ds9.ds9()
    d.set('file {0}'.format(filename))

    x, y = lc.ccdx[frame_index], lc.ccdy[frame_index]
    d.set('region command {{circle {x} {y} {radius}}}'.format(
        x=x, y=y, radius=radius.to(u.pix).value))
    d.set('zoom to 8')
