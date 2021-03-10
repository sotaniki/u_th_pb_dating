import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 24
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['lines.linewidth'] = 0.8



d8 = 1.55125 * (10**(-10))
d5 = 9.8485 * (10**(-10))
myu = 9.74
ur = 137.88


df = pd.read_csv("stacey_kramers1975.csv")

x = df["206Pb/204Pb"]
y = df["207Pb/204Pb"]

x_galena = []
y_galena = []


x_feldspar = []
y_feldspar = []

x_premordial = []
y_premordial = []

for i in range(len(x)):
    if df["Sample"][i] == "galena":
        x_galena.append(x[i])
        y_galena.append(y[i])
    elif df["Sample"][i] == "feldspar":
        x_feldspar.append(x[i])
        y_feldspar.append(y[i])
    else:
        x_premordial.append(x[i])
        y_premordial.append(y[i])




#def pb_common(time):
#    return (12.998 + myu/ur * (np.exp(d5*3.7*(10**9)) - np.exp(d5*time)))/(11.152 + myu * (np.exp(d8*3.7*(10**9)) - np.exp(d8*time)))
def pbc64_1(time):
    return 9.307 + 7.19 * (np.exp(d8*4.57*(10**9)) - np.exp(d8*time))
def pbc74_1(time):
    return 10.294 + 7.19/ur * (np.exp(d5*4.57*(10**9)) - np.exp(d5*time))



def pbc64_2(time):
    return 11.152 + myu * (np.exp(d8*3.7*(10**9)) - np.exp(d8*time))
def pbc74_2(time):
    return 12.998 + myu/ur * (np.exp(d5*3.7*(10**9)) - np.exp(d5*time))






xlist = []
ylist = []

xlist_2 = []
ylist_2 = []

for i in range(8):
    xlist.append((pbc64_1((45.7-i)*1e+8)))
    ylist.append((pbc74_1((45.7-i)*1e+8)))

for i in range(38):
    xlist.append((pbc64_2((37-i)*1e+8)))
    ylist.append((pbc74_2((37-i)*1e+8)))

#for i in range(45):
#    xlist.append((pbc64_1((45.7-i)*1e+8)))
#    ylist.append((pbc74_1((45.7-i)*1e+8)))


plt.plot(xlist, ylist)
plt.scatter(x_galena, y_galena, label = "Galena")
plt.scatter(x_feldspar, y_feldspar, label = "Feldspar")
plt.scatter(x_premordial, y_premordial, label = "Canyon Diablo troilite")
plt.xlabel('$\mathrm{^{206}Pb/^{204}Pb}$')
plt.ylabel('$\mathrm{^{207}Pb/^{204}Pb}$')
plt.legend()
plt.show()
