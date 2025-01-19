from dronekit import *
import time

connection_string = "127.0.0.1:14550"

iha=connect(connection_string,wait_ready=True,timeout=100)

print(iha.location.global_relative_frame.alt) #Yükseklik komutu

#İHA'nın motorunu calistiren ve havalandiran fonksiyon
def motor_ve_yukselme(yukseklik):               
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
    while iha.location.global_relative_frame.alt<yukseklik*0.95:
        print("IHA yukseliyor...")
        iha_yuksekligi = iha.location.global_relative_frame.alt
        print("IHA yuksekligi: ", iha_yuksekligi)
        time.sleep(0.3)
    print("IHA hedef yukseklige ulasti.")

def iha_indirme():
    iha.mode=VehicleMode("LAND")
    while iha.location.global_frame.alt>1:
        print("IHA inis yapiliyor...")
        time.sleep(0.5)

def ucus():  #Basit bir konuma götürmek için gerekli olan kodlar.
    iha.mode=VehicleMode("GUIDED")
    iha.armed=True
    konum=LocationGlobalRelative(-35,149,16)
    iha.simple_goto(konum)

#motor_ve_yukselme(25)        
#iha_indirme()
ucus()
