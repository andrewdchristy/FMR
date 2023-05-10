"""
-Kittel fit (Hres vs. freq) for dP/dH curves
-Decides which part of data to use by editing range with np.delete
-Can go between (g, M_eff) and (g, M_eff, H_k) fits by editing Kittel func and parameters
-3 parameter fit requires f^2 (uncomment it in body of code)
"""
# Deleting Hres values that fell outside of swept H-field (problem with fit)
# Also deleting Hres values that are not on the line (manually checked)
index = []
for i in range(len(Hres)):
    if Hres[i] < min(H) or Hres[i] > max(H):
        index.append(i)
    elif freq[i]/Hres[i] > 1.5e7: # decides the section of data being fit
        index.append(i)
    else:
        continue    
Hres = np.delete(Hres, index)
freq = np.delete(freq, index)
dH = np.delete(dH, index)

# Converting Hres to A/m from Oe
Hres = 79.557*Hres 

# Squaring f
#freq = freq**2

# Performing fit        
p0 = [2, 10000]
popt_kittel, pcov = curve_fit(Kittel, Hres, freq, p0 = p0, method = 'lm', maxfev = 20000)
g = popt_kittel[0]
M_eff = popt_kittel[1]
#H_k = popt_kittel[2]

h = 6.626e-34 #J/Hz
b_m = 9.274e-24 # bohr magneton, J/T
gamma = ((g*b_m)/h)*1e-9 #gyromagnetic ratio, GHz/T
M_eff_T = M_eff*(4*np.pi/1e7)
#H_k_T = H_k*(4*np.pi/1e7)
print("Kittel Fit Parameters")
print(f"g-factor = {g}"), print(f"gamma = {gamma} GHz/T"), print(f"mu_0*M_eff = {M_eff_T} T")
#print(f"mu_0*H_k = {H_k_T} T")

# Calculate R^2
R_squared_calc(Hres, freq, Kittel, popt_kittel)

# Define a new x-range for H to continue plot to x = 0
H_extrap = np.linspace(0, 55000, 100)

# Plotting data + fit
fig, ax = plt.subplots()
ax.plot(Hres, freq, 'ko', label = 'Data')
ax.plot(H_extrap, Kittel(H_extrap, *popt_kittel), 'r-', label = 'Fit')
ax.set_xlim(0, 55000)
ax.set_ylim(0, 3.5e9)
ax.set_xlabel('Resonant H-field (A/m)')
ax.set_ylabel('Frequency (Hz)')
ax.set_title('Kittel Plot for TIG Line')
ax.legend()
plt.show()
