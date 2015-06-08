#!/usr/bin/env python

import socket
import struct
import time
import sys
import binascii
from prime import *

import struct
import pysodium

LAST_NOUNCE = "\x00" * 24

if len(sys.argv) == 2:
    
    if  ".bin" in sys.argv[1]:
        print "File Access Key Mode"
        f = open(sys.argv[1], "rb")
        data = f.read()
        f.close()
        ACCESS_KEY = binascii.hexlify(data)
        if len(ACCESS_KEY) != 32:
            print "Invalid Access Key!"
            exit(1)
        print "Read access key from %s is %s" %(sys.argv[1],ACCESS_KEY)
    else:
        ACCESS_KEY = sys.argv[1].lower().replace(" ","")
        if len(ACCESS_KEY) != 32:
            print "Invalid Access Key: %s (parsed to: %s)" %(sys.argv[1], ACCESS_KEY) 
            exit(1)
    
    pkf = open("spublick", "rb")
    pk = pkf.read()
    pkf.close()

    skf = open("sprivk", "rb")
    sk = skf.read()
    skf.close()

    #ACCESS_KEY = "e8da 79a5 b000 e910 030b 3bca 3ff9 7ab1" #DSUNA

    IP = "115.68.108.183"
    #IP      = "127.0.0.1"
    PORT    = 60000

    accesscode = ACCESS_KEY.lower().replace(" ","")

        
    ProfileID = 0
    MachineID = 1154

    login = LoginPacket()
    login.AccessCode = accesscode
    login.MachineID = MachineID
    login.PlayerID = 0

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (OFICIAL_SERVER_IP, 60000)
    tcp.connect(dest)
    data = EncryptPacket(login.ToBinary(), pk, sk)
    tcp.send (data)
    time.sleep(0.01)

    gprof = None

    msg = ""
    profile = ""
    while True:
        msg += tcp.recv(4)
        if len(msg) > 0:
            size = struct.unpack("<I", msg[:4])[0]
            msg = msg[4:]
            msg += tcp.recv(size-4-len(msg))
            while len(msg) < size-4:
                msg += tcp.recv((size-4) - len(msg))

            data = DecryptPacket(msg, pk, sk)
            msg = ""
            try:
                packtype = struct.unpack("<I",data[4:8])[0]
                if packtype == ProfilePacket.PacketType:
                    profile = ProfilePacket()
                    profile.FromBinary(data)
                    gprof = profile
                    break

                elif packtype == KeepAlivePacket.PacketType:
                    #print "Received KeepAlive"
                    pass

                elif packtype == ProfileBusyPacket.PacketType:
                    break

                else:
                    #print "PacketType: %s (%x)" %(packtype, packtype)
                    f = open("pack-%s-%x.bin"%(packtype,packtype),"wb")
                    f.write(data)
                    f.close()
            except Exception,e:
                print "Error: %s" %e
    tcp.close()
    if gprof == None:
        print '{}'
    else:
        print '{"avatar":"%s","name":"%s"}' % (gprof.Avatar, gprof.Nickname)
else:
    print "{}"
