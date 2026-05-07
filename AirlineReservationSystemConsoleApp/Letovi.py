# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:01:47 2025

@author: milan
"""

import Db

def prikaziSveLetove():
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id, polazni_grad, dolazni_grad, 
           DATE_FORMAT(datum, '%d.%m.%Y.') as datum,
           DATE_FORMAT(vreme, '%H:%i') as vreme,
           broj_mesta, cena
    FROM letovi
    """
    cursor.execute(query)
    letovi = cursor.fetchall()

    cursor.close()
    conn.close()

    if not letovi:
        print("\nNema letova u bazi.")
    else:
        print("\n--- Lista letova ---")
        for let in letovi:
            print(f"ID: {let['id']} | {let['polazni_grad']} -> {let['dolazni_grad']} | "
                  f"Datum: {let['datum']} | Vreme: {let['vreme']} | "
                  f"Mesta: {let['broj_mesta']} | Cena: {let['cena']}")

def dodajLet():
    polazni = input("Polazni grad: ")
    dolazni = input("Dolazni grad: ")
    datum = input("Datum (DD.MM.YYYY.): ")
    vreme = input("Vreme (HH:MM): ")
    broj_mesta = input("Broj mesta: ")
    cena = input("Cena karte: ")

    delovi = datum.split('.')
    dan, mesec, godina = delovi[0], delovi[1], delovi[2]
    datum_mysql = f"{godina}-{mesec}-{dan}"

    conn = Db.getConnection()
    cursor = conn.cursor()

    query = """
        INSERT INTO letovi (polazni_grad, dolazni_grad, datum, vreme, broj_mesta, cena)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (polazni, dolazni, datum_mysql, vreme, broj_mesta, cena))
    conn.commit()

    cursor.close()
    conn.close()

    print("Let je uspešno dodat.")

def izmeniLet():
    prikaziSveLetove()
    id_leta = input("\nUnesite ID leta koji želite da izmenite: ")

    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, polazni_grad, dolazni_grad,
               datum as datum_original,
               DATE_FORMAT(datum, '%d.%m.%Y.') as datum,
               DATE_FORMAT(vreme, '%H:%i') as vreme,
               broj_mesta, cena
        FROM letovi WHERE id = %s
    """, (id_leta,))
    let = cursor.fetchone()

    if not let:
        print("Let sa tim ID-jem ne postoji.")
    else:
        print("Ostavite prazno polje ako ne želite da menjate podatak.")
        novi_polazni = input(f"Polazni grad ({let['polazni_grad']}): ") or let['polazni_grad']
        novi_dolazni = input(f"Dolazni grad ({let['dolazni_grad']}): ") or let['dolazni_grad']
        novi_datum = input(f"Datum ({let['datum']}): ")
        novo_vreme = input(f"Vreme ({let['vreme']}): ")
        novi_broj_mesta = input(f"Broj mesta ({let['broj_mesta']}): ") or let['broj_mesta']
        nova_cena = input(f"Cena ({let['cena']}): ") or let['cena']

        if novi_datum:
            delovi = novi_datum.split('.')
            dan, mesec, godina = delovi[0], delovi[1], delovi[2]
            novi_datum = f"{godina}-{mesec}-{dan}"
        else:
            novi_datum = let['datum_original']

        if not novo_vreme:
            novo_vreme = let['vreme']

        update_query = """
        UPDATE letovi
        SET polazni_grad=%s, dolazni_grad=%s, datum=%s, vreme=%s, broj_mesta=%s, cena=%s
        WHERE id=%s
        """
        cursor.execute(update_query, (
            novi_polazni, novi_dolazni, novi_datum, novo_vreme, novi_broj_mesta, nova_cena, id_leta
        ))
        conn.commit()
        print("Let je uspešno izmenjen.")

    cursor.close()
    conn.close()

def obrisiLet():
    prikaziSveLetove()
    id_leta = input("\nUnesite ID leta koji želite da obrišete: ")

    conn = Db.getConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM letovi WHERE id = %s", (id_leta,))
    postoji = cursor.fetchone()

    if not postoji:
        print("Let sa tim ID-jem ne postoji.")
    else:
        cursor.execute("DELETE FROM letovi WHERE id = %s", (id_leta,))
        conn.commit()
        print("Let je obrisan.")

    cursor.close()
    conn.close()