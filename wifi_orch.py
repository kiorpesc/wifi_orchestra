import subprocess
from time import sleep
import re
import rtmidi
import random

c_open = [24, 31, 36, 43, 48, 55, 60, 72, 84]
c_sus = [26, 29, 38, 40, 50, 53, 59]
c_mel = [48, 50, 52, 53, 55, 57, 59, 60]
midiout = 0
current_notes = []

#while True:
def scan_wifi():    
    scan = subprocess.Popen("wpa_cli scan", stdout=None, stderr=None, shell=True)
    process = subprocess.Popen("wpa_cli scan_results", stdout=subprocess.PIPE, stderr=None, shell=True)
    networks = []
    for line in iter(process.stdout.readline, b''):
        if line[0] == 'S' or line[0] == 'O' or line[0] == 'b':
            pass
        else:
            networks.append(list(line.split('\t')))

    process.communicate()
    return networks


def init_midi():
    global midiout
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    ports = midiout.get_port_count()
    print ports

    for x in range(ports):
        print midiout.get_port_name(x)
    
    #set all channels to reed organ (for now)
    ch = 0
    midiout.send_message([ch + 192, 20])
    ch = 5
    midiout.send_message([ch + 192, 20])
    ch = 10
    midiout.send_message([ch + 192, 48])
    


def kill_midi():
    global midiout
    midiout = 0

def generate_midi_list(nets):
    messages = []
    for x in nets:
        messages.append(midify(x))
    return messages

def find_note_by_bssid(bssid):
    for x in range(len(current_notes)):
        if current_notes[x][0] == (bssid):
            return x
    return -1 

def midify(net):
    global current_notes
    this_note = find_note_by_bssid(net[0])
    output = []
    vel = 120/45 * (int(net[2]) + 95)
    if vel < 0:
        vel = 0
        if this_note > -1:
            current_notes.pop(this_note)
    else:
        if vel < 30:
            vel = 30
        if vel > 120:
            vel = 120
    # 2412 = ch 1
    # each channel is 5Hz from the previous
    # for now, channel can set midi channel (easy solution)
    chan = (int(net[1]) - 2412) / 5
    output.append(chan + 144)

    # generate and append note value
    if len(net[3]) > 6:
        note = c_open[random.randint(0, len(c_open)-1)]
    else:
        note = c_mel[random.randint(0, len(c_mel)-1)]
        if this_note > -1:
            stop_single_note(this_note)
            current_notes[this_note][1][1] = note
            current_notes[this_note][1][2] = random.randint(70,110)
    output.append(note)

    #generate and append velocity value
    # -95 and lower means zero velocity (note off)
    # 50 and higher means 120 velocity
    if note >=60 and vel > 100:
        vel = 100
    output.append(vel)
    if this_note == -1:
        current_notes.append([net[0], output])
    return output

def send_all_midi():
    global midiout
    for x in current_notes:
        midiout.send_message([x[1][0]-16, x[1][1], 0])
        midiout.send_message(x[1])
        sleep(0.25)

def stop_single_note(index):
    global midiout
    midiout.send_message([current_notes[index][1][0] - 16, current_notes[index][1][1], 0])

def stop_all_notes():
    global midiout
    for x in current_notes:
        midiout.send_message([x[1][0] - 16, x[1][1], 0])
'''
note_on = [0x90, 60, 80] # channel 9? (10 was 0x99), middle C, velocity 112
note_on2 = [0x91, 64, 90]
note_off = [0x80, 60, 0]
note_off2 = [0x81, 64, 0]
prog_change1 = [0xC0, 20]

#midiout.send_message(note_on)
#midiout.send_message(note_on2)
for x in range(128):
    midiout.send_message([0x90, 60, x])
    time.sleep(.05)

time.sleep(2)
midiout.send_message(note_off)
#midiout.send_message(note_off2)
'''

def main():
    init_midi()
    while True:
        networks = scan_wifi()
        notes = generate_midi_list(networks)
        print notes
        #stop_all_notes()
        send_all_midi()
        sleep(2)        

if __name__ == "__main__":
    main()

