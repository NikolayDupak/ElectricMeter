class Sensor:
    import serial
    import time
    __commands = {
        'init': (0x2F, 0x3F, 0x21, 0x0D, 0x0A),
        'end': (0x01, 0x42, 0x30, 0x03, 0x75),
        'readData': (0x01, 0x52, 0x31, 0x02, 0x45, 0x54, 0x30, 0x50, 0x45, 0x28, 0x29, 0x03, 0x37)
    }
    """
    init - /?!..
    end - .B0.u
    readData - .R1.ETOPE().7
    """

    __answers = {
        'init': (0x2F, 0x45, 0x4B, 0x54, 0x35),
        'Data': (0x02, 0x45, 0x54, 0x30, 0x50, 0x45)
    }
    answer = None

    def __init__(self, serial_port='/dev/ttyUSB0', address=0):

        self.serial_speed = 9600
        try:
            self.ser = self.serial.Serial(serial_port, 9600)
        except self.serial.SerialException:
            print("No serial port")

        pass

    def read(self, time=0.5):
        while True:
            message = b''
            resive_bytes = self.ser.inWaiting()
            if resive_bytes != 0:
                message += self.ser.read(b)
            self.time.sleep(time)
            return message

    def wait_answer(self, answer, time=0.5) -> bool:
        message = self.read(time)
        if message == b'':
            return False
        for i in range(len(message)):
            ind = 0
            for j in range(len(answer)):
                if message[i] == answer[j]:
                    ind += 1
            if ind == len(answer):
                self.answer = message
                return True
        return False

    def send(self, data):

        start_time = self.time.time()
        count_of_bytes = self.ser.write(data)
        clock = (count_of_bytes * 11) / self.serial_speed
        now_time = self.time.time()
        res = clock - (now_time - start_time)
        self.time.sleep(res)

    def read_data(self):
        self.send(self.__commands['init'])
        if self.wait_answer(self.__answers['init']):
            self.send(self.__commands['readData'])
            if self.wait_answer(self.__answers['Data']):
                self.send(self.__commands['end'])
                return self.answer

