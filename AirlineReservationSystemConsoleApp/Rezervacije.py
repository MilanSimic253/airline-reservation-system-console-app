# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:03:26 2025

@author: milan
"""

import Db

def prikaziDostupneLetove():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id, polazni_grad, dolazni_grad,
           DATE_FORMAT(datum, '%d.%m.%Y.') as datum,
           DATE_FORMAT(vreme, '%H:%i') as vreme,
           broj_mesta, cena
    FROM letovi 
    WHERE broj_mesta > 0
    """
    cursor.execute(query)
    letovi = cursor.fetchall()

    cursor.close()
    conn.close()

    if not letovi:
        print("\nNema dostupnih letova.")
    else:
        print("\n--- Dostupni letovi ---")
        for let in letovi:
            print(f"ID: {let['id']} | {let['polazni_grad']} -> {let['dolazni_grad']} | "
                  f"Datum: {let['datum']} | Vreme: {let['vreme']} | "
                  f"Mesta: {let['broj_mesta']} | Cena: {let['cena']}")

def rezervisiKarte(id_korisnika):
    prikaziDostupneLetove()
    id_leta = input("\nUnesite ID leta koji želite da rezervišete: ")
    broj_karata = int(input("Unesite broj karata: "))

    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM letovi WHERE id = %s", (id_leta,))
    let = cursor.fetchone()

    if not let:
        print("Let sa tim ID-jem ne postoji.")
    elif let['broj_mesta'] < broj_karata:
        print("Nema dovoljno slobodnih mesta.")
    else:
        insert_query = """
            INSERT INTO rezervacije (id_korisnika, id_leta, broj_karata)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (id_korisnika, id_leta, broj_karata))

        novo_stanje = let['broj_mesta'] - broj_karata
        cursor.execute("UPDATE letovi SET broj_mesta = %s WHERE id = %s", (novo_stanje, id_leta))

        conn.commit()
        print("Rezervacija je uspešno kreirana.")

    cursor.close()
    conn.close()

def prikaziRezervacije(id_korisnika):
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT r.id, l.polazni_grad, l.dolazni_grad, 
           DATE_FORMAT(l.datum, '%d.%m.%Y.') as datum,
           DATE_FORMAT(l.vreme, '%H:%i') as vreme,
           r.broj_karata, 
           DATE_FORMAT(r.datum_rezervacije, '%d.%m.%Y') as datum_rezervacije
    FROM rezervacije r, letovi l
    WHERE r.id_leta = l.id
    AND r.id_korisnika = %s
    """
    cursor.execute(query, (id_korisnika,))
    rezervacije = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rezervacije:
        print("\nNemate nijednu rezervaciju.")
    else:
        print("\n--- Moje rezervacije ---")
        for r in rezervacije:
            print(f"ID rezervacije: {r['id']} | Let: {r['polazni_grad']} -> {r['dolazni_grad']} | "
                  f"Datum: {r['datum']} | Vreme: {r['vreme']} | "
                  f"Karte: {r['broj_karata']} | Rezervisano: {r['datum_rezervacije']}")

def otkaziRezervaciju(id_korisnika):
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, l.polazni_grad, l.dolazni_grad, r.broj_karata
        FROM rezervacije r, letovi l
        WHERE r.id_leta = l.id
        AND r.id_korisnika = %s
    """, (id_korisnika,))
    prikazRezervacija = cursor.fetchall()

    if not prikazRezervacija:
        print("Nemate nijednu rezervaciju.")
        cursor.close()
        conn.close()
        return

    print("\n--- Vaše rezervacije ---")
    for r in prikazRezervacija:
        print(f"ID: {r['id']} | {r['polazni_grad']} -> {r['dolazni_grad']} | Karte: {r['broj_karata']}")

    id_rez = input("\nUnesite ID rezervacije koju želite da otkažete: ")

    cursor.execute("SELECT * FROM rezervacije WHERE id = %s AND id_korisnika = %s",
                   (id_rez, id_korisnika))
    rez = cursor.fetchone()

    if not rez:
        print("Ne postoji takva rezervacija ili ne pripada vama.")
    else:
        cursor.execute("UPDATE letovi SET broj_mesta = broj_mesta + %s WHERE id = %s",
                       (rez['broj_karata'], rez['id_leta']))
        cursor.execute("DELETE FROM rezervacije WHERE id = %s", (id_rez,))
        conn.commit()
        print("Rezervacija je uspešno otkazana.")

    cursor.close()
    conn.close()