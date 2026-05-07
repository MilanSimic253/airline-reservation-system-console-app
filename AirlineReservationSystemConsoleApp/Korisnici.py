# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:00:31 2025

@author: milan
"""

import Db

def login(username, password):
    conn = Db.getConnection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT k.id, k.username, u.naziv AS uloga
        FROM korisnici k, uloge u
        WHERE k.uloga_id = u.id
        AND k.username = %s 
        AND k.password = %s
        """
    cursor.execute(query, (username, password))
    rezultat = cursor.fetchone()

    cursor.close()
    conn.close()

    return rezultat