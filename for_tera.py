import pandas as pd
import csv
import numpy as np

d8 = 1.55125 * (10**(-10))
d5 = 9.8485 * (10**(-10))
myu = 9.74
ur = 137.88

def pb_common(time):
    return (12.998 + myu/ur * (np.exp(d5*3.7*(10**9)) - np.exp(d5*time)))/(11.152 + myu * (np.exp(d8*3.7*(10**9)) - np.exp(d8*time)))
#pbc46 = 11.152 + myu * (np.exp(d8*3.7*(10**9)) - np.exp(d8*time))
#pbc47 = 12.998 + myu/ur * (np.exp(d5*3.7*(10**9)) - np.exp(d5*time))
def pb_radiogenic(time):
    return (np.exp(d5*time)-1)/(np.exp(d8*time)-1)/137.88
#print(pb_radiogenic(1e+9))

num = int(input("the number of iterative calculation for common-Pb correction: "))

df = pd.read_csv("isotopic_ratio.csv")

x = 1/df["206Pb/238U"]
x_err = df["error"]/df["206Pb/238U"]/df["206Pb/238U"]
y = df["207Pb/206Pb"]
y_err = df["error.3"]

len = len(x)
print(len)

def common_pb_correction(upb, pbpb, upb_err, iterative, list):
    ratio = 1
    for i in range(num):
        print(i+1)
        age = np.log((1+1/upb*ratio))/d8/1e+6
        ratio = 1/((pb_common(age)-pb_radiogenic(age))/(pb_common(age)-pbpb))
        age_corrected = np.log(1/upb*ratio+1)/d8/1e+6
#        for j in range(len):
#            print(ratio[j], age_corrected[j], age[j]-age_corrected[j])
        print("")

    age_err = np.log(1/upb*ratio*(1+ np.sqrt((upb_err/upb)**2 + (y_err/(pb_common(age)-pbpb))**2))+1)/d8/1e+6 - age_corrected
#    for j in range(len):
#        print(age_corrected[j], age_err[j])
    print("")
    list.append(age_corrected)
    list.append(age_err)


ls = []
common_pb_correction(x,y, x_err, num, ls)
#age = np.log((1+1/x))/d8/1e+6
#ratio = 1/((pb_common(age)-pb_radiogenic(age))/(pb_common(age)-y))
#x_corrected_1 = x/ratio
#age_corrected_1 = np.log(1/x*ratio+1)/d8/1e+6

g = open('twplot.csv', 'w')
writer = csv.writer(g, lineterminator='\n')
csvlist = []
csvlist.append("238Pb/206Pb")
csvlist.append("error")
csvlist.append("207Pb/206Pb")
csvlist.append("error")
csvlist.append("common-Pb corrected 206Pb/238U age / Ma")
csvlist.append("error")

writer.writerow(csvlist)

for i in range(len):
    csvlist = []
    csvlist.append(x[i])
    csvlist.append(x_err[i])
    csvlist.append(y[i])
    csvlist.append(y_err[i])
    csvlist.append(ls[0][i])
    csvlist.append(ls[1][i])
    writer.writerow(csvlist)
