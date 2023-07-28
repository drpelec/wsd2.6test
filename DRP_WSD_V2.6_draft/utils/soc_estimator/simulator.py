from Battery import *

# Open Testing File
fin = open('sim_glasgow.csv', 'r')

# Battery(Initial SOC, initial time)
cell0 = Battery(SOC_init=95, timestamp=0, P_GAIN=15, I_GAIN=.01, HYST_GAIN=17.45, CORRECTION_INTERVAL=60)

fin.readline()

for line in fin:
    # [t,I,Vt,T,SOC_matlab] = line.split(',')
    [t, I, Vt, T, dummy] = line.split(',')
    SOC_py = cell0.update((eval(Vt) / 10000) - 0.004 * eval(I), eval(I), eval(T), eval(t))
    # fout.write(str(t) + ',' + str(SOC_py) + ',' + str(SOC_matlab) )
    # fout.write(str(t) + ',' + str(SOC_py) + '\n')
    print str(t) + ',' + str(SOC_py)
