import numpy as np
from matplotlib import pyplot as plt
from math import pi, cos, sin
import pandas as pd
from scipy import optimize as opt
from scipy import stats



#constants
d8 = 1.55125 * (10**(-10))
d5 = 9.8485 * (10**(-10))
ur = 137.88




plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 18
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['lines.linewidth'] = 0.8



#error ellipse program based on Noda (2017)
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


def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:, order]

def myEllipse(x, y, sigma_x, sigma_y, cov_xy, conf="none"):
    cov = ([sigma_x ** 2, cov_xy], [cov_xy, sigma_y ** 2])
    vals, vecs = eigsorted(cov)
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    n = 100
    if (vals[0] < 0.0) | (vals[1] < 0.0):
        print("!!! Unable to draw an error ellipse [Data %s] !!!")
        return (np.repeat(0, n), np.repeat(0, n))
    else:
        width, height = 2 * np.sqrt(stats.chi2.ppf(conf, 2)) * np.sqrt(vals)
        tpi = np.linspace(0, 2 * np.pi, n, endpoint=True)
        st = np.sin(tpi)
        ct = np.cos(tpi)
        ell = []
        angle = np.deg2rad(theta)
        sa = np.sin(angle)
        ca = np.cos(angle)
        # p = np.empty((n, 2))
        xelip = x + width / 2 * ca * ct - height / 2 * sa * st
        yelip = y + width / 2 * sa * ct + height / 2 * ca * st
        if len(xelip) > 0:
            print(xelip)
            plt.plot(xelip, yelip, c = "blue")
            return (xelip, yelip)
        else:
            return (np.repeat(0, n), np.repeat(0, n))


#Plotting data on tera-wasserburg concordia curve
filename = input("csvfile\n@")
df = pd.read_csv(filename)
x = df["238U/206Pb"]
y = df["207Pb/206Pb"]
x_err = df["error"]
y_err = df["error.1"]
s = df["error correlation"]
rho = df["error correlation"]*df["error"]*df["error.1"]
for i in range(len(x)):
    myEllipse(x[i], y[i], x_err[i], y_err[i], rho[i], 0.95)

#regression line (York, 1969)
wx = (x_err)**(-2)
wy = (y_err)**(-2)
ymean = np.sum(y)/len(y)
xmean = np.sum(x)/len(x)
b_init = np.sum((y-ymean)*(x-xmean))/np.sum((x-xmean)*(x-xmean))
def z(b):
    return (wx*wy)/((b**2)*wy+wx-2*b*r*np.sqrt(wx*wy))
def x_ave(b):
    return np.sum(z(b)*x)/np.sum(z(b))
def y_ave(b):
    return np.sum(z(b)*y)/np.sum(z(b))
def u(b):
    return x - x_ave(b)
def v(b):
    return y - y_ave(b)
alpha = np.sqrt(wx*wy)
r = s
def calc(b):
    return (b**2)*np.sum((z(b)**2)*(u(b)*v(b)/wx-r*(u(b)**2)/alpha))+b*np.sum((z(b)**2)*(u(b)**2/wy-v(b)**2/wx))-np.sum((z(b)**2)*(u(b)*v(b)/wy-r*(v(b)**2)/alpha))
b_reg = opt.fsolve(calc,b_init)
a = y_ave(b_reg)-b_reg*x_ave(b_reg)
print(a, b_reg)

def residual(b):# S
    return np.sum(z(b)*((y-b*x-a)**2))

def sigma_b(b):
    return np.sqrt(1.0 / np.sum(z(b) * (u(b) ** 2)))

def sigma_a(b):
    #    sigma_ai = np.sum((x**2)*z(b))/np.sum(z(b))/np.sum((u(b)**2)*z(b))
    return np.sqrt(1.0 / np.sum(z(b)) + x_ave(b) ** 2 * sigma_b(b) ** 2)  # York2004ajp




def tw(x):
    return 1/137.88*((1/x+1)**(d5/d8)-1)*x
def reg(x):
    return b_reg*x+a
def intercept(x):
    return reg(x)-tw(x)

x_reg = np.arange(0, 30, 0.1)
y_reg = []
for item in x_reg:
    y_reg.append(item*b_reg+a)



mswd = (residual(b_reg)/(len(x)-2))

print("x_average", x_ave(b_reg))

print("y_average", y_ave(b_reg))
print("a_error", sigma_a(b_reg)*2.093*np.sqrt(mswd))
print("b_error", sigma_b(b_reg)*2.093*np.sqrt(mswd))
print("MSWD", residual(b_reg)/(len(x)-2))

y_reg_upper = []
for item in x_reg:
    y_reg_upper.append(item*b_reg+a+np.sqrt(mswd)*2.093*np.sqrt(sigma_a(b_reg)**2+(sigma_b(b_reg)**2)*item*(item-2*x_ave(b_reg))))

y_reg_lower = []
for item in x_reg:
    y_reg_lower.append(item*b_reg+a-np.sqrt(mswd)*2.093*np.sqrt(sigma_a(b_reg)**2+(sigma_b(b_reg)**2)*item*(item-2*x_ave(b_reg))))


#drow tera-wasserburg concordia curve
tr_x = []
tr_y = []
tmpoints = []
for i in range(10000):
    tm = (i+1)*(10**6)
    tmpoints.append(tm)
for t in  tmpoints:
    px = 1 / (np.exp(d8*t)-1)
    py = 1/ur*(np.exp(d5*t)-1)/(np.exp(d8*t)-1)
    tr_x.append(px)
    tr_y.append(py)

plt.plot(tr_x, tr_y, color = "black")
plt.plot(x_reg, y_reg, color = "black")
plt.plot(x_reg,y_reg_upper, color = "black")
plt.plot(x_reg,y_reg_lower, color = "black")

plt.xlabel('$\mathrm{^{238}U/^{206}Pb}$')
plt.ylabel('$\mathrm{^{207}Pb/^{206}Pb}$')
plt.xlim(0, 6)
plt.ylim(0, 1)
plt.tight_layout()
#plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=1)
plt.show()
