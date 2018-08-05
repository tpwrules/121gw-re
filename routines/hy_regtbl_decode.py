#DCV 50.000

regs =     [   0,   0,0x13,0x8A,   5,0x40,   0,0x4D,0x31,   1,
     0x22,   0,   0,   9,0x28,0xA0,0x80,0xC7,   8,0x2C]

#ACV 50.000
regs = [0xF6,0xDD,   2,0x83,0xF5,0x41,   2,0x4D,0x31,   1,
        0,   0,0x90,   0,0x88,0xB0,0x80,0xC0,0x38,0x2C]

# ACV 50.000 1ms peak

regs = [    0xF6,0xDD,   4,   3,0x52,0x10,0x87,0x25,0x31,0xEC,
        0,   0,   0,   9,0x88,0xA0,0xB0,0xC7,0x38,0x20]

regs = [0,   0,0x14,0x93,0x85,   0,   0,   0,0x55,   0,
        8,   8,   0,0x80,0x80,0x86,0x80,0xD1,   0,0xAC]
def _rb(r, n):
    return (regs[r-0x20] & (1 << n)) > 0

def _rbm(r, s, n):
    v = 0
    for b in range(n+s-1, s-1, -1):
        v <<= 1
        v |= _rb(r, b)
    return v

def _yn(b):
    return "Y" if b else "N"

VSSA = 0
VDDA = 3.6
# PB0: measurement input
# PB1: amps in? (A_IN)
# PB2: connected to PA3 through 100nf cap
# PB3: connected to AGND through 10k resistor
# PB4: connected to OP1O through 1uf cap
# PB5: unconnected
# PB6: ADR3412 1.2V zener
PB6 = 1.2
# PB7: something AC related
# PB8: connected to AGND through 47k resistor

print("11. CLOCK SYSTEM")
print("Oscillator: enabled: {}, selected: {}".format(
    _rb(0x33, 5), not _rb(0x33, 4)))
print("AD2CLK frequency: {}".format(
    "Fsysclk/4" if _rb(0x26, 3) else "Fsysclk/2"))
print("")

print("12.1 VOLTAGE REFERENCE GENERATOR")
print("Bias circuit: enabled: {}".format(_rb(0x31, 6)))
print("REFO buffer: enabled: {}, source: {}".format(
    _rb(0x31, 7),
    "PB<6> ({}V)".format(PB6) if _rb(0x30, 7) else "1.2V bandgap"))
REFO = PB6 if _rb(0x30, 7) else 1.2

print("ADC common (ACM): {}V".format(
    (1.2, 0.9, 1.5, 1.125)[_rb(0x25, 3)<<1+_rb(0x25, 2)]))
print("Voltage reference generator 1: enabled: {}".format(_rb(0x2F, 7)))
AGND = VDDA*(0.5, 0.3, 0.1, "Floating")[_rbm(0x31, 4, 2)]
print("Voltage reference generator 2: AGND={}V".format(AGND))
print("")

print("12.2 ANALOG SWITCH NETWORK")
print("Capacitor array: {} pF".format(0.2*_rbm(0x30, 0, 7)))
print("Input switches:")
for si in range(9, -1, -1):
    print("  PA<{}>: PS: {}, DS: {}, FS: {}, SS: {}".format(
        si,
        _yn(_rb(0x2A+(si>>1), 4*(si & 1)+3)),
        _yn(_rb(0x2A+(si>>1), 4*(si & 1)+2)),
        _yn(_rb(0x2A+(si>>1), 4*(si & 1)+1)),
        _yn(_rb(0x2A+(si>>1), 4*(si & 1)+0)),
    ))

smode = _rbm(0x2F, 0, 4)
if smode & 8:
    print("S switches: CMPO dependent")
else:
    smv = (
        # SGND, SVDD, SVSS, SVSO1, SVSO2, SCP, SCN
        (0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 1 ,0, 0, 0),
        (1, 0, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 1 ,1, 0),
        (0, 0, 1, 0, 1, 0, 1)
    )[smode]

    print("S switches: SGND: {}, SVDD: {}, SVSS: {}, SVSO1: {}, SVSO2: {}, SCP: {}, SCN: {}".format(
        _yn(smv[0]),
        _yn(smv[1]),
        _yn(smv[2]),
        _yn(smv[3]),
        _yn(smv[4]),
        _yn(smv[5]),
        _yn(smv[6])
    ))

def _vds(n):
    n -= 1
    m = (1, 2, 4, 8, 10, 12,
         14, 16, 18, 20, 22,
         24, 26, 28, 32, 34, 35)[n]
    return (m/36*VDDA, "VDS<{}>".format(n+1))

def _vdsc(n):
    n -= 1
    m = (1, 2, 4, 8, 10, 12,
         14, 16, 18, 20, 22,
         24, 26, 28, 32, 34, 35)[n]
    return (m/36*VDDA, "VDSC<{}>".format(n+1))

def _agndp(n):
    if REFO >= 2*AGND:
        m = (60, 61, 62, 63, 65, 70,
            80, 90, 100, 110)[n]/120
        return (m*(REFO-AGND)+(m-1)*(AGND)+AGND,
            "AGNDP<{}>".format(n))
    else:
        m = (0, 2, 4, 6, 10, 20,
             40, 60, 80, 100)[n]
        return ((m/120)*(REFO-AGND) + AGND,
            "AGNDP<{}>".format(n))

def _agndn(n):
    if REFO >= 2*AGND:
        m = (60, 59, 58, 57, 55, 50,
            40, 30, 20, 10)[n]/120
        return (m*(REFO-AGND)+(m-1)*(AGND)+AGND,
            "AGNDN<{}>".format(n))
    else:
        m = (0, 2, 4, 6, 10, 20,
             40, 60, 80, 100)[n]
        return ((-m/120)*(REFO-AGND) + AGND,
            "AGNDN<{}>".format(n))

def _n(n):
    return ("?", n)

def _pb(n):
    ns = "PB<{}>".format(n)
    if n == 0:
        return ("[meas input thru 1meg or so]", ns)
    elif n == 1:
        return ("[amps in (A_IN)?]", ns)
    elif n == 2:
        return ("[PA3 thru 100nf]", ns)
    elif n == 3:
        return ("[AGND thru 10k]", ns)
    elif n == 4:
        return ("[OP1O thru 1uf]", ns)
    elif n == 5:
        return ("unconnected", ns)
    elif n == 6:
        return (PB6, ns)
    elif n == 7:
        return ("[AC something]", ns)
    elif n == 8:
        return ("[AGND thru 47k]", ns)

VREF = 0

if smode & 8:
    print("VREF: CMPO dependent")
else:
    vs = _rbm(0x31, 0, 4)
    VREF, vrn = (_vds(17),
         _vds(16),
         _vds(15),
         _agndp(9),
         _agndp(8),
         _agndp(7),
         _agndp(6),
         _agndp(0),
         _vds(1),
         _vds(2),
         _vds(3),
         _agndn(9),
         _agndn(8),
         _agndn(7),
         _agndn(6),
         _pb(7)
    )[vs]
    print("VREF: {}V ({})".format(VREF, vrn))

print("SDIO: {}".format(_yn(_rb(0x24, 3))))
print("")

print("12.3 OPAMP and Comparator")
print("OPAMP 1")
print("  Enabled: {}".format(_rb(0x32, 3)))
print("  -: {}".format(
    "OP1N" if _rb(0x25, 0) else "OP1O"))
print("  +: {}".format(
    ("SENSE", "FB", "RLU", "AGND",
     "PB<0>", "PB<1>", "PB<2>", "PB<8>")[_rbm(0x32, 0, 3)]))
print("  Chop: {}".format(
    ("Always 0", "1kHz", "2kHz", "Always 1")[_rbm(0x33, 6, 2)]))

print("OPAMP 2")
print("  Enabled: {}".format(_rb(0x32, 7)))
print("  -: {}".format(
    "OP2N" if _rb(0x25, 1) else "OP2O"))
print("  +: {}".format(
    ("SENSE", "FB", "RLU", "AGND",
     "PB<0>", "PB<1>", "PB<2>", "PB<3>")[_rbm(0x32, 4, 3)]))

print("Comparator")
print("  Enabled: {}".format(_rb(0x20, 4)))
INCMP = ("SENSE", "FB", "OP1O", "PB<0>",
         "PB<1>", "RLD", "PB<3>", "PB<4>")[_rbm(0x20, 5, 3)]
print("  Input: {}".format(INCMP))
VRHCMP, vrhcmpn = (
    _vdsc(16),
    _vdsc(13),
    _vdsc(11),
    _vdsc(10),
    _vdsc(9),
    _pb(7),
    _agndp(6),
    _agndp(5),
    _agndp(4),
    _agndp(3),
    _agndp(2),
    _agndp(1),
    _agndp(0),
    _agndn(1)
)[_rbm(0x21, 4, 4)]
print("  Hi voltage (VRHCMP): {}V ({})".format(VRHCMP, vrhcmpn))
VRLCMP, vrlcmpn = (
    _vdsc(2),
    _vdsc(5),
    _vdsc(7),
    _vdsc(8),
    _vdsc(9),
    _vdsc(10),
    _vdsc(11),
    (PB6, "PB<6>"),
    _agndn(6),
    _agndn(5),
    _agndn(4),
    _agndn(3),
    _agndn(2),
    _agndn(1),
    _agndp(0),
    _agndp(1)
)[_rbm(0x21, 0, 4)]
print("  Lo voltage (VRLCMP): {}V ({})".format(VRLCMP, vrlcmpn))
print()

print("12.4 Pre-Filter, ADC input MUX, Temperature Sensor")
print("Pre-Filter")

AD1FP, ad1fpn = (
    _n("SENSE"), _n("FB"),
    _n("RLU"), _n("OP1O"),
    _n("OP2O"), (VDDA, "VDDA"),
    (REFO, "REFO"), (VREF, "VREF"),
    _pb(0), _pb(1),
    _pb(2), _pb(3),
    _pb(4), _pb(5),
    (PB6, "PB<6>"), _pb(7) 
)[_rbm(0x24, 4, 4)]
print("  Positive Input (AD1FP): {}V ({})".format(AD1FP, ad1fpn))

AD1FN, ad1fnn = (
    _n("SENSE"), _n("RLU"),
    (VSSA, "VSSA"), (AGND, "AGND"),
    _pb(2), _pb(3),
    _pb(4), _pb(5)
)[_rbm(0x24, 0, 3)]
print("  Negative Input (AD1FN): {}V ({})".format(AD1FN, ad1fnn))

print("  Resistor: {}".format(
    ("100K", "10K", "0", "[filter disabled]")[_rbm(0x33, 2, 2)]))

print("AD1 Input")
AD1IP, ad1ipn = (
    (AD1FP, "AD1FP"), _n("FB"),
    _n("TS1P"), _n("TS1N")
)[_rbm(0x33, 0, 2)]
AD1IN, ad1inn = (
    (AD1FN, "AD1FN"), _n("RLU"),
    _n("TS2N"), _n("TS2P")
)[_rbm(0x33, 0, 2)]
print("  Positive Input (AD1IP): {}V ({})".format(AD1IP, ad1ipn))
print("  Negative Input (AD1IN): {}V ({})".format(AD1IN, ad1inn))

AD1RH, ad1rhn = (
    _n("FB"), (REFO, "REFO"),
    (VREF, "VREF"), (PB6, "PB<6>"),
    _n("RLU"), (VDDA, "VDDA"),
    (AGND, "AGND"), _n("INVALID")
)[_rbm(0x28, 4, 3)]
AD1RL, ad1rln = (
    _n("RLU"), (AGND, "AGND"),
    _pb(3), _pb(5),
    _n("FB"), (VSSA, "VSSA"),
    (VREF, "VREF"), _n("INVALID")
)[_rbm(0x28, 0, 3)]

print("  Positive Reference (AD1RH): {}V ({})".format(AD1RH, ad1rhn))
print("  Negative Reference (AD1RL): {}V ({})".format(AD1RL, ad1rln))

print("AD2 Input")
AD2IP, ad2ipn = (
    _n("OP1O"), _n("OP2O"),
    _pb(4), _pb(7)
)[_rbm(0x27, 6, 2)]
AD2IN, ad2inn = (
    _n("RLU"), (AGND, "AGND"),
    _pb(3), _pb(5)
)[_rbm(0x27, 4, 2)]

print("  Positive Input (AD2IP): {}V ({})".format(AD2IP, ad2ipn))
print("  Negative Input (AD2IN): {}V ({})".format(AD2IN, ad2inn))

AD2RH, ad2rhn = (
    _n("FB"), (REFO, "REFO"),
    (VREF, "VREF"), _pb(6)
)[_rbm(0x27, 2, 2)]
AD2RL, ad2rln = (
    _n("RLU"), (AGND, "AGND"),
    _pb(3), _pb(5)
)[_rbm(0x27, 0, 2)]

print("  Positive Reference (AD2RH): {}V ({})".format(AD2RH, ad2rhn))
print("  Negative Reference (AD2RL): {}V ({})".format(AD2RL, ad2rln))

print("The meter does not have register data for AD3, \
so its registers are not shown")

# print("AD3 Input")
# AD3IP, ad3ipn = (
#     _n("OP1O"), _n("OP2O"),
#     _pb(4), _pb(7)
# )[_rbm(0x35, 6, 2)]
# AD3IN, ad3inn = (
#     _n("RLU"), (AGND, "AGND"),
#     _pb(3), _pb(5)
# )[_rbm(0x35, 4, 2)]

# print("  Positive Input (AD3IP): {}V ({})".format(AD3IP, ad3ipn))
# print("  Negative Input (AD3IN): {}V ({})".format(AD3IN, ad3inn))
# print("  References shared with AD2")

print()

print("13.1 High resolution ADC (AD1)")
print("  Enabled: {}".format(_rb(0x23, 7)))
print("  Chop mode: {}".format(("VX+Vos", "VX-Vos", "VX", "VX")
    [_rbm(0x22, 3, 2)]))
print("  Input gain: {}x".format(0.9*(1+_rbm(0x25, 4, 2))))
print("  Reference gain: {}x".format((1, "1/3")[_rb(0x23, 4)]))
ad1os = _rbm(0x22, 5, 3)
if ad1os & 4:
    ad1os = -(ad1os & 3)
print("  DC offset: {}".format(0.25*ad1os))
print("  Pos/neg input buffered: {}/{}".format(
    _yn(_rb(0x23, 1)), _yn(_rb(0x23, 0))))
print("  Pos/neg reference buffered: {}/{}".format(
    _yn(_rb(0x23, 3)), _yn(_rb(0x23, 2))))
print("  Oversampling ratio: {}".format(256*(2**_rbm(0x22, 0, 3))))
print()

print("13.2 High Speed ADC, Low Pass Filter, RMS Converter, and Peak Hold")
print("AD2")
print("  Enabled: {}".format(_rb(0x26, 7)))
print("  Chop enabled: {}".format(_rb(0x26, 5)))
print("  Input gain: {}x".format(0.5*(1+_rbm(0x25, 6, 2))))
print("  Reference gain: {}x".format((1, "1/3")[_rb(0x26, 4)]))
print("  Oversampling ratio: {}".format(
    min(1024, 32*(2**_rbm(0x26, 0, 3)))))

print("  Phase (SPHACAL): Not in meter register tables")

print("AD3")
print("  The meter does not have register data for AD3, \
so its registers are not shown")
# print("  Enabled: {}".format(_rb(0x34, 7)))
# print("  Chop enabled: {}".format(_rb(0x34, 5)))
# print("  Input gain: {}x".format(0.5*(1+_rbm(0x35, 2, 2))))
# print("  Reference gain: {}x".format((1, "1/3")[_rb(0x34, 4)]))
# print("  Oversampling ratio: {}".format(
#     min(1024, 32*(2**_rbm(0x26, 0, 3)))))

# print("AD2 register source: {}".format(
#     ("AD2DATA", "AD3DATA")[_rb(0x34, 2)]))

print("Low Pass Filter")
print("  Enabled: {}".format(_rb(0x29, 6)))
# print("  LPF register source: {}".format(
#     ("LPF[AD2DATA]", "LPF[AD3DATA]")[_rb(0x34, 2)]))
print("  Oversampling ratio: {}".format(128*(2**_rbm(0x29, 3, 3))))

print("RMS Converter")
print("  Enabled: {}".format(_rb(0x29, 7)))
# print("  RMS register source (X=AD2, Y=AD3): {}".format(
#     ("sum(X^2)/N", "sum(XY)/N", "sum(Y^2)/N", "sum(Y^2)/N")[
#     2*_rb(0x34, 2)+_rb(0x34, 3)]))

print("Peak Hold")
print(" Enabled: {}".format(_rb(0x29, 2)))
print(" Data source: {}".format(
    ("AD2<18:0>", "AD1<23:5>", "LPF<18:0>", "LPF<18:0>")[_rbm(0x29, 0, 2)]))
print()

print("14. Frequency Counter, CNT and CMP pin")
print("Frequency Counter")
print("  Enabled: {}".format(_rb(0x20, 1)))
print("  Input: {}".format(
    ("ACPO (comparator output)", "PCNTI (CNT pin input)")[_rb(0x20, 3)]))

print("CMP Pin")
print("  Enabled: {}".format(_rb(0x20, 2)))