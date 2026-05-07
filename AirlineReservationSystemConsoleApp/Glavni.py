# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:07:07 2025

@author: milan
"""

import Korisnici
import Letovi
import Rezervacije
import AdminRezervacije

def prikaziMeniAdmina():
    print("\n--- ADMIN MENI ---")
    print("1. Prikaz svih letova")
    print("2. Dodavanje novog leta")
    print("3. Izmena leta")
    print("4. Brisanje leta")
    print("5. Pregled svih rezervacija")
    print("6. Brisanje rezervacije")
    print("7. Prikaz rezervacija po letu")
    print("8. Prikaz rezervacija po datumu leta")
    print("9. Ukupan prihod po letu")
    print("0. Izlaz")

def prikaziMeniKorisnika():
    print("\n--- KORISNIK MENI ---")
    print("1. Prikaz dostupnih letova")
    print("2. Rezervacija karata")
    print("3. Pregled rezervacija")
    print("4. Otkaži rezervaciju")
    print("0. Izlaz")

def main():
    print("=== AVIO REZERVACIJE ===")
    username = input("Korisničko ime: ")
    password = input("Lozinka: ")

    korisnik = Korisnici.login(username, password)

    if korisnik:
        print(f"\nUspešno prijavljivanje! Dobrodošao, {korisnik['username']} ({korisnik['uloga']}).")

        if korisnik['uloga'] == 'admin':
            while True:
                prikaziMeniAdmina()
                izbor = input("Izaberite opciju: ")
        
                if izbor == "1":
                    Letovi.prikaziSveLetove()
                elif izbor == "2":
                    Letovi.dodajLet()
                elif izbor == "3":
                    Letovi.izmeniLet()
                elif izbor == "4":
                    Letovi.obrisiLet()
                elif izbor == "5":
                    AdminRezervacije.prikaziSveRezervacije()
                elif izbor == "6":
                    AdminRezervacije.obrisiRezervacijuAdmin()
                elif izbor == "7":
                    AdminRezervacije.prikaziRezervacijePoLetu()
                elif izbor == "8":
                    AdminRezervacije.prikaziRezervacijePoDatumuLeta()
                elif izbor == "9":
                    AdminRezervacije.prikaziUkupanPrihodPoLetu()

                elif izbor == "0":
                    print("Izlaz iz programa.")
                    break
                else:
                    print("Nepostojeća opcija, pokušajte ponovo.")


        else:
            while True:
                prikaziMeniKorisnika()
                izbor = input("Izaberite opciju: ")
                if izbor == "1":
                    Rezervacije.prikaziDostupneLetove()
                elif izbor == "2":
                    Rezervacije.rezervisiKarte(korisnik['id'])
                elif izbor == "3":
                    Rezervacije.prikaziRezervacije(korisnik['id'])
                elif izbor == "4":
                    Rezervacije.otkaziRezervaciju(korisnik['id'])
                elif izbor == "0":
                    print("Izlaz iz programa.")
                    break
                else:
                    print("Nepostojeća opcija, pokušajte ponovo.")
    else:
        print("\nNeuspešno prijavljivanje! Pogrešno korisničko ime ili lozinka.")

if __name__ == "__main__":
    main()
