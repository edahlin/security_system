import serial

ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=5)

while True:
    line = ser.readline()
    splitline = line.split(',')

    if splitline[0] == "SGPGGA":
        lattitude = line[2]
        lattitude_direction = line[3]
        longitude = line[4]
        longitude_direction = line[5]

        print(line)
        break
