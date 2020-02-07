import socket
import gpiozero
import traceback

key_mapping = dict()
bind_ip = '0.0.0.0'
bind_port = 9999


buzzer = gpiozero.TonalBuzzer(21)
led1 = gpiozero.LED(20)
led2 = gpiozero.LED(16)
led3 = gpiozero.LED(12)
led4 = gpiozero.LED(17)

def on_key(key):
    def decorator(func):
        key_mapping[key] = key_mapping.get(key, [])+[func]
        return func
    return decorator

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


@on_key('Buzzer')
def buzz(v):
    if int(v):
        buzzer.play(440.0)
    else:
        buzzer.stop()


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
