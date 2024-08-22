import sys
import time
from test.eeprom import read_fru_eeprom

import adi
import matplotlib.pyplot as plt
import numpy as np

# Optionally passs URI as command line argument,
# else use default ip:analog.local

my_uri = sys.argv[1] if len(sys.argv) >= 2 else "ip:analog.local"
print("uri: " + str(my_uri))

# device connections

ad3552r = adi.ad3552r(uri=my_uri, device_name="ad3552r")

# device configurations

ad3552r.tx_enabled_channels = [0, 1]
ad3552r.tx_cyclic_buffer = False

# signal generation
fs = int(ad3552r.channel[0].sample_rate)
# Signal frequency
fc = 80000
# Number of samples
N = int(fs / fc)
# Period
ts = 1 / float(fs)
# Time array
t = np.arange(0, N * ts, ts)
# Sine generation
samples = np.sin(2 * np.pi * t * fc)
# Amplitude (full_scale / 2)
samples *= (2 ** 15) - 1
# Offset (full_scale / 2)
samples += 2 ** 15
# conversion to unsigned int and offset binary
samples = np.uint16(samples)

print("sample rate:", ad3552r.channel[0].sample_rate)
print("Sample data min:", samples.min())
print("Sample data max:", samples.max())

if ad3552r.tx_cyclic_buffer == True:
	ad3552r.tx([samples, samples])
else:
	for i in range (2):
		ad3552r.tx([samples, samples])

plt.suptitle("AD3552R samples data")
plt.plot(t, samples)
plt.xlabel("Samples")
plt.show()

ad3552r.tx_destroy_buffer()
