import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import pandas as pd
import scipy.signal as signal

def dPdH(H, dH, Hres, k1, k2, b):
    return k1*((2*dH*(H - Hres))/(((H - Hres)**2) + dH**2)**2) - k2*((dH**2 - (H - Hres)**2)/(((H - Hres)**2) + dH**2)**2) + b

def R_squared_calc(x, y, func, popt):
    square_residuals = np.sum(np.square(y - func(x, *popt)))
    total_squares = np.sum(np.square(y - np.mean(y)))
    R_squared = 1 - (square_residuals/total_squares)
    print("R^2 = {:.4f}".format(R_squared))
    print("\n")
    return R_squared

def Kittel(Hres, g, M_eff):
    mu_0 = 1.2566e-6 # T*m/A
    h = 6.626e-34 #J/Hz
    b_m = 9.274e-24 # bohr magneton, J/T
    return (((g*b_m*mu_0)/(h)))*((M_eff + Hres)*(Hres))**(1/2)

def LLG_linear(f, alpha, dH_0):
    return dH_0 + (4*np.pi*alpha*f)/(gamma*2*np.pi)

os.chdir(r"C:\Users\achri\Desktop\python stuff")
print("directory changed")

file_name = input("Enter file signifier: ")
print("\n")

data = pd.read_csv(f"{file_name}.csv")
data = np.array(data)

dHlist = []
Hreslist = []
freqlist = []

freq = data[0, 1:]

"""
-Fitting data to derivative of asymmetric Lorentzian (dP/dH)
-Attempts to find peaks, then uses that to center curve fit
"""
for i in range(1, len(freq)):
    H = 671.7*data[4:, 0] # Converting from instrument current to Oe
    P = data[4:, i]/max(data[4:, i])
#   print(f"{freq[i]/1e9} GHz")
    peaks = signal.find_peaks(P, height=0.1, distance=10)
#   print(len(H[peaks[0]]))
    
#   fig, ax = plt.subplots()
#   ax.plot(H, P, 'ko')
    
    for j in range(len(peaks[0])):
        p0 = [20, H[peaks[0][j]], 1, 1, 0.2]
        popt, pcov = curve_fit(dPdH, H, P, p0=p0, maxfev = 20000)
        dHlist.append(popt[0])
        Hreslist.append(popt[1])
        freqlist.append(freq[i])
#       ax.plot(H, dPdH(H, *popt), 'r-')
#       ax.set_title(f"Normalized Absorption for {freq[i]/1e9} GHz")
#       plt.show()

Hres = np.asarray(Hreslist)
freq = np.asarray(freqlist)
dH = np.asarray(dHlist)

fig, ax = plt.subplots()
ax.plot(Hres, freq, 'ko')
ax.set_title("Full Kittel Plot")
ax.set_xlabel("H-field (Oe)")
ax.set_ylabel("Frequency (Hz)")
ax.axis([0, 700, 1e9, 5e9])
plt.show()
