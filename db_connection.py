import sqlite3

def connect_db():
    conn = sqlite3.connect("cricket.db")
    return conn