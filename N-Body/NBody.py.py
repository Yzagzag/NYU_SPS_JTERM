import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
'''
NATURAL UNITS:  Distance [AU], Time [Years], Mass [Solar Masses]
'''

nbodies = 4
pi = np.pi
G = 4*pi**2
M_sun = 13
m_earth = 1e-6
m_moon = 1e-9
m_jupiter = 0
d_earth = 1
d_moon = 1e-2
d_jupiter = 2
#circular orbits!
v_earth  = np.sqrt(G*M_sun/d_earth)
v_moon = v_earth + np.sqrt(G*m_earth/d_moon)
v_jupiter = np.sqrt(G*M_sun/d_jupiter)

#integration parametsr
duration = 5
nsteps = 100000
dt = duration/nsteps
#initial conditions
r = np.zeros([nsteps, 3*nbodies])
v = np.zeros([nsteps, 3*nbodies])
a = np.zeros([nsteps, 3*nbodies])
m = [M_sun, m_earth, m_moon, m_jupiter]

r[0] = [0, 0, 0, d_earth, 0, 0, -1.00001*d_earth, 0, 0, d_jupiter, 0, 0]
v[0] = [0, 0, 0, 0, v_earth, 0, 0, -1.000005*v_earth, 0, 0, v_jupiter, 0]
#loop to calculate initial accelerations
for j in range(nbodies):
	for k in range(nbodies):
		if j != k:
			dr = r[0, j*3:j*3 + 3] - r[0, k*3:k*3 + 3]
			R_mag = np.sqrt(sum(dr*dr))
			a[0, j*3:j*3 + 3] = a[0, j*3:j*3 + 3] + -G*m[k]*dr/R_mag**3

#start integrating!
for i in range(1, nsteps):
	for j in range(nbodies):
		r[i, j*3:j*3 + 3] = r[i-1, j*3:j*3 + 3] + v[i-1, j*3: j*3 + 3]*dt
		v[i, j*3:j*3 + 3] = v[i-1, j*3:j*3 + 3] + a[i-1, j*3:j*3 + 3]*dt
	for j in range(nbodies):
		for k in range(nbodies):
			if j != k:
				dr = r[i, j*3:j*3 + 3] - r[i, k*3:k*3 + 3]
				R_mag = np.sqrt(sum(dr*dr))
				a[i, j*3:j*3 + 3] = a[i, j*3:j*3 + 3] + -G*m[k]*dr/R_mag**3
#plotting!
fig, ax = plt.subplots()
ax.plot(r[:, 0], r[:, 1])
ax.plot(r[:, 3], r[:, 4])
ax.plot(r[:, 6], r[:, 7])
ax.plot(r[:, 9], r[:, 10])
ax.set(xlim = (-3, 3), ylim=(-3, 3))
plt.axis('equal')
plt.show()
