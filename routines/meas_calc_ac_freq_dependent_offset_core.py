# input lookup tables, in Hz
# 10KHz used for modes ACV at ranges 500V and 600V, plus ACuA/mA/A all ranges
mcafdoc_infreq_tbl_10khz = [ 50, 400, 1000, 3000, 5000, 7000, 10000 ]
# 100KHz used for all ACmV ranges
mcafdoc_infreq_tbl_100khz = [ 50, 400, 1000, 10000, 30000, 50000, 70000, 90000, 100000 ]

# correction tables for the above modes and ranges
# first row is used if input <= 5000 counts, second used otherwise
mcafdoc_corr_tbl_acmv50 = [
    [ 0,  3,  0, -2,  1, 18, 47, 81, 100 ],
    [ 0, -5, -1,  7, 40, 70, 90, 98, 100 ]
]

mcafdoc_corr_tbl_acmv500 = [
    [ 0,  1, -1, -2, -1, 15, 45, 82, 100 ],
    [ 0, -2, -1,  3, 19, 40, 65, 88, 100 ]
]

mcafdoc_corr_tbl_acv500 = [
    [ 0, 2, 22, 78, 98, 99, 100 ],
    [ 0, 2, 22, 77, 96, 99, 100 ]
]

mcafdoc_corr_tbl_acv600 = [
    [ 0, 2, 22, 85, 95, 99, 100 ],
    [ 0, 2, 22, 77, 95, 99, 100 ] # second row effectively unused
]

mcafdoc_corr_tbl_acuA = [
  [ 0, -10,  3, 20, 35, 55, 100 ],
  [ 0, -20, -8,  2, 16, 43, 100 ]
]

mcafdoc_corr_tbl_acmA = [
  [ 0, -10,  3, 20, 40, 55, 100 ],
  [ 0, -15, -4,  7, 20, 47, 100 ]
]

# for range 5
decirange_factor = 26
fullrange_factor = 216
decirange_factor_lf = 0
fullrange_factor_lf = 0

# the digits is the meter input
# the four factors are from calibration ROM
# the range is the input range
# the in_freq is the input frequency, in hz
# the return factor is subtracted from the displayed value
# this implements the meas_calc_ac_freq_dependent_offset_core(digits, factor) routine
def func(digits, dr_fact, fr_fact, dr_fact_lf, fr_fact_lf, rang, in_freq):
    # validate conditions for application
    if rang == 5 and digits >= 6000: return 0
    if digits >= 55000: return 0
    if rang >= 8: return 0
    if in_freq <= 50: return 0
    if rang == 2 or rang == 3:
        # call routine specifically for those ranges
        # (later)
        return 0

    if digits <= 5000:
        in_gt_5000 = True
    else:
        in_gt_5000 = False

    # first, find location in appropriate table
    if rang in [0, 1]:
        loctbl = macfdoc_infreq_tbl_100khz
    else:
        loctbl = mcafdoc_infreq_tbl_10khz

    for ti in range(len(loctbl)):
        if loctbl[ti] >= in_freq:
            break

    # determine how far into that range the input is
    size_of_range = loctbl[ti] - loctbl[ti-1]
    dist_into_range = in_freq - loctbl[ti-1]
    frac_into_range = dist_into_range/size_of_range

    # now get the appropriate output table depending on the meas range
    if rang == 0:
        frtbl = mcafdoc_corr_tbl_acmv50[in_gt_5000]
    elif rang == 1:
        frtbl = mcafdoc_corr_tbl_acmv500[in_gt_5000]
    elif rang == 4:
        frtbl = mcafdoc_corr_tbl_acv500[in_gt_5000]
    elif rang == 5:
        frtbl = mcafdoc_corr_tbl_acv600[in_gt_5000]
    elif rang == 6:
        frtbl = mcafdoc_corr_tbl_acuA[in_gt_5000]
    elif rang == 7:
        frtbl = mcafdoc_corr_tbl_acmA[in_gt_5000]

    fr_hi = frtbl[ti]
    fr_lo = frtbl[ti-1]

    corr_val = int((fr_hi-fr_lo)*frac_into_range + 0.5) + fr_lo

    corr_val_decirange = int((dr_fact * corr_val) / 100)
    corr_val_fullrange = int((fr_fact * corr_val) / 100)

    if rang == 5:
        corr_digits_decirange = corr_val_decirange + 600
        corr_digits_fullrange = corr_val_fullrange + 5400
        digits_decirange = 600
    else:
        corr_digits_decirange = corr_val_decirange + 5000
        corr_digits_fullrange = corr_val_fullrange + 45000
        digits_decirange = 5000

    if corr_digits_decirange < digits:
        fr_hi = corr_val_fullrange
        fr_lo = corr_val_fullrange - corr_val_decirange

        x = ((digits - digits_decirange) / corr_digits_fullrange) - 1
        corr_in_range = x * fr_lo
    else:
        fr_hi = 0
        corr_in_range = (digits / digits_decirange) * corr_val_decirange

    return int(corr_in_range) + fr_hi


# now a short little demo to display the effect

def calculate(factor):
    out = np.empty((38900, ))
    for digit in range(0, 389000, 10):
        out[int(digit/10)] = 10 - func(10, factor,
            fullrange_factor, decirange_factor_lf,
            fullrange_factor_lf, 5, digit)
    print(out)
    return out

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, bottom=0.25)
xdigits = np.array(range(0, 389000, 10))
l, = plt.loglog(xdigits, calculate(0)/10)
plt.axis([50, 389000, 0.5, 200])
plt.xlabel("Input Frequency/Hz")
plt.ylabel("Displayed Voltage/V")
plt.title("Decirange Factor effect on 1V input vs. Frequency")

sax = plt.axes([0.15, 0.1, 0.75, 0.03])
sfactor = Slider(sax, 'Factor', -3000, 3000, valinit=0)

def update(val):
    l.set_ydata(calculate(int(val))/10)
    fig.canvas.draw_idle()

sfactor.on_changed(update)

plt.show()