"""Laptop based physics model for our
smart catapult, has a gui for user input
of desired distance and outputs
positions for the servos and stepper moters"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from random import random
# ser = serial.Serial('/dev/tty.usbserial', 9600)


def calcCatapultInteractions(thetaA, rA, hA, wA, mA, kS, attachPointS, dA, eqLS, stopAngle):
    iA = mA * (wA ** 2 + hA ** 2) / 3

    xPosS = attachPointS[0]
    yPosS = attachPointS[1]

    omegaA = 0
    y0 = [thetaA, omegaA]
    t = np.linspace(0, 5, 10000)

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

    # plt.plot(t, omegaF)
    # plt.title("Angular Velocity over Time", fontsize=20)
    # plt.xlabel("Time (s)", fontsize=18)
    # plt.ylabel("Angular Velocity (rads/s)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.figure()
    # plt.title("Catapult Tip Trajectory", fontsize=20)
    # plt.axis((-.4, 0, 0, .4))
    # plt.xlabel("X Position (m)", fontsize=18)
    # plt.ylabel("Y Position (m)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.plot(rA * np.cos(thetaF), rA * np.sin(thetaF))
    # plt.figure()
    # plt.title("Catapult Angle over Time", fontsize=20)
    # plt.xlabel("Time (s)", fontsize=18)
    # plt.ylabel("Angle (Rad)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.plot(t, thetaF)
    # plt.show()

    return [thetaF[-1], omegaF[-1]]


def calcProjectileMotion(posI, vI):
    x0 = posI[0]
    y0 = posI[1]

    vx0 = vI[0]
    vy0 = vI[1]

    yI = [x0, y0, vx0, vy0]
    t = np.linspace(0, 10, 50000)

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

    # plt.figure()
    # plt.plot(t, xf)
    # plt.title("X Distance over Time", fontsize=20)
    # plt.xlabel("Time (s)", fontsize=18)
    # plt.ylabel("X Distance (m)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.figure()
    # plt.plot(t, yf)
    # plt.title("Y Distance over Time", fontsize=20)
    # plt.xlabel("Time (s)", fontsize=18)
    # plt.ylabel("Y Distance (m)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.figure()
    # plt.plot(xf, yf)
    # plt.title("Projectile Trajectory", fontsize=20)
    # plt.xlabel("X Distance (m)", fontsize=18)
    # plt.ylabel("Y Distance (m)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.figure()
    # plt.plot(t, vxf)
    # plt.title("Vx over Time", fontsize=20)
    # plt.xlabel("Time", fontsize=18)
    # plt.ylabel("Vx Distance", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.figure()
    # plt.plot(t, vyf)
    # plt.title("Vy over Time", fontsize=20)
    # plt.xlabel("Time", fontsize=18)
    # plt.ylabel("Vy Distance", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.show()

    return [xf, yf]

if __name__ == '__main__':
    print "Start"
    data = np.zeros([1, 2])

    for angle in np.arange(np.pi, np.pi / 2, -.05):
        [thetaF, omegaF] = calcCatapultInteractions(
            np.pi, .3302, .0127, .0191, .056, .197, (
                0.143764, 0.102616), 0.16764, .1778,
            angle)

        r = .35
        vf = abs(omegaF * r)

        posI = [r * np.cos(thetaF), r * np.sin(thetaF)]
        vI = [vf * np.sin(thetaF), -vf * np.cos(thetaF)]

        trajectory = calcProjectileMotion(posI, vI)

        plt.plot(trajectory[0], trajectory[1], color=(
            (angle - np.pi / 2) / (np.pi / 2), (angle - np.pi / 2) / (np.pi / 2), (angle - np.pi / 2) / (np.pi / 2)), alpha = .8, label="Theta = " + str(angle))

    plt.title("The Effect of Stopping Arm Angle on Trajectory", fontsize=20)
    plt.xlabel("X Distance (m)", fontsize=18)
    plt.ylabel("Y Distance (m)", fontsize=18)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.show()

    # rt = 0.039116
    # height = 0.102616
    # xDist = 0.143764
    # data = np.zeros([1, 2])

    # for angle in np.arange(0, np.pi / 2, 0.01):
    #     [thetaF, omegaF] = calcCatapultInteractions(
    #         np.pi, .3302, .0127, .0191, .056, .197,
    #         (xDist + (rt * np.cos(angle)),
    #          height + (rt * np.sin(angle))), 0.16764, .1778, 3 * np.pi / 4)

    #     r = .35
    #     vf = abs(omegaF * r)

    #     posI = [r * np.cos(thetaF), r * np.sin(thetaF)]
    #     vI = [vf * np.sin(thetaF), -vf * np.cos(thetaF)]

    #     trajectory = calcProjectileMotion(posI, vI)
    #     xTraj = trajectory[0]
    #     xF = xTraj[-1]
    #     data = np.vstack([data, [angle, xF]])

    # print data
    # plt.plot(
    #     data[:, 0], data[:, 1])

    # plt.title(
    #     "The Effect of Tension Arm Angle on the Total Range of Catapult", fontsize=20)
    # plt.xlabel("Tension Arm Angle (Rad)", fontsize=18)
    # plt.ylabel("Total X Distance (m)", fontsize=18)
    # plt.yticks(fontsize=14)
    # plt.xticks(fontsize=14)

    # plt.legend(loc='upper right')
    # plt.show()
