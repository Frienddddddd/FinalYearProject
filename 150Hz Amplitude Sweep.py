# ------------------------------
# ----- Initialize Program -----
# ------------------------------



# import modules (MicroPump & Valve)
import serial                                                                           # allow python to talk to harware using COM port (USB Serial Connection)
import time                                                                             # time related function (example: pause)
from gpiozero import DigitalOutputDevice                                                # import class from GPIO library to digital control pi pins

# Define variables for MicroPump
COM_PORT = "/dev/ttyUSB0"                                                    # USB port from pi5 connected to Android port from ESP32 | Mac_Terminal: ls /dev/tty* OR Windows_DeviceManage: COM_
BAUDRATE = 115200                                                                       # bits per second given from software manual
TIMEOUT = 1.0                                                                           # if no more commands after 1 second, ESP32 stop waiting and go work!

# Define output pins and set all as off for Valve
SV1_Terminal1 = DigitalOutputDevice(26, initial_value=False)                            # Define GPIO pin 14 as output pin for Solenoid Valve 1 and turn off            
SV1_Terminal2 = DigitalOutputDevice(19, initial_value=False)                            # Define GPIO pin 15 as output pin for Solenoid Valve 1 and turn off 
SV2_Terminal1 = DigitalOutputDevice(20, initial_value=False)                            # Define GPIO pin 7 as output pin for Solenoid Valve 2 and turn off 
SV2_Terminal2 = DigitalOutputDevice(21, initial_value=False)                            # Define GPIO pin 8 as output pin for Solenoid Valve 2 and turn off 



# ------------------------------
# ------ Define Functions ------
# ------------------------------



# Function: open_port --> Help connect ESP32 with COM port
def open_port(port=COM_PORT):                                                           # Use value of COM_PORT else specified
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


# send voltage at polarity A
def State_A():
    # Latch terminal 1 of each Solenoid Valve
    SV1_Terminal1.on()                                                  
    SV1_Terminal2.off()
    SV2_Terminal1.on()
    SV2_Terminal2.off()
    time.sleep(0.01)                                                                    # 10 ms pulse and turn off
    # Stop sending voltage pulse to all terminal
    SV1_Terminal1.off() 
    SV1_Terminal2.off()
    SV2_Terminal1.off()
    SV2_Terminal2.off()

# send voltage at polarity B
def State_B():
    # Latch terminal 2 of each Solenoid Valve
    SV1_Terminal1.off()
    SV1_Terminal2.on()
    SV2_Terminal1.off()
    SV2_Terminal2.on()
    time.sleep(0.01)                                                                    # 10 ms pulse and turn off
    # Stop sending voltage pulse to all terminal
    SV1_Terminal1.off()
    SV1_Terminal2.off()
    SV2_Terminal1.off()
    SV2_Terminal2.off()



# ------------------------
# ----- Main Program -----
# ------------------------



try:

    print("Connecting with ESP32")
    ser = open_port()                                                                   # start connection with COM port (ESP32)



    print("Pump On 25")                                            
    set_pump_amplitude(ser, pump=3, amplitude=25)                                       # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1) 
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 10 seconds

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 50")                                            
    set_pump_amplitude(ser, pump=3, amplitude=50)                                       # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 10 seconds

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function

    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 75")                                            
    set_pump_amplitude(ser, pump=3, amplitude=75)                                       # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 100")                                            
    set_pump_amplitude(ser, pump=3, amplitude=100)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 125")                                            
    set_pump_amplitude(ser, pump=3, amplitude=125)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 10 seconds

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 150")                                            
    set_pump_amplitude(ser, pump=3, amplitude=150)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 10 seconds

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function

    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 175")                                            
    set_pump_amplitude(ser, pump=3, amplitude=175)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=3, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 200")                                            
    set_pump_amplitude(ser, pump=3, amplitude=200)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 225")                                            
    set_pump_amplitude(ser, pump=3, amplitude=225)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    
    time.sleep(2)                                                                       # pause for 2 seconds 



    print("Pump On 250")                                            
    set_pump_amplitude(ser, pump=3, amplitude=250)                                      # set which pump to turn on and at what amplitude (0 Vpp - 250 Vpp)
    time.sleep(0.1)                                                                     # give time to process command
    set_pump_frequency(ser, driver=0, frequency=150)                                    # set which driver to adjust and to what frequency (50 - 800 Hz)
    turn_pump_on(ser, pump=3)                                                           # use turn_pump_on function
    time.sleep(10)                                                                      # turn pump on for 3 minutes

    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function
    


    ser.close()                                                                         # close connection with COM port (ESP32)
    print("Disconnecting from ESP32")


except KeyboardInterrupt:

    SV1_Terminal1.off()
    SV1_Terminal2.off()
    SV2_Terminal1.off()
    SV2_Terminal2.off()
    
    print("Pump Off")
    turn_pump_off(ser, pump=3)                                                          # use turn_pump_off function

    ser.close()                                                                         # close connection with COM port (ESP32)
    print("Disconnecting from ESP32")
