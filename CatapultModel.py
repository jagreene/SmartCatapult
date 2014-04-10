"""Laptop based physics model for our 
smart catapult, has a gui for user input
of desired distance and outputs
positions for the servos and stepper moters"""

import serial
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.integrate import odeint
import time

# ser = serial.Serial('/dev/tty.usbserial', 9600)


def calcCatapultInteractions(thetaA, rA, hA, wA, mA, kS, attachPointS, dA, eqLS, stopAngle):
    iA = mA * (wA ** 2 + hA ** 2) / 12

    xPosS = attachPointS[0]
    yPosS = attachPointS[1]

    omegaA = 0
    y0 = [thetaA, omegaA]
    t = np.linspace(0, .2, 10000)

    def calcAlpha(y, t):
        thetaI = y[0]
        omegaI = y[1]

        xPosA = dA * np.cos(thetaI)
        yPosA = dA * np.sin(thetaI)

        lS = np.sqrt((xPosA - xPosS) ** 2 + (yPosA - yPosS) ** 2)
        thetaS = np.arctan((yPosA - yPosS) / (xPosA - xPosS))

        fS = -kS * (lS - eqLS)
        tA = fS * dA * np.sin(thetaS)

        alpha = tA / iA

        dOmega = alpha
        dTheta = omegaI

        return [dTheta, dOmega]

    soln = odeint(calcAlpha, y0, t)

    thetaF = soln[:, 0]
    omegaF = soln[:, 1]

    thetaF = np.extract(thetaF - stopAngle >= 0, thetaF)
    omegaF = omegaF[:len(thetaF)]
    t = t[:len(thetaF)]

    print "Final Angle = " + str(thetaF)
    print "Final Omega = " + str(omegaF)

    # plt.plot(rA*np.cos(thetaF), rA*np.sin(thetaF), linewidth=2.0)
    # pylab.show()
    plt.plot(t, omegaF)
    plt.title("Angular Velocity over Time")
    plt.xlabel("time")
    plt.ylabel("Angular Velocity (rads/s)")
    plt.figure()
    plt.title("Catapult Tip Trajectory")
    plt.xlabel("Y Position")
    plt.ylabel("X Position")
    plt.plot(rA * np.cos(thetaF), rA * np.sin(thetaF))
    plt.figure()
    plt.title("Catapult Angle over Time")
    plt.xlabel("Time")
    plt.ylabel("Angle")
    plt.plot(t, thetaF)
    plt.show()

    return [thetaF[-1], omegaF[-1]]


def calcProjectileMotion(posI, vI):
    x0 = posI[0]
    y0 = posI[1]

    vx0 = vI[0]
    vy0 = vI[1]

    yI = [x0, y0, vx0, vy0]
    t = np.linspace(0, 5, 5000)

    def calcForces(y, t):

        vxI = y[2]
        vyI = y[3]

        ax = 0
        ay = -9.8

        dx = vxI
        dy = vyI

        dvx = ax
        dvy = ay

        return [dx, dy, dvx, dvy]

    soln = odeint(calcForces, yI, t)
    xf = soln[:, 0]
    yf = soln[:, 1]

    vxf = soln[:, 2]
    vyf = soln[:, 3]

    yf = np.extract(yf >= 0, yf)
    xf = xf[:len(yf)]

    vxf = vxf[:len(yf)]
    vyf = vyf[:len(yf)]

    t = t[:len(yf)]

    print yf

    plt.figure()
    plt.plot(t, xf)
    plt.title("X Distance over Time")
    plt.xlabel("time")
    plt.ylabel("X Distance")
    plt.figure()
    plt.plot(t, yf)
    plt.title("Y Distance over Time")
    plt.xlabel("Time")
    plt.ylabel("Y Distance")
    plt.figure()
    plt.plot(xf, yf)
    plt.title("Trajectory")
    plt.xlabel("X Distance")
    plt.ylabel("Y Distance")
    plt.figure()
    plt.plot(t, vxf)
    plt.title("Vx over Time")
    plt.xlabel("Time")
    plt.ylabel("Vx Distance")
    plt.figure()
    plt.plot(t, vyf)
    plt.title("Vy over Time")
    plt.xlabel("Time")
    plt.ylabel("Vy Distance")
    plt.show()


[thetaF, omegaF] = calcCatapultInteractions(
    np.pi, .35, .01, .05, .25, .25, (.2, .25), .2, 0, 3 * np.pi / 4)

print thetaF
print omegaF
r = .35
vf = abs(omegaF * r)

posI = [r * np.cos(thetaF), r * np.sin(thetaF)]
vI = [vf * np.cos(thetaF), vf * np.sin(thetaF)]
print posI
print vI

calcProjectileMotion(posI, vI)
