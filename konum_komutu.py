from dronekit import *
import time
import math
from math import radians
from pymavlink import mavutil

connection_string = "127.0.0.1:14550"

iha=connect(connection_string,wait_ready=True,timeout=100)

def arm_ol_ve_yuksel(yukseklik):
    while iha.is_armable==False:
        print("araç arm edilmeyi bekliyor.")
        time.sleep(0.5)
    print("IHA su anda hazir.")

    iha.mode=VehicleMode("GUIDED")
    while iha.mode!="GUIDED":
        print("GUIDED moduna gecis bekleniyor.")
        time.sleep(0.5)

    print("IHA arm ediliyor.")
    iha.armed=True

    while iha.armed==False:
        print("IHA arm edilmeyi bekliyor.")
        time.sleep(0.5)

    print("IHA arm edildi.")

    iha.simple_takeoff(yukseklik)
    while iha.location.global_relative_frame.alt<25*0.95:
        print("IHA yukseliyor...")
        iha_yuksekligi = iha.location.global_relative_frame.alt
        print("IHA yuksekligi: ", iha_yuksekligi)
        time.sleep(0.3)
    print("IHA hedef yukseklige ulasti.")


def position(posx, posy, posz, hizAcisal, iha):
    mesaj = iha.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # sağdan sola mesajın okunup okunmayacağı (0 okur, 1 okumaz)
        posx, posy, posz,  # pozisyonlar(metre)
        0, 0, 0,  # hızlar(m/s)
        0, 0, 0,  # ivmeler(m/s^2)
        0, math.radians(hizAcisal), 0)  # açısal hızlar (rad/s)
    iha.send_mavlink(mesaj)

arm_ol_ve_yuksel(10)

position(5,0,0,-14,iha=iha) #Arm edildiğin yerin 5 metre ilerisine ve 14 metre yukarısına git.
while iha.location.local_frame.north<=4.90:
    print("5 metre kuzeye gidiliyor")
    time.sleep(0.3)
print("5 metre kuzeye gidildi.")
time.sleep(2)

position(5,5,0,-14,iha=iha) #Arm edildiğin yerin 5 metre ilerisine, 5 metre doğusuna ve 14 metre yukarısına git.
while iha.location.local_frame.east<=4.90:
    print("5 metre doguya gidiliyor")
    time.sleep(0.3)
print("5 metre doguya gidildi.")
time.sleep(2)

position(0,5,0,-14,iha=iha) #Arm edildiğin yere ve 14 metre yukarısına git.
while iha.location.local_frame.north>=0.1:
    print("5 metre guneye gidiliyor")
    time.sleep(0.3)
print("5 metre guneye gidildi.")
time.sleep(2)

position(0,0,0,-20,iha=iha) #Arm edildiğin yerin 5 metre ilerisine ve 14 metre yukarısına git.
while iha.location.local_frame.down<=19.90:
    print("5 metre yukarıya gidiliyor")
    time.sleep(0.3)
print("5 metre yukarıya gidildi.")
time.sleep(2)

