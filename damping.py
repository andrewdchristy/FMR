"""
Making fit for Gilbert damping of TIG line
All (Hres, f) points and their dH for CoFeB were removed in Kittel fitting
"""
# Some linewidths become negative in the fit (I don't know why)
# Magnitudes are correct but the sign is off, so this takes care of it
for i in range(len(freq)):
    dH[i] = np.abs(dH[i])

# Converting f to GHz and dH to T
freq = freq*1e-9
dH = (dH*79.557)*(4*np.pi/1e7)
popt_damping, pcov = curve_fit(LLG_linear, freq, dH, p0 = [0.4, 0.001])
alpha = popt_damping[0]
dH_0 = popt_damping[1]
print("Damping Equation Parameters")
print(f"alpha = {alpha}"), print(f"Inhomogeneous broadening = {dH_0} T")

R_squared_calc(freq, dH, LLG_linear, popt_damping)

# Define a new x-range for f to continue plot to x = 0
freq_extrap = np.linspace(0, 3.5, 50) 

fig, ax = plt.subplots()
ax.plot(freq, dH, 'ko', label="Experimental Data")
ax.plot(freq_extrap, LLG_linear(freq_extrap, *popt_damping), 'r-', label="Linear Fit")
ax.set_title("Gilbert Damping Parameter for TIG Line")
ax.set_xlabel("Frequency (GHz)")
ax.set_ylabel("Linewidth (HWHM) (T)")
ax.set_xlim(0, 3.5)
ax.legend()
plt.show()
