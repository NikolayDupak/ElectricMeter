class SensorMqtt:
    import re
    import decimal as dec
    __data = list()
    __value = tuple()
    __reading = False
    __status = 0


    def on_message(self, client, userdata, msg):
        self.read_answer(msg.payload)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def __init__(self, adddress, port=1883):
        import paho.mqtt.client as mqtt
        self.client = mqtt.Client()
        # client.username_pw_set(username="Nick", password="pass")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(adddress, port, 60)

        # client.publish("answer", 310)
        self.client.subscribe("answer")
        self.client.loop_start()

    def __del__(self):
        self.client.loop_stop()

    def send_request(self):
        print("send")
        self.client.publish("info", "V")
        self.__status = 1

    def read_answer(self, msg):
        print(msg)
        if msg == b"START":
            print("Start reading")
            self.__status = 2
            self.__reading = True
            return
        if msg == b"END":
            print("End reading")
            self.__reading = False
            self.__status = 3
            self.parse_answer()
            return
        self.__data.append(msg)

    def parse_answer(self):
        print(self.__data)
        for ans in self.__data:
            if len(ans) >= 50:
                self.parse_value(ans)
        pass

    def parse_value(self, answer: bytes):
        """
                get answer and return tuple of data with check sum
                (sum, T0, T1, T2, T3, T4)
        """
        # print(answer)
        string = str(answer, "utf-8")
        res = self.re.findall(r'ET0PE\(\d+\.\d+\)', string)
        # print(res)
        dataOfValue = list()
        self.dec.getcontext().prec = 10
        for i in res:
            # print(i)
            val = i[6:-1]
            val = self.dec.Decimal(val)
            dataOfValue.append(val)

        print(dataOfValue)
        self.__value = dataOfValue
        return tuple(dataOfValue)

    def get_value(self):
        return self.__value

    def get_status(self):
        return self.__status