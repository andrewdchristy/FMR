# Make heatmap, put Kittel fitted data on heatmap
H_ax = data[1:, 0]
H_ax = 79.557*671.1*H_ax # Converting instrument current (A) to H-field (A/m)
f_ax = data[0, 1:]
P_data = data[1:, 1:]
P_data = np.transpose(P_data) # The data in .csv form has H on y and f on x

z_min , z_max = np.min(P_data), np.max(P_data) 

fig, ax = plt.subplots()

c = ax.pcolormesh(H_ax, f_ax, P_data, cmap='rainbow', vmin=z_min, vmax=z_max)
ax.plot(H_ax, Kittel(H_ax, *popt_kittel), "r-", label = "fit")
ax.set_title('Heatmap of Absorption for CoFeB/TIG')
ax.set_xlabel('H-field (A/m)')
ax.set_ylabel('Frequency (Hz)')
ax.axis([H_ax.min(), H_ax.max(), f_ax.min(), f_ax.max()])
fig.colorbar(c, ax=ax)
ax.legend()
plt.show()
