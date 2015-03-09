import matplotlib.pyplot as plt


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
