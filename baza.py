import csv

def pobrisi_tabele(conn):
    """
    Pobriše tabele iz baze.
    """
    conn.execute("DROP TABLE IF EXISTS karta;")
    conn.execute("DROP TABLE IF EXISTS postaja;")
    conn.execute("DROP TABLE IF EXISTS proga;")
    conn.execute("DROP TABLE IF EXISTS vlak;")
    conn.execute("DROP TABLE IF EXISTS dan;")
    conn.execute("DROP TABLE IF EXISTS vmesne_postaje;")

def ustvari_tabele(conn):
    """
    Ustvari tabele v bazi.
    """
    conn.execute("""
        CREATE TABLE karta (
            datum DATE REFERENCES dan (datum),
            tip   TEXT,-- dvosmerna, enosmerna
            od    INT  REFERENCES postaja (id),
            kam   INT  REFERENCES postaja (id) 
        );
    """)
    conn.execute("""
        CREATE TABLE postaja (
        id  INT  PRIMARY KEY,
        ime TEXT
        );
    """)
    conn.execute("""
        CREATE TABLE proga (
            šifra           INT  PRIMARY KEY,
            tip             TEXT,-- intercity, mednarodni, potniški ipd verjetno xDD1
            zacetna_postaja INT  REFERENCES postaja (id),
            koncna_postaja  INT  REFERENCES postaja (id),
            ura_prihoda     TIME,
            ura_odhoda      TIME
        );
    """)
    conn.execute("""
        CREATE TABLE vlak (
            reg     TEXT PRIMARY KEY,
            vozi_na INT  REFERENCES proga (šifra) --,
            -- od      INT  REFERENCES postaja (id),
            -- kam     INT  REFERENCES postaja (id) 
        );
    """)
    conn.execute("""
        CREATE TABLE dan (
            datum DATE PRIMARY KEY,
            vlak       REFERENCES vlak (reg),
            proga      REFERENCES proga (šifra) 
        );
    """)
    conn.execute("""
        CREATE TABLE vmesne_postaje (
        vedno      TEXT,
        id_postaje INT  REFERENCES postaja (id),
        id_proge   INT  REFERENCES proga (id) 
    );
    """)

def uvozi_karta(conn):
    """
    Uvozi podatke o kartah.
    """
    conn.execute("DELETE FROM karta;")

    with open('Podatki/karta.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_postaja(conn):
    """
    Uvozi podatke o postajah.
    """
    conn.execute("DELETE FROM proga;")
    conn.execute("DELETE FROM karta;")
    conn.execute("DELETE FROM vmesne_postaje;")
    conn.execute("DELETE FROM vlak;")
    conn.execute("DELETE FROM postaja;")

    with open('Podatki/postaja.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_proga(conn):
    """
    Uvozi podatke o progah.
    """
    conn.execute("DELETE FROM vlak;")
    conn.execute("DELETE FROM dan;")
    conn.execute("DELETE FROM vmesne_postaje;")
    conn.execute("DELETE FROM proga;")

    with open('Podatki/proga.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_vlak(conn):
    """
    Uvozi podatke o vlakih.
    """
    conn.execute("DELETE FROM dan;")
    conn.execute("DELETE FROM vlak;")

    with open('Podatki/vlak.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_dan(conn):
    """
    Uvozi podatke o tem kateri vlak vozi po kateri progi v nekem dnevu.
    """
    conn.execute("DELETE FROM karta;")
    conn.execute("DELETE FROM dan;")

    with open('Podatki/dan.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def uvozi_vmesne_postaje(conn):
    """
    Uvozi podatke o tem kateri vlak vozi po kateri progi, v nekem dnevu.
    """

    conn.execute("DELETE FROM vmesne_postaje;")

    with open('Podatki/vmesne_postaje.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO igralci VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            conn.execute(poizvedba, vrstica)

def ustvari_bazo(conn):
    """
    Opravi celoten postopek postavitve baze.
    """
    pobrisi_tabele(conn)
    ustvari_tabele(conn)
    uvozi_karta(conn)
    uvozi_postaja(conn)
    uvozi_proga(conn)
    uvozi_vlak(conn)
    uvozi_dan(conn)
    uvozi_vmesne_postaje(conn)

def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        conn = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if conn.fetchone() == (0, ):
            ustvari_bazo(conn)