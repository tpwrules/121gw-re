
# table is cal_ohms_50M_factor_tbl
# first 13 entries are an input map
indata = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
# and the second 13 are an output map
outdata = [0, 37, 65, 85, 100, 100, 100, 87, 10, 40, 0, -37, -65]

# the digits is the meter input, from 0 to 55999
# the factor is the application factor, from -3000 to 3000 
# (limited by cal_ohms_50M_offset_factor_validate())
# the return factor is subtracted from the displayed value
# this implements the meas_ohms_calc_50M_offset(digits, factor) routine
def func(digits, factor):
    if digits >= 56000: return 0

    # determine location in the input table
    loc = 0
    for x in range(13):
        if 1000*indata[x] >= digits:
            loc = x
            break

    # determine how far into that range the input is
    digits_into_range = digits - 1000*indata[loc-1]
    digits_in_range = 1000*(indata[loc] - indata[loc-1])
    frac_into_range = digits_into_range/digits_in_range

    # determine the size of the output range
    digits_in_outrange = outdata[loc] - outdata[loc-1]
    # and map the output to it
    digits_out = (frac_into_range * digits_in_outrange) + outdata[loc-1]

    # now multiply by the correction factor and return
    return int(digits_out*factor/100)

# now a short little demo to display the effect

def calculate(factor):
    out = np.empty((56000, ))
    for digit in range(56000):
        out[digit] = digit - func(digit, factor)
    return out

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, bottom=0.25)
xdigits = np.array(range(56000))
l, = plt.plot(xdigits/1000, calculate(0)/1000)
plt.axis([0, 56, 0, 56])
plt.xlabel("Measured Value/MOhm")
plt.ylabel("Displayed Value/MOhm")
plt.title("Calibration Factor Effect on 50MOhm Range Measurements")

sax = plt.axes([0.15, 0.1, 0.75, 0.03])
sfactor = Slider(sax, 'Factor', -3000, 3000, valinit=0)

def update(val):
    l.set_ydata(calculate(int(val))/1000)
    fig.canvas.draw_idle()

sfactor.on_changed(update)

plt.show()