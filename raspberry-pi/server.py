import socket
import gpiozero
import traceback
import serial
#from mearm import meArm
import time

key_mapping = dict()
bind_ip = '0.0.0.0'
bind_port = 9999

#ser = serial.Serial('/dev/ttyACM0',19200)

def send_serial_cmd(key, value):
    value = int(value)
    key = bytes(key, 'utf8')
    value = bytes.fromhex(hex(value)[2:].zfill(2))
    ser.write(key)
    ser.write(value)
    ser.flush()


#buzzer = gpiozero.TonalBuzzer(21)
led1 = gpiozero.PWMLED(23)
led2 = gpiozero.LED(24)
led3 = gpiozero.LED(25)
led4 = gpiozero.LED(8)

base_servo = gpiozero.Servo(17)
claw_servo = gpiozero.Servo(5) # the Klaw!
arm_maj_servo = gpiozero.Servo(27)
arm_min_servo = gpiozero.Servo(22)


#arm = meArm.meArm()
#arm.begin()

def on_key(key):
    def decorator(func):
        key_mapping[key] = key_mapping.get(key, [])+[func]
        return func
    return decorator

def lerp(v0, v1, t):
    return v0 + t * (v1 - v0)

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

GRABBING = False

@on_key('RightGrab')
def grab(v):
    global GRABBING
    if int(v):
        GRABBING = True
        #send_serial_cmd('K',0)
#        arm.setClaw(-1)
        claw_servo.value = -1
    else:
        GRABBING = False

@on_key('Z')
def zcoord(v):
    v = float(v.replace(',', '.'))
#    arm.nz=v
#    if time.time()-last_upd>0.1:
#        arm.goDirectlyTo(arm.nx+ox, arm.ny+oy, arm.nz+oz)
#        global last_upd
#        last_upd = time.time()

#    a = lerp(0,180,v)
#    send_serial_cmd('B', a)
    base_servo.value = v

@on_key('Y')
def ycoord(v):
    v = float(v.replace(',', '.'))
#    arm.ny = v
    arm_maj_servo.value = v

@on_key('X')
def xcoord(v):
    v = float(v.replace(',', '.'))
#    arm.nx = v
    arm_min_servo.value = v

@on_key('RightSqueeze')
def squeeze(v):
    v = 1 - float(v.replace(',', '.'))
    if not GRABBING:
        #send_serial_cmd('K', lerp(60, 110, v))
        claw_servo.value = (map_value(v, 0, 1, -0.8, 0.5))

@on_key('Colliding')
def on_collide(v):
    v = int(v)
    if v:
        led2.on()
    else:
        base_servo.detach()
        arm_maj_servo.detach()
        arm_min_servo.detach()
        led2.off()
#        buzzer.stop()

@on_key('Y')
def set_brightness(v):
    v = v.replace(',','.')
    led1.value = float(v)
#    buzzer.play(220.0 + float(v)*220.0)

@on_key('LED1')
def ledA(v):
    print('LED1',v)
    (led1.on if int(v) else led1.off)()

@on_key('LED2')
def ledB(v):
    print('LED2',v)
    (led2.on if int(v) else led2.off)()

@on_key('LED3')
def ledC(v):
    print('LED3',v)
    (led3.on if int(v) else led3.off)()

@on_key('LED4')
def ledD(v):
    print('LED4',v)
    (led4.on if int(v) else led4.off)()


#@on_key('Buzzer')
#def buzz(v):
#    if int(v):
#        buzzer.play(440.0)
#    else:
#        buzzer.stop()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((bind_ip, bind_port))

buf = bytearray()

while 1:
    data, addr = sock.recvfrom(1024)
    buf += data
    sep = buf.split(b'\x00')
    if len(sep)!=1:
        buf = sep[-1]
        for part in sep[:-1]:
            print(part)
            k, v = part.split(b'\xff')
            k = str(k, 'utf-8')
            v = str(v, 'utf-8') # TODO: maybe preserve bin-data?
            if k not in key_mapping:
                 print('Key',k,'not found!')
            else:
                print('Calling',len(key_mapping[k]),'callbacks')
                for callback in key_mapping[k]:
                    try:
                        callback(v)
                    except:
                        traceback.print_exc()
