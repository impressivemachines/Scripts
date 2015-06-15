from scipy import optimize
from scipy import linalg
import scipy as sp
import numpy as np
import sys

# this code expects a space separated file of triplets of readings for x,y,z axes from an accelerometer
# or magnetometer, e.g.
# 1149 86 9115
# 1147 63 9084
# 1114 40 9124
# 1082 61 9112
# 1128 57 9094
# 1124 33 9091
#
# you should gather a few hundred readings while turning the sensor around in multiple different orientations
# for accelerometers you should turn it very carefully and not shake the unit so as to avoid adding
# any acceleration that is not from the earth's gravity vector

if len(sys.argv)!=2:
	print "usage: python calibrate.py data_file"
	sys.exit()
	
data = open(sys.argv[1])

def get_min_max_guess(meas, scale):
	max_meas = meas[:, :].max(axis=0)
	min_meas = meas[:, :].min(axis=0)
	n = (max_meas + min_meas) / 2
	sf = 2*scale/(max_meas - min_meas)
	return np.array([n[0], n[1], n[2], sf[0], sf[1], sf[2]])

def scale_measurements(meas, p):
	l_norm = []
	for m in meas[:, ]:
		sm = (m - p[0:3])*p[3:6]
		l_norm.append(linalg.norm(sm))
	return np.array(l_norm)

def err_func(params):
	scaled_data = scale_measurements(imu_array, params)
	err = sp.ones(len(imu_array)) - scaled_data
	return err

imu = []
for line in data:
	v = line.split()
	imu.append([float(v[0]),float(v[1]),float(v[2])])

n = len(imu)
print n,"data points loaded"
if n<10:
	print "too few data points for optimization"
	sys.exit()

imu_array = np.array(imu)
param0 = get_min_max_guess(imu_array,1.0)

#print imu_array
print "starting params (initial guess)"
print " offsets = (",param0[0],param0[1],param0[2],")"
print " scales = (",param0[3],param0[4],param0[5],")"
print " gains = (",1.0/param0[3],1.0/param0[4],1.0/param0[5],")"
print " error = ", linalg.norm(err_func(param0))

paramsfinal,ok = optimize.leastsq(err_func, param0)

print "final params (after optimization)"
print " offsets = (",paramsfinal[0],paramsfinal[1],paramsfinal[2],")"
print " scales = (",paramsfinal[3],paramsfinal[4],paramsfinal[5],")"
print " gains = (",1.0/paramsfinal[3],1.0/paramsfinal[4],1.0/paramsfinal[5],")"
print " error = ", linalg.norm(err_func(paramsfinal))

