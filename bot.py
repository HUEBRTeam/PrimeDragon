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
    
    ACCESS_KEY = sys.argv[1].lower().replace(" ","")
    if len(ACCESS_KEY) != 32:
        print "Invalid Access Key: %s (parsed to: %s)" %(sys.argv[1], ACCESS_KEY) 
        exit(1)
    
    #print "Loading Public Key"
    pkf = open("spublick", "rb")
    pk = pkf.read()
    pkf.close()

    #print "Loading Private Key"
    skf = open("sprivk", "rb")
    sk = skf.read()
    skf.close()

    #ACCESS_KEY = "e8da 79a5 b000 e910 030b 3bca 3ff9 7ab1" #DSUNA

    IP = "115.68.108.183"
    #IP      = "127.0.0.1"
    PORT    = 60000

    accesscode = ACCESS_KEY.lower().replace(" ","")

    f = open("machineinfo.bin", "rb")
    machineinfo_data = f.read()
    f.close()
    machineinfo = MachineInfoPacket_v2()
    machineinfo.FromBinary(machineinfo_data)
    machineinfo.netaddr = "000.000.000.000"
    machineinfo.Memory = 1024*1024*1024
    machineinfo.MachineID = 0xFFFFFFFF
    songpackets = []

    for i in range(3):       
        f = open("songpacket%s.bin"%i, "rb")
        songboard_data = f.read()
        f.close()
        songpacket = ScoreBoardPacket()
        songpacket.FromBinary(songboard_data)
        #songpacket.Score = 0
        #songpacket.EXP = 0
        songpacket.PP = 0xFFFF
        songpackets.append(songpacket)
        
    ProfileID = 0
    MachineID = 0

    login = LoginPacket()
    login.AccessCode = accesscode
    login.MachineID = MachineID
    login.PlayerID = 0

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (OFICIAL_SERVER_IP, 60000)
    tcp.connect(dest)

    #print "Sending Machine Info Packet v2"
    data = EncryptPacket(machineinfo.ToBinary(), pk, sk)
    tcp.send(data)
    time.sleep(0.01)

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
                if packtype == ACKPacket.PacketType:
                    mdata = ACKPacket()
                    mdata.FromBinary(data)
                    #print "Received MachineID %s (0x%x)" % (mdata.MachineID,mdata.MachineID)
                    MachineID = mdata.MachineID
                    login.AccessCode = accesscode
                    login.MachineID = MachineID
                    login.PlayerID = 0
                    #print "Disconnecting"
                    tcp.close()
                    time.sleep(0.01)
                    #print "Reconnecting"
                    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dest = (OFICIAL_SERVER_IP, 60000)
                    tcp.connect(dest)
                    data = EncryptPacket(login.ToBinary(), pk, sk)
                    #print "Sending login for AC: %s" %accesscode
                    tcp.send (data)
                    time.sleep(0.01)
                elif packtype == ProfilePacket.PacketType:
                    #print "Got Profile Packet!"
                    profile = ProfilePacket()
                    profile.FromBinary(data)
                    #print "NickName: %s" % profile.Nickname
                    #print "ProfileID: %s" % profile.ProfileID
                    ProfileID = profile.ProfileID
                    #print "Sending Enter Profile"
                    ep = EnterProfilePacket()
                    ep.ProfileID = ProfileID
                    ep.MachineID = MachineID
                    data = EncryptPacket(ep.ToBinary(), pk, sk)
                    tcp.send(data) 
                    #print "Disconnecting"
                    tcp.close()
                    time.sleep(0.01)
                    #print "Reconnecting"
                    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dest = (OFICIAL_SERVER_IP, 60000)
                    tcp.connect(dest)
                    for i in songpackets:
                        print "Sending ScoreBoard"
                        i.ProfileID = ProfileID
                        i.MachineID = MachineID
                        i.unk2 = 119
                        data = EncryptPacket(i.ToBinary(), pk, sk)
                        tcp.send(data)
                        #print "Disconnecting"
                        tcp.close()
                        time.sleep(0.01)
                        #print "Reconnecting"
                        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        dest = (OFICIAL_SERVER_IP, 60000)
                        tcp.connect(dest)

                    print "Done. Sending Request for Level"
                    req = RequestLevelUpInfoPacket()
                    req.ProfileID = ProfileID
                    data = EncryptPacket(req.ToBinary(), pk, sk)
                    tcp.send(data)
                    time.sleep(0.01)
                    #print "Waiting for level packet"

                elif packtype == KeepAlivePacket.PacketType:
                    #print "Received KeepAlive"
                    pass

                elif packtype == ProfileBusyPacket.PacketType:
                    print "Your profile is already in use! :("
                    break

                elif packtype == LevelUpInfoPacket.PacketType:
                    pp = LevelUpInfoPacket()
                    pp.FromBinary(data)
                    print "Current level: %s"%pp.Level
                    #print "Sending ByePacket"
                    bp = ByePacket()
                    bp.ProfileID = ProfileID
                    data = EncryptPacket(bp.ToBinary(), pk, sk)
                    tcp.send(data) 
                    print "Go check your PP ;)"
                    break
                else:
                    #print "PacketType: %s (%x)" %(packtype, packtype)
                    f = open("pack-%s-%x.bin"%(packtype,packtype),"wb")
                    f.write(data)
                    f.close()
            except Exception,e:
                print "Error: %s" %e
    tcp.close()
    print "Done!"
else:
    print "No access key provided!"
