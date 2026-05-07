# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 13:59:27 2025

@author: milan
"""

import mysql.connector

def getConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='sj_aviokarte'
    )
    return conn