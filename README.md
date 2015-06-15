# Scripts
Python scripts for various purposes

## Calibrate
This script is for calibrating accelerometers and magnetometers. It works out the XYZ axis gain and offset based on a file containing a series of measurements. The measurement file is an ASCII file consisting of space separated X, Y, and Z axis readings, one per line. The only command line argument is the filename.

Gather the source data by turning the accelerometer around carefully to get a lot of readings of the normal gravity vector. The script assumes that the acceleration will be one g in some direction, so avoid shaking the sensor and introducing additional acceleration. Gather a few hundred readings taken over thirty seconds or so in various orientations. The same approach can be used with a magnetometer.

The script will perform a least squares fit to the data to get the best gain and offset values according to "reading = gain * accel + offset" for each axis.
