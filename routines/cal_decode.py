import sys
import struct

f = open(sys.argv[1], "rb")

def _og(a, cap=False):
    f.seek(a)
    offset, gain = struct.unpack(">ii", f.read(8))
    if cap:
        gain /= 100000
    else:
        gain /= 1000000
    return offset, gain

def _gw(a):
    f.seek(a)
    return struct.unpack(">h", f.read(2))[0]

def _gl(a):
    f.seek(a)
    return struct.unpack(">i", f.read(4))[0]

print("Misc Factors:")
print("  Internal thermistor: {}".format(_gw(0x2E0)))
print("  HY3131 Frequency: {} Hz".format(_gl(0x104)))
print()

print("DCV")
print("  5.0000V: Offset: {}, Gain: 1/{}".format(*_og(0x70)))
print("  50.000V: Offset: {}, Gain: 1/{}".format(*_og(0x80)))
print("  500.00V: Offset: {}, Gain: 1/{}".format(*_og(0x90)))
print("  1000.0V (and LowZ): Offset: {}, Gain: 1/{}".format(*_og(0xA0)))
print()

print("ACV")
print("  5.0000V: Offset: {}, Gain: 1/{}".format(*_og(0x30)))
print("           Frequency nonlinearity coefficients:")
print("             100kHz: 500mV: {}, 5V: {}".format(_gw(0x38), _gw(0x3A)))
print("             20kHz:  500mV: {}, 5V: {}".format(_gw(0x3C), _gw(0x3E)))
print("  50.000V: Offset: {}, Gain: 1/{}".format(*_og(0x40)))
print("           Frequency nonlinearity coefficients:")
print("             100kHz: 5V: {}, 50V: {}".format(_gw(0x48), _gw(0x4A)))
print("             20kHz:  5V: {}, 50V: {}".format(_gw(0x4C), _gw(0x4E)))
print("  500.00V: Offset: {}, Gain: 1/{}".format(*_og(0x50)))
print("           Frequency nonlinearity coefficients:")
print("             10kHz: 50V: {}, 500V: {}".format(_gw(0x58), _gw(0x5A)))
print("  1000.0V (and LowZ): Offset: {}, Gain: 1/{}".format(*_og(0x60)))
print("           Frequency nonlinearity coefficients:")
print("             10kHz: 60V: {}, 600V: {}".format(_gw(0x68), _gw(0x6A)))
print()
print("1ms Peak: Offset: {}, Gain: 1/{}".format(*_og(0x2D0)))
print()

print("DCmV")
print("  50.000mV: Offset: {}, Gain: 1/{}".format(*_og(0xB0)))
print("  500.00mV: Offset: {}, Gain: 1/{}".format(*_og(0xC0)))
print()

print("ACmV")
print("  50.000mV: Offset: {}, Gain: 1/{}".format(*_og(0xD0)))
print("            Frequency nonlinearity coefficients:")
print("              100kHz: 5mV: {}, 50mV: {}".format(_gw(0xD8), _gw(0xDA)))
print("  500.00mV: Offset: {}, Gain: 1/{}".format(*_og(0xE0)))
print("            Frequency nonlinearity coefficients:")
print("              100kHz: 50mV: {}, 500mV: {}".format(_gw(0xE8), _gw(0xEA)))
print()

print("Temperature: Offset: {}, Gain: 1/{}".format(*_og(0xF0)))
print()

print("Resistance")
print("  50.000Ω: Offset: {}, Gain: 1/{}".format(*_og(0x110)))
print("  500.00Ω (and Continuity): Offset: {}, Gain: 1/{}".format(*_og(0x120)))
print("  5.0000kΩ: Offset: {}, Gain: 1/{}".format(*_og(0x130)))
print("  50.000kΩ: Offset: {}, Gain: 1/{}".format(*_og(0x140)))
print("  500.00kΩ: Offset: {}, Gain: 1/{}".format(*_og(0x150)))
print("  5.0000MΩ: Offset: {}, Gain: 1/{}".format(*_og(0x160)))
print("  50.000MΩ: Offset: {}, Gain: 1/{}".format(*_og(0x170)))
print("            Nonlinearity coefficient: {}".format(_gl(0x178)))
print()

print("Diode: Offset: {}, Gain: 1/{}".format(*_og(0x180)))
print()

print("Capacitance")
print("  10.00nF: Offset: {}, Gain: 1/{}".format(*_og(0x190, cap=True)))
print("  100.0nF: Offset: {}, Gain: 1/{}".format(*_og(0x1A0, cap=True)))
print("  1.000µF: Offset: {}, Gain: 1/{}".format(*_og(0x1B0, cap=True)))
print("  10.00µF: Offset: {}, Gain: 1/{}".format(*_og(0x1C0, cap=True)))
print("  100.0µF: Offset: {}, Gain: 1/{}".format(*_og(0x1D0, cap=True)))
print("  10.00mF: Offset: {}, Gain: 1/{}".format(*_og(0x1E0, cap=True)))
print()

print("ACµVA")
print("  5V*50µA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x300)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x308)))
print("  50V*50µA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x310)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x318)))
print("  5V*500µA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x320)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x328)))
print("  50V*500µA: Volts Offset: {}, Gain: 1/{}".format(*_og(0x330)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x338)))
print()

print("ACmVA")
print("  5V*5mA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x340)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x348)))
print("  50V*5mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x350)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x358)))
print("  5V*50mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x360)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x368)))
print("  50V*50mA: Volts Offset: {}, Gain: 1/{}".format(*_og(0x370)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x378)))
print()

print("ACVA")
print("  5V*500mA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x380)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x388)))
print("  50V*500mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x390)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x398)))
print("  5V*10A:     Volts Offset: {}, Gain: 1/{}".format(*_og(0x3A0)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x3A8)))
print("  50V*10A:    Volts Offset: {}, Gain: 1/{}".format(*_og(0x3B0)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x3B8)))
print()

print("ACµA")
print("  50.000µA: Offset: {}, Gain: 1/{}".format(*_og(0x1F0)))
print("  500.00µA: Offset: {}, Gain: 1/{}".format(*_og(0x200)))
print()

print("DCµA")
print("  50.000µA: Offset: {}, Gain: 1/{}".format(*_og(0x210)))
print("  500.00µA: Offset: {}, Gain: 1/{}".format(*_og(0x220)))
print()

print("ACmA")
print("  5.0000mA: Offset: {}, Gain: 1/{}".format(*_og(0x230)))
print("  50.000mA: Offset: {}, Gain: 1/{}".format(*_og(0x240)))
print()

print("DCmA")
print("  5.0000mA: Offset: {}, Gain: 1/{}".format(*_og(0x250)))
print("  50.000mA: Offset: {}, Gain: 1/{}".format(*_og(0x260)))
print()

print("ACA")
print("  500.00mA: Offset: {}, Gain: 1/{}".format(*_og(0x270)))
print("  5.0000A:  Offset: {}, Gain: 1/{}".format(*_og(0x280)))
print("  10.000A:  Offset: {}, Gain: 1/{}".format(*_og(0x290)))
print()

print("DCA")
print("  500.00mA: Offset: {}, Gain: 1/{}".format(*_og(0x2A0)))
print("  5.0000A:  Offset: {}, Gain: 1/{}".format(*_og(0x2B0)))
print("  10.000A:  Offset: {}, Gain: 1/{}".format(*_og(0x2C0)))
print()


print("DCµVA")
print("  5V*50µA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x3C0)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x3C8)))
print("  50V*50µA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x3D0)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x3D8)))
print("  5V*500µA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x3E0)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x3E8)))
print("  50V*500µA: Volts Offset: {}, Gain: 1/{}".format(*_og(0x3F0)))
print("              Amps Offset: {}, Gain: 1/{}".format(*_og(0x3F8)))
print()

print("DCmVA")
print("  5V*5mA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x400)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x408)))
print("  50V*5mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x410)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x418)))
print("  5V*50mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x420)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x428)))
print("  50V*50mA: Volts Offset: {}, Gain: 1/{}".format(*_og(0x430)))
print("             Amps Offset: {}, Gain: 1/{}".format(*_og(0x438)))
print()

print("DCVA")
print("  5V*500mA:   Volts Offset: {}, Gain: 1/{}".format(*_og(0x440)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x448)))
print("  50V*500mA:  Volts Offset: {}, Gain: 1/{}".format(*_og(0x450)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x458)))
print("  5V*10A:     Volts Offset: {}, Gain: 1/{}".format(*_og(0x460)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x468)))
print("  50V*10A:    Volts Offset: {}, Gain: 1/{}".format(*_og(0x470)))
print("               Amps Offset: {}, Gain: 1/{}".format(*_og(0x478)))
print()