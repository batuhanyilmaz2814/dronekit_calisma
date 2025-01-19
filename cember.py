from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

drone = connect("127.0.0.1:14550", wait_ready=True)

print("Araca baglanti gerceklestirildi.")

def kalkis(yukseklik):
    while True:
        while drone.is_armable is not True:
            print("Arac motorları calismaya hazir degil.")
            time.sleep(0.5)

        while True:
            print("Arac motorlari hazir, devam etmek ister misiniz?")
            sonuc = input("(e/h):")
            if sonuc != "e" and sonuc != "h":
                print("Hatali giris yaptiniz.")
                continue
            elif sonuc == "e":
                break
            else:
                break

        if sonuc == "h":
            break
        
        print("Arac motorlari calistiriliyor.")

        drone.mode = VehicleMode("GUIDED")

        drone.armed = True

        print("motorlar calistirildi.")

        drone.simple_takeoff(yukseklik)

        while drone.location.global_relative_frame.alt < yukseklik * 0.9:
            print("Arac hedefe yukseliyor.")
            time.sleep(0.7)

        break



def ileri_git(drone, mesafe_metre):
    """
    Drone'u ileri götürmek için bir hedef belirler ve hareket ettirir.

    Args:
        drone: Bağlantı kurulmuş drone nesnesi
        mesafe_metre: Drone'un ne kadar ileri gitmesi gerektiği (metre cinsinden)
    """
    # Mevcut konumu al
    current_location = drone.location.global_relative_frame
    yaw = math.radians(drone.heading)  # Drone'un mevcut yönü (başlık)

    # 5 metre ileri konum hesaplama
    ileri_lat = current_location.lat + (mesafe_metre * math.cos(yaw) / 111320)  # Enlem
    ileri_lon = current_location.lon + (mesafe_metre * math.sin(yaw) / (111320 * math.cos(math.radians(current_location.lat))))  # Boylam
    hedef_konum = LocationGlobalRelative(ileri_lat, ileri_lon, current_location.alt)

    # Hedef konuma git
    print("Drone hedefe ilerliyor...")
    drone.simple_goto(hedef_konum)

    # Hedefe varana kadar bekle
    while True:
        current_lat = drone.location.global_relative_frame.lat
        current_lon = drone.location.global_relative_frame.lon

        # Hedefe yakınlık kontrolü
        mesafe = math.sqrt(
            (current_lat - ileri_lat) ** 2 + (current_lon - ileri_lon) ** 2
        ) * 111320  # Metreye dönüştür
        print(f"Mevcut mesafe: {mesafe:.2f} metre")
        if mesafe < 0.5:  # 0.5 metre yakınlık toleransı
            print("Drone hedefe ulaştı.")
            break
        time.sleep(1)

def cember_ciz(drone, yaricap, nokta_sayisi):

    # Başlangıç konumu merkez olarak al
    merkez_lat = drone.location.global_relative_frame.lat
    merkez_lon = drone.location.global_relative_frame.lon
    merkez_alt = drone.location.global_relative_frame.alt

    print("Çember çizimi başlıyor...")

    for i in range(nokta_sayisi):
        # Çember üzerindeki açı
        aci = 2 * math.pi * (i / nokta_sayisi)

        # Çember üzerindeki noktayı hesapla
        hedef_lat = merkez_lat + (yaricap * math.cos(aci) / 111320)
        hedef_lon = merkez_lon + (yaricap * math.sin(aci) / (111320 * math.cos(math.radians(merkez_lat))))

        # Hedef konumu oluştur
        hedef_konum = LocationGlobalRelative(hedef_lat, hedef_lon, merkez_alt)

        # Hedefe git
        print(f"Hedef {i+1}/{nokta_sayisi}: {hedef_lat:.6f}, {hedef_lon:.6f}")
        drone.simple_goto(hedef_konum)

        # Noktaya yaklaşana kadar bekle
        while True:
            current_lat = drone.location.global_relative_frame.lat
            current_lon = drone.location.global_relative_frame.lon

            # Hedefe olan mesafeyi hesapla
            mesafe = math.sqrt(
                (current_lat - hedef_lat) ** 2 + (current_lon - hedef_lon) ** 2
            ) * 111320
            if mesafe < 0.5:  # Tolerans: 0.5 metre
                print(f"Hedefe ulaşıldı: {mesafe:.2f} metre")
                break
            time.sleep(0.5)

    print("Çember tamamlandı!")



def cember_ciz_akici(drone, yaricap, nokta_sayisi, hiz):
    """
    Drone'un başlangıç noktasını merkez alarak çember çizer ve duraksamadan hareket eder.
    
    Args:
        drone: Bağlı drone nesnesi
        yaricap: Çemberin yarıçapı (metre cinsinden)
        nokta_sayisi: Çemberin düzgünlüğü için belirlenen nokta sayısı
        hiz: Drone'un hareket hızı (m/s)
    """
    # Başlangıç konumu merkez olarak al
    merkez_lat = drone.location.global_relative_frame.lat
    merkez_lon = drone.location.global_relative_frame.lon
    merkez_alt = drone.location.global_relative_frame.alt

    print("Çember çizimi başlıyor...")

    # Çember üzerindeki tüm noktaları hesapla
    noktalar = []
    for i in range(nokta_sayisi):
        aci = 2 * math.pi * (i / nokta_sayisi)  # Çember üzerindeki açı
        hedef_lat = merkez_lat + (yaricap * math.cos(aci) / 111320)
        hedef_lon = merkez_lon + (yaricap * math.sin(aci) / (111320 * math.cos(math.radians(merkez_lat))))
        noktalar.append(LocationGlobalRelative(hedef_lat, hedef_lon, merkez_alt))

    # Hız belirleme
    drone.airspeed = hiz

    # Noktalara sırayla git
    for hedef_konum in noktalar:
        print(f"Hedefe ilerleniyor: {hedef_konum.lat:.6f}, {hedef_konum.lon:.6f}")
        drone.simple_goto(hedef_konum)

        # Çember üzerindeki noktaları arka arkaya gönderirken bekleme süresini çemberin büyüklüğüne göre ayarlayın
        time.sleep((yaricap / hiz) * 2 / nokta_sayisi)  # Küçük duraksamalarla ilerler

    print("Çember tamamlandı!")
    



                



kalkis(12.3)
ileri_git(drone, 5)

while True:
    cember_ciz_akici(drone, 200, 100, 20)

