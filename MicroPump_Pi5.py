# ------------------------------
# ----- Initialize Program -----
# ------------------------------



# import modules (MicroPump & Valve)
import serial                                                                           # allow python to talk to hardware using COM port (USB Serial Connection)
import time                                                                             # time related function (example: pause)

# Define variables for MicroPump
COM_PORT = "/dev/ttyUSB0"                                                               # USB port from pi5 connected to Android port from ESP32 | Mac_Terminal: ls /dev/tty.* OR Windows_DeviceManage: COM_
BAUDRATE = 115200                                                                       # bits per second given from software manual
TIMEOUT = 1.0                                                                           # if no more commands after 1 second, ESP32 stop waiting and go work!


# ------------------------------
# ------ Define Functions ------
# ------------------------------


# Function: open_port --> Help connect ESP32 with COM port
def open_port(port=COM_PORT):                                                           # use value of COM_PORT else specified
    ser = serial.Serial(port, BAUDRATE, timeout=TIMEOUT)                                # class from pyserial library to start a conneciton with ESP32 (make all the agreements!)
    time.sleep(0.1)                                                                     # small pause to let device settle
    return ser                                                                          # return serial connection


# Function: send_cmd --> Send commands
def send_cmd(ser, cmd):
    to_send = (cmd + "\r\n").encode('utf-8')                                            # from software manual: all commands must end with a new line tage "\r\n" and data bits = 8
    ser.write(to_send)                                                                  # class from pyserial library to send commands to ESP32


# Function: turn_pump_on --> turn selected pump on
def turn_pump_on(ser, pump):
    send_cmd(ser, f"P{pump}ON")                                                         # send P<p>ON command to ESP32


# Function: turn_pump_off --> turn selected pump off
def turn_pump_off(ser, pump):                                                     
    send_cmd(ser, f"P{pump}OFF")                                                        # send P<p>OFF command to ESP32


# Function: set_pump_amplitude --> set the amplitude for the selected pump
def set_pump_amplitude(ser, pump, amplitude):                                    
    send_cmd(ser, f"P{pump}V{int(amplitude)}")                                          # send P<p>V<a> command to ESP32


# Function: set_pump_frequency --> set the frequency for the selected driver
def set_pump_frequency(ser, driver,frequency):                                          # send F<d>=<f> command to ESP32                        
    send_cmd(ser, f"F{driver}={frequency}")                                    



# ------------------------
# ----- Main Program -----
# ------------------------



try:

    print("Connecting with ESP32")
    ser = open_port()                                                                   # start connection with COM port (ESP32)
    

    print("Pump On")                                            
    set_pump_amplitude(ser, pump=1, amplitude=75)                                       # set which pump to turn on and at what amplitude (range: 0 Vpp - 250 Vpp)
    time.sleep(1)                                                                       # give time to process command
    set_pump_frequency(ser, driver=0, frequency=180)                                    # set which driver to adjust and to what frequency (range: 50 Hz - 800 Hz)
    turn_pump_on(ser, pump=1)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 10 seconds

    print("Pump Off")
    turn_pump_off(ser, pump=1)                                                          # use turn_pump_off function
    

    ser.close()                                                                         # close connection with COM port (ESP32)
    print("Disconnecting from ESP32")


except KeyboardInterrupt:                                                               # stop the operation right away when press "control + c" on keyboard
    
    print("Pump Off")
    turn_pump_off(ser, pump=1)                                                          # use turn_pump_off function

    ser.close()                                                                         # close connection with COM port (ESP32)
    print("Disconnecting from ESP32")
