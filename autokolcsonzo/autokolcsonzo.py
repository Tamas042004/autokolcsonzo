from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os

# Absztrakt Auto osztály
class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.foglalt = False

    @abstractmethod
    def __str__(self):
        pass

# Személyautó osztály
class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, szemelyek_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.szemelyek_szama = szemelyek_szama

    def __str__(self):
        return f"Személyautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap, Személyek száma: {self.szemelyek_szama}"

# Teherautó osztály
class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def __str__(self):
        return f"Teherautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Bérleti díj: {self.berleti_dij} Ft/nap, Teherbírás: {self.teherbiras} kg"

# Bérlés osztály
class Berles:
    def __init__(self, auto: Auto, berles_datum: datetime):
        self.auto = auto
        self.berles_datum = berles_datum
        self.auto.foglalt = True

    def __str__(self):
        return f"Bérlés - {self.auto}, Bérlés dátuma: {self.berles_datum.strftime('%Y-%m-%d')}"

# Autókölcsönző osztály
class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto: Auto):
        self.autok.append(auto)

    def auto_berles(self, rendszam: str, berles_datum: datetime):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                if auto.foglalt:
                    print("Ez az autó már foglalt!")
                    return None
                if berles_datum < datetime.now():
                    print("Csak jövőbeli dátumra lehet foglalni!")
                    return None
                berles = Berles(auto, berles_datum)
                self.berlesek.append(berles)
                print(f"Sikeres bérlés! Ár: {auto.berleti_dij} Ft")
                return berles
        print("Nem található ilyen rendszámú autó!")
        return None

    def berles_lemondas(self, rendszam: str):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam:
                berles.auto.foglalt = False
                self.berlesek.remove(berles)
                print("Sikeres lemondás!")
                return
        print("Nem található ilyen bérlés!")

    def berlesek_listazasa(self):
        if not self.berlesek:
            print("Nincsenek aktív bérlések.")
        else:
            print("Aktív bérlések:")
            for berles in self.berlesek:
                print(berles)

# Felhasználói interfész
def felhasznaloi_interfesz():
    # Adatok.txt létrehozása
    with open("adatok.txt", "w", encoding="utf-8") as f:
        f.write("Név: [Bánfalvi Tamás]\n")
        f.write("Szak: [Mérnökinformatika]\n")
        f.write("Neptun kód: [MHSZ2Z]\n")

    # Autókölcsönző létrehozása és inicializálása
    kolcsonzo = Autokolcsonzo("Python Autókölcsönző")

    # Kezdeti autók hozzáadása
    kolcsonzo.auto_hozzaadas(Szemelyauto("ABC-123", "Toyota Corolla", 10000, 5))
    kolcsonzo.auto_hozzaadas(Szemelyauto("DEF-456", "Honda Civic", 12000, 5))
    kolcsonzo.auto_hozzaadas(Teherauto("GHI-789", "Ford Transit", 15000, 2000))

    # Kezdeti bérlések
    kolcsonzo.auto_berles("ABC-123", datetime.now() + timedelta(days=1))
    kolcsonzo.auto_berles("DEF-456", datetime.now() + timedelta(days=2))
    kolcsonzo.auto_berles("GHI-789", datetime.now() + timedelta(days=3))

    # Felhasználói menü
    while True:
        print("\n=== Python Autókölcsönző ===")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Kilépés")

        valasztas = input("Válassz egy menüpontot (1-4): ")

        if valasztas == "1":
            rendszam = input("Add meg az autó rendszámát: ")
            datum_str = input("Add meg a bérlés dátumát (ÉÉÉÉ-HH-NN formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                kolcsonzo.auto_berles(rendszam, datum)
            except ValueError:
                print("Érvénytelen dátum formátum!")

        elif valasztas == "2":
            rendszam = input("Add meg a lemondandó bérlés autójának rendszámát: ")
            kolcsonzo.berles_lemondas(rendszam)

        elif valasztas == "3":
            kolcsonzo.berlesek_listazasa()

        elif valasztas == "4":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás!")

if __name__ == "__main__":
    felhasznaloi_interfesz()