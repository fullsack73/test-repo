import numpy as np
import matplotlib.pylab as plt
import matplotlib

x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Look, a Sine function")
plt.show()