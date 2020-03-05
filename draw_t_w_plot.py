import numpy as np
from matplotlib import pyplot as plt
from math import pi, cos, sin
import pandas as pd

#constants
d8 = 1.55125 * (10**(-10))
d5 = 9.8485 * (10**(-10))
ur = 137.88



plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['lines.linewidth'] = 0.8

def ellipse_blue(u,v,a,b,t_rot):
    t = np.linspace(0, 2*pi, 100)
    Ell = np.array([a*np.cos(t) , b*np.sin(t)])
        #u,v removed to keep the same center location
    R_rot = np.array([[cos(t_rot) , -sin(t_rot)],[sin(t_rot) , cos(t_rot)]])
        #2-D rotation matrix

    Ell_rot = np.zeros((2,Ell.shape[1]))
    for i in range(Ell.shape[1]):
        Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])
    plt.plot(u+Ell_rot[0,:] , v+Ell_rot[1,:],'blue',linewidth = "1.5") #rotated ellipse

def ellipse_red(u,v,a,b,t_rot):
    t = np.linspace(0, 2*pi, 100)
    Ell = np.array([a*np.cos(t) , b*np.sin(t)])
        #u,v removed to keep the same center location
    R_rot = np.array([[cos(t_rot) , -sin(t_rot)],[sin(t_rot) , cos(t_rot)]])
        #2-D rotation matrix
    Ell_rot = np.zeros((2,Ell.shape[1]))
    for i in range(Ell.shape[1]):
        Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])
    plt.plot(u+Ell_rot[0,:] , v+Ell_rot[1,:],'red',linewidth = "1.5") #rotated ellipse


#drow tera-wasserburg concordia curve
tr_x = []
tr_y = []
tmpoints = []
for i in range(5000):
    tm = (i+1)*(10**6)
    tmpoints.append(tm)

for t in  tmpoints:
    px = 1 / (np.exp(d8*t)-1)
    py = 1/ur*(np.exp(d5*t)-1)/(np.exp(d8*t)-1)
    tr_x.append(px)
    tr_y.append(py)

#reading csv
df = pd.read_csv("20200215_twplot.csv")
x = df["238U/206Pb"]
y = df["207Pb/206Pb"]
x_err = df["error"]
y_err = df["error.1"]


print(df["core_rim"])
for i in range(len(x)):
    if df["core_rim"][i] == "core":
        ellipse_blue(x[i],y[i],x_err[i],y_err[i],0)
    elif:
        df["core_rim"][i] == "rim":
        ellipse_red(x[i],y[i],x_err[i],y_err[i],0)
    else:
        ellipse_blue(x[i],y[i],x_err[i],y_err[i],0)


plt.plot(tr_x, tr_y, color = "black")
plt.xlim(0, 80)
plt.ylim(0, 1)
plt.xlabel('$\mathrm{^{238}U/^{206}Pb}$')
plt.ylabel('$\mathrm{^{207}Pb/^{206}Pb}$')
plt.show()
