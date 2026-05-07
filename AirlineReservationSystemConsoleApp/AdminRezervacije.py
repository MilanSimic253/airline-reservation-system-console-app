# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:05:09 2025

@author: milan
"""

import Db
import matplotlib.pyplot as plt

def prikaziSveRezervacije():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT r.id, k.username, l.polazni_grad, l.dolazni_grad, 
           DATE_FORMAT(l.datum, '%d.%m.%Y.') as datum,
           DATE_FORMAT(l.vreme, '%H:%i') as vreme,
           r.broj_karata, 
           DATE_FORMAT(r.datum_rezervacije, '%d.%m.%Y.') as datum_rezervacije
    FROM rezervacije r, korisnici k, letovi l
    WHERE r.id_korisnika = k.id
    AND r.id_leta = l.id
    """
    cursor.execute(query)
    rezervacije = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rezervacije:
        print("\nTrenutno nema rezervacija.")
    else:
        print("\n--- Sve rezervacije ---")
        for r in rezervacije:
            print(f"ID rez: {r['id']} | Korisnik: {r['username']} | "
                  f"Let: {r['polazni_grad']} -> {r['dolazni_grad']} | "
                  f"Datum: {r['datum']} | Vreme: {r['vreme']} | "
                  f"Karte: {r['broj_karata']} | Rezervisano: {r['datum_rezervacije']}")

def obrisiRezervacijuAdmin():
    prikaziSveRezervacije()
    id_rez = input("\nUnesite ID rezervacije za brisanje: ")

    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rezervacije WHERE id = %s", (id_rez,))
    rez = cursor.fetchone()

    if not rez:
        print("Rezervacija sa tim ID-jem ne postoji.")
    else:
        id_leta = rez['id_leta']
        broj_karata = rez['broj_karata']

        cursor.execute("UPDATE letovi SET broj_mesta = broj_mesta + %s WHERE id = %s",
                       (broj_karata, id_leta))

        cursor.execute("DELETE FROM rezervacije WHERE id = %s", (id_rez,))
        conn.commit()
        print("Rezervacija je uspešno obrisana.")

    cursor.close()
    conn.close()
    
def prikaziRezervacijePoLetu():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT CONCAT(polazni_grad, ' -> ', dolazni_grad) AS ruta, SUM(r.broj_karata) AS ukupno
    FROM rezervacije r, letovi l
    WHERE r.id_leta = l.id
    GROUP BY ruta
    ORDER BY ukupno DESC
    """
    cursor.execute(query)
    rezultati = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rezultati:
        print("Nema rezervacija za prikaz grafikona.")
        return

    rute = [r['ruta'] for r in rezultati]
    karte = [r['ukupno'] for r in rezultati]

    plt.figure(figsize=(10,6))
    plt.bar(rute, karte, color='blue')
    plt.title("Prikaz rezervacija po letu")
    plt.xlabel("Let")
    plt.ylabel("Broj rezervisanih karata")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
def prikaziRezervacijePoDatumuLeta():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT DATE_FORMAT(datum, '%d.%m.%Y.') as datum_format, datum, SUM(r.broj_karata) AS ukupno
    FROM rezervacije r, letovi l
    WHERE r.id_leta = l.id
    GROUP BY datum
    ORDER BY datum
    """
    cursor.execute(query)
    rezultati = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rezultati:
        print("Nema rezervacija za prikaz grafikona.")
        return

    datumi = [r['datum_format'] for r in rezultati]
    karte = [r['ukupno'] for r in rezultati]

    plt.figure(figsize=(10,6))
    plt.plot(datumi, karte, marker='o', linestyle='-', color='purple')
    plt.title("Prikaz rezervacija po datumu leta")
    plt.xlabel("Datum leta")
    plt.ylabel("Broj rezervisanih karata")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def prikaziUkupanPrihodPoLetu():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT CONCAT(l.polazni_grad, ' -> ', l.dolazni_grad) AS ruta, 
           SUM(r.broj_karata * l.cena) AS zarada
    FROM rezervacije r, letovi l
    WHERE r.id_leta = l.id
    GROUP BY ruta
    ORDER BY zarada DESC
    """
    cursor.execute(query)
    rezultati = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rezultati:
        print("Nema rezervacija za prikaz grafikona.")
        return

    rute = [r['ruta'] for r in rezultati]
    zarade = [r['zarada'] for r in rezultati]

    plt.figure(figsize=(10,6))
    plt.bar(rute, zarade, color='red')
    plt.title("Ukupan prihod po letu")
    plt.xlabel("Let")
    plt.ylabel("Ukupan prihod")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()