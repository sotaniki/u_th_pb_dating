import csv
import glob
import numpy as np


list = glob.glob('*.csv')

x = input('monitored uranium isotope 1.235U or 2.238U : ')
t = input('integration time:')



print(list)

if x == "1":
    ls = []
    num = 0
    for i in list:
        if "TRA" in i:
            print(i)
#        if i != "output.csv":
            f = open(i,'r').readlines()
            for line in f:
                a = line.split(',')
                if a[0] != "Raw Data\n":
                    if a[0] != "NICE Results\n":
                        ls.append(a)
                        num = num +1
                    else:
                        break
                else:
                    break
        else:
            continue
    len = int((num-12)/22)
    print(num)
 #   print(ls)
    u235 = []
    th232 = []
    pb208 = []
    pb207 = []
    pb206 = []
    pb204 = []
    hg202 = []

    pb206_u238 = []
    pb207_u235 = []
    pb207_pb206 = []
    pb208_th232 = []
    pb208_pb206 = []




    err_235 = []
    err_232 = []
    err_208 = []
    err_207 = []
    err_206 = []
    err_204 = []
    err_202 = []

    err_pb206_u238 = []
    err_pb207_u235 = []
    err_pb208_th232 = []
    err_pb207_pb206 = []

    err_pb208_pb206 = []




    for i in range(len):
        u_s = float(ls[26+i*22][1])
        u_b = float(ls[15+i*22][1])
        u235.append((u_s-u_b)/1.602e-8)
        err_235.append(np.sqrt((u_s+u_b)/1.602e-8))
        th232.append((float(ls[27+i*22][1])-float(ls[16+i*22][1]))/1.602e-8)
    #    err_232.append(np.sqrt((float(ls[27+i*22][1])+float(ls[16+i*22][1]))/1.602e-8))
        err_232.append(np.sqrt((float(ls[27+i*22][1])-float(ls[16+i*22][1]))/1.602e-8))
        pb208.append((float(ls[28+i*22][1])-float(ls[17+i*22][1]))/1.602e-8)
        err_208.append(np.sqrt((float(ls[28+i*22][1])+float(ls[17+i*22][1]))/1.602e-8))
        pb207.append((float(ls[29+i*22][1])-float(ls[18+i*22][1]))/1.602e-8)
        err_207.append(np.sqrt((float(ls[29+i*22][1])+float(ls[18+i*22][1]))/1.602e-8))
        pb206.append((float(ls[30+i*22][1])-float(ls[19+i*22][1]))/1.602e-8)
        err_206.append(np.sqrt((float(ls[30+i*22][1])+float(ls[19+i*22][1]))/1.602e-8))
        pb204.append((float(ls[31+i*22][1])-float(ls[20+i*22][1]))/1.602e-8)
        err_204.append(np.sqrt((float(ls[31+i*22][1])+float(ls[20+i*22][1]))/1.602e-8))
        hg202.append((float(ls[32+i*22][1])-float(ls[21+i*22][1]))/1.602e-8)
        err_202.append(np.sqrt((float(ls[32+i*22][1])+float(ls[21+i*22][1]))/1.602e-8))

        pb206_u238.append(pb206[i]/u235[i]/137.88)
        err_pb206_u238.append(pb206_u238[i]*np.sqrt(1/pb206[i]+1/(u235[i]*137.88)))
        pb207_u235.append(pb207[i]/u235[i])
        err_pb207_u235.append(pb207_u235[i]*np.sqrt(1/pb207[i]+1/u235[i]))
        pb207_pb206.append(pb207[i]/pb206[i])
        err_pb207_pb206.append(pb207_pb206[i]*np.sqrt(1/pb207[i]+1/pb206[i]))
        pb208_th232.append(pb208[i]/th232[i])
        err_pb208_th232.append(pb208_th232[i]*np.sqrt(1/pb208[i]+1/th232[i]))
        pb208_pb206.append(pb208[i]/pb206[i])
        err_pb208_pb206.append(pb208_pb206[i]*np.sqrt(1/pb208[i]+1/pb206[i]))



    g = open('output.csv', 'w')
    writer = csv.writer(g, lineterminator='\n')


    csvlist = []
    csvlist.append("235U")
    csvlist.append("error")
    csvlist.append("232Th")
    csvlist.append("error")
    csvlist.append("208Pb")
    csvlist.append("error")
    csvlist.append("207Pb")
    csvlist.append("error")
    csvlist.append("206Pb")
    csvlist.append("error")
    csvlist.append("204Pb")
    csvlist.append("error")
    csvlist.append("202Hg")
    csvlist.append("error")
    csvlist.append("206Pb/238U")
    csvlist.append("error")
    csvlist.append("207Pb/235U")
    csvlist.append("error")
    csvlist.append("208Pb/232Th")
    csvlist.append("error")
    csvlist.append("207Pb/206U")
    csvlist.append("error")
    csvlist.append("208Pb/206Pb")
    csvlist.append("error")
    writer.writerow(csvlist)





    for i in range(len):
        csvlist = []
        csvlist.append(u235[i]*137.88*float(t))
        csvlist.append(err_235[i]*137.88*np.sqrt(float(t)))
        csvlist.append(th232[i]*float(t))
        csvlist.append(err_232[i]*np.sqrt(float(t)))
        csvlist.append(pb208[i]*float(t))
        csvlist.append(err_208[i]*np.sqrt(float(t)))
        csvlist.append(pb207[i]*float(t))
        csvlist.append(err_207[i]*np.sqrt(float(t)))
        csvlist.append(pb206[i]*float(t))
        csvlist.append(err_206[i]*np.sqrt(float(t)))
        csvlist.append(pb204[i]*float(t))
        csvlist.append(err_204[i]*np.sqrt(float(t)))
        csvlist.append(hg202[i]*float(t))
        csvlist.append(err_202[i]*np.sqrt(float(t)))
        csvlist.append(pb206_u238[i])
        csvlist.append(err_pb206_u238[i])
        csvlist.append(pb207_u235[i])
        csvlist.append(err_pb207_u235[i])
        csvlist.append(pb208_th232[i])
        csvlist.append(err_pb208_th232[i])
        csvlist.append(pb207_pb206[i])
        csvlist.append(err_pb207_pb206[i])
        csvlist.append(pb208_pb206[i])
        csvlist.append(err_pb208_pb206[i])
        writer.writerow(csvlist)

    g.close()

else:
    ls = []
    num = 0
    for i in list:
        if "TRA" in i:
            print(i)
#        if i != "output.csv":
            f = open(i,'r').readlines()
            for line in f:
                a = line.split(',')
                if a[0] != "Raw Data\n":
                    if a[0] != "NICE Results\n":
                        ls.append(a)
                        num = num +1
                    else:
                        break
                else:
                    break
        else:
            continue

    len = int((num-12)/22)

    u238 = []
    th232 = []
    pb208 = []
    pb207 = []
    pb206 = []
    pb204 = []
    hg202 = []

    pb206_u238 = []
    pb207_u235 = []
    pb207_pb206 = []
    pb208_th232 = []
    pb208_pb206 = []


    err_238 = []
    err_232 = []
    err_208 = []
    err_207 = []
    err_206 = []
    err_204 = []
    err_202 = []
    err_pb206_u238 = []
    err_pb207_u235 = []
    err_pb207_pb206 = []
    err_pb208_th232 = []
    err_pb208_pb206 = []


    for i in range(len):
        u_s = float(ls[26+i*22][1])
        u_b = float(ls[15+i*22][1])
        u238.append((u_s-u_b)/1.602e-8)
        err_238.append(np.sqrt((u_s+u_b)/1.602e-8))
        th232.append((float(ls[27+i*22][1])-float(ls[16+i*22][1]))/1.602e-8)
    #    err_232.append(np.sqrt((float(ls[27+i*22][1])+float(ls[16+i*22][1]))/1.602e-8))
        err_232.append(np.sqrt((float(ls[27+i*22][1])-float(ls[16+i*22][1]))/1.602e-8))
        pb208.append((float(ls[28+i*22][1])-float(ls[17+i*22][1]))/1.602e-8)
        err_208.append(np.sqrt((float(ls[28+i*22][1])+float(ls[17+i*22][1]))/1.602e-8))
        pb207.append((float(ls[29+i*22][1])-float(ls[18+i*22][1]))/1.602e-8)
        err_207.append(np.sqrt((float(ls[29+i*22][1])+float(ls[18+i*22][1]))/1.602e-8))
        pb206.append((float(ls[30+i*22][1])-float(ls[19+i*22][1]))/1.602e-8)
        err_206.append(np.sqrt((float(ls[30+i*22][1])+float(ls[19+i*22][1]))/1.602e-8))
        pb204.append((float(ls[31+i*22][1])-float(ls[20+i*22][1]))/1.602e-8)
        err_204.append(np.sqrt((float(ls[31+i*22][1])+float(ls[20+i*22][1]))/1.602e-8))
        hg202.append((float(ls[32+i*22][1])-float(ls[21+i*22][1]))/1.602e-8)
        err_202.append(np.sqrt((float(ls[32+i*22][1])+float(ls[21+i*22][1]))/1.602e-8))

        pb206_u238.append(pb206[i]/u238[i])
        err_pb206_u238.append(pb206_u238[i]*np.sqrt((err_206[i]/pb206[i])**2+(err_238[i]/u238[i])**2)/np.sqrt(float(t)))
        pb207_u235.append(pb207[i]/u238[i]*137.88)
        err_pb207_u235.append(pb207_u235[i]*np.sqrt((err_207[i]/pb207[i])**2+(err_238[i]/u238[i]*137.88)**2)/np.sqrt(float(t)))
        pb208_th232.append(pb208[i]/th232[i])
        err_pb208_th232.append(pb208_th232[i]*np.sqrt((err_208[i]/pb208[i])**2+(err_232[i]/th232[i])**2)/np.sqrt(float(t)))
        pb207_pb206.append(pb207[i]/pb206[i])
        err_pb207_pb206.append(pb207_pb206[i]*np.sqrt((err_207[i]/pb207[i])**2+(err_206[i]/pb206[i])**2)/np.sqrt(float(t)))
        pb208_pb206.append(pb208[i]/pb206[i])
        err_pb208_pb206.append(pb208_pb206[i]*np.sqrt((err_208[i]/pb208[i])**2+(err_206[i]/pb206[i])**2)/np.sqrt(float(t)))





    g = open('output.csv', 'w')
    writer = csv.writer(g, lineterminator='\n')


    csvlist = []
    csvlist.append("238U")
    csvlist.append("error")
    csvlist.append("232Th")
    csvlist.append("error")
    csvlist.append("208Pb")
    csvlist.append("error")
    csvlist.append("207Pb")
    csvlist.append("error")
    csvlist.append("206Pb")
    csvlist.append("error")
    csvlist.append("204Pb")
    csvlist.append("error")
    csvlist.append("202Hg")
    csvlist.append("error")
    csvlist.append("206Pb/238U")
    csvlist.append("error")
    csvlist.append("207Pb/235U")
    csvlist.append("error")
    csvlist.append("208Pb/232Th")
    csvlist.append("error")
    csvlist.append("207Pb/206U")
    csvlist.append("error")
    csvlist.append("208Pb/206Pb")
    csvlist.append("error")
    writer.writerow(csvlist)



    for i in range(len):
        csvlist = []
        csvlist.append(u238[i]*float(t))
        csvlist.append(err_238[i]*np.sqrt(float(t)))
        csvlist.append(th232[i]*float(t))
        csvlist.append(err_232[i]*np.sqrt(float(t)))
        csvlist.append(pb208[i]*float(t))
        csvlist.append(err_208[i]*np.sqrt(float(t)))
        csvlist.append(pb207[i]*float(t))
        csvlist.append(err_207[i]*np.sqrt(float(t)))
        csvlist.append(pb206[i]*float(t))
        csvlist.append(err_206[i]*np.sqrt(float(t)))
        csvlist.append(pb204[i]*float(t))
        csvlist.append(err_204[i]*np.sqrt(float(t)))
        csvlist.append(hg202[i]*float(t))
        csvlist.append(err_202[i]*np.sqrt(float(t)))
        csvlist.append(pb206_u238[i])
        csvlist.append(err_pb206_u238[i])
        csvlist.append(pb207_u235[i])
        csvlist.append(err_pb207_u235[i])
        csvlist.append(pb208_th232[i])
        csvlist.append(err_pb208_th232[i])
        csvlist.append(pb207_pb206[i])
        csvlist.append(err_pb207_pb206[i])
        csvlist.append(pb208_pb206[i])
        csvlist.append(err_pb208_pb206[i])
        writer.writerow(csvlist)

    g.close()
