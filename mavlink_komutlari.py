from dronekit import *
import math
import time
from pymavlink import mavutil

connection_string = "127.0.0.1:14550"

drone = connect(connection_string,wait_ready=True,timeout=100)

print(drone.is_armable) #Drone motorları çalıştırılabilir mi?

def yuksel(yukseklik):  #drone'u yükseltmek için gerekli olan kodlar.
    while drone.is_armable==False:
        print("araç arm edilmeyi bekliyor.")
        time.sleep(0.5)
    print("Drone su anda hazir.")

    drone.mode=VehicleMode("GUIDED")
    while drone.mode!="GUIDED":
        print("GUIDED moduna gecis bekleniyor.")
        time.sleep(0.5)

    print("Drone arm ediliyor.")
    drone.armed=True

    while drone.armed==False:
        print("Drone arm edilmeyi bekliyor.")
        time.sleep(0.5)

    print("Drone arm edildi.")

    drone.simple_takeoff(yukseklik)
    while drone.location.global_relative_frame.alt<yukseklik*0.95:
        print("Drone yukseliyor...")
        drone_yuksekligi = drone.location.global_relative_frame.alt
        print("Drone yuksekligi: ", drone_yuksekligi)
        time.sleep(0.3)
    print("Drone hedef yukseklige ulasti.")


def velocity(velocity_x,yaw_rate,velocity_y,velocity_z, drone):
    message = drone.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0b0000011111000111,
        0,0,0,
        velocity_x, velocity_y, velocity_z,
        0,0,0,
        0, math.radians(yaw_rate))
    
    drone.send_mavlink(message)

#ÖNEMLİ!!   Buradaki komutlaar 3 saniyelik çalışır, devam etmesi için tekrar göndermek gerekir.

yuksel(10)
print("10 metre yuksekliğe çıkıldı.")
velocity(5,0,0,0,drone=drone)
print("x ekseninde 5 m/s hızla ilerleniyor.")
time.sleep(3)
velocity(0,0,5,0,drone=drone)
print("y ekseninde 5 m/s hızla ilerleniyor.")
time.sleep(3)
velocity(0,0,0,-5,drone=drone)
print("z ekseninde 5 m/s hızla ilerleniyor.")
time.sleep(3)
velocity(0,60,0,0,drone=drone)
print("kendi etrafında saat yönünde 60 derece dönülüyor.")
time.sleep(3)






    

