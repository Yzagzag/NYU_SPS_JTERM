import numpy as np
import matplotlib.pyplot as plt
#NATURAL UNITS: Distance [AU], Time [Years], Mass [MS]

#constants
pi = np.pi
G = 4*pi**2
M_sun = 1
D_earth = 1
V_earth = 2*pi*D_earth/1

#integration parameters
duration = 2 #T = (4*pi**2)*D_earth^3/2
nsteps = 1000
dt = duration/nsteps

#initialize
r = np.empty([nsteps, 3])
v = np.empty([nsteps, 3])
a = np.empty([nsteps, 3])

#initial conditions!
r[0] = [D_earth, 0, 0]
v[0] = [0, V_earth, 0]
R_mag = np.sqrt(sum(r[0]*r[0]))
a[0] = -G*M_sun*r[0]/R_mag**3

#euler: integrate to move the planet
for i in range(1, nsteps):
	r[i] = r[i-1] + v[i-1]*dt
	v[i] = v[i-1] + a[i-1]*dt
	R_mag = np.sqrt(sum(r[i]*r[i]))
	a[i] = -G*M_sun*r[i]/R_mag**3

fig, (ax1, ax2) = plt.subplots(1, 2, sharey =True)
ax1.plot(r[:, 0], r[:, 1])
ax1.plot(0, 0, 'bo')
ax1.axis('equal')
#movie!
for i in range(0, nsteps):
	ax2.cla()
	ax2.scatter(r[i, 0], r[i, 1])
	ax2.plot(0, 0, 'r*')
	ax2.axis((-1.5, 1.5, -1.5, 1.5))
	plt.pause(1e-20)
plt.show()