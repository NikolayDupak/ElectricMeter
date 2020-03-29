#!/bin/usr python3
import SensorMqtt
import time
import re
from decimal import *
import pymysql


def parse_value(answer: bytes):
    """
            get answer and return tuple of data with check sum
            (sum, T0, T1, T2, T3, T4)
    """
    print(answer)
    string = str(answer, "utf-8")
    # string = answer
    res = re.findall(r'ET0PE\(\d+\.\d+\)', string)
    print(res)
    dataOfValue = list()
    getcontext().prec = 10
    for i in res:
        print(i)
        val = i[6:-1]
        val = Decimal(val)
        dataOfValue.append(val)
    summ = Decimal(0)
    for i in range(1, len(dataOfValue) - 1):
        summ += dataOfValue[i]
    if summ == dataOfValue[0]:
        print("TRUE")

    print(dataOfValue)
    return tuple(dataOfValue)

def main():
    # Open database connection
    db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Database version : %s " % data)

    # disconnect from server
    db.close()

    """CE301 = SensorMqtt.SensorMqtt("192.168.8.101")
    CE301.send_request()
    while True:
        if CE301.get_status() == 3:
            break
        print(CE301.get_status())
        time.sleep(2)
    print(CE301.get_value())
"""


if __name__ == '__main__':
    main()