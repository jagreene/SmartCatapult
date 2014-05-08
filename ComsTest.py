import serial
from serial.tools import list_ports
from time import sleep


class Catapult(object):

    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)

    def init_coms(self):
        serin = 0
        while serin != 1:
            serin = self.ser.read()

    def send_motor_position(self, motor, pos):
        sleep(5)
        self.ser.write(motor)
        sleep(.1)
        self.ser.write(pos)
        sleep(.1)

        print "Sending info"
        text = self.ser.readline()
        print text

if __name__ == '__main__':
    ports = []
    port = None
    for tty in list_ports.comports():
        try:
            port = serial.Serial(port=tty[0])
            if port.isOpen():
                ports.append(tty)
        except serial.SerialException as ex:
            print 'Port {0} is unavailable: {1}'.format(tty, ex)

    try:
        port = ports[0]
        port = port[0]
        print port
    except:
        print 'No available ports'

    if port:
        baud = 9600

        Catapult = Catapult(port, baud)

        # Catapult.init_coms()
        Catapult.send_motor_position("A", '45')
        Catapult.send_motor_position("A", '45')
        Catapult.send_motor_position("A", '45')
