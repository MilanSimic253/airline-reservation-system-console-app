CREATE DATABASE IF NOT EXISTS sj_aviokarte;
USE sj_aviokarte;

CREATE TABLE uloge (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naziv VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO uloge (naziv)
VALUES ('admin'), ('korisnik');

CREATE TABLE korisnici (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    uloga_id INT NOT NULL,
    FOREIGN KEY (uloga_id) REFERENCES uloge(id)
);

CREATE TABLE letovi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    polazni_grad VARCHAR(50) NOT NULL,
    dolazni_grad VARCHAR(50) NOT NULL,
    datum DATE NOT NULL,
    vreme TIME NOT NULL,
    broj_mesta INT NOT NULL,
    cena INT NOT NULL
);

CREATE TABLE rezervacije (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_korisnika INT NOT NULL,
    id_leta INT NOT NULL,
    broj_karata INT NOT NULL,
    datum_rezervacije DATETIME DEFAULT NOW(),
    FOREIGN KEY (id_korisnika) REFERENCES korisnici(id),
    FOREIGN KEY (id_leta) REFERENCES letovi(id)
);

INSERT INTO korisnici (username, password, uloga_id)
VALUES ('admin', 'admin', 1),
       ('korisnik1', 'korisnik1', 2),
       ('korisnik2', 'korisnik2', 2);

INSERT INTO letovi (polazni_grad, dolazni_grad, datum, vreme, broj_mesta, cena)
VALUES ('Beograd', 'Pariz', '2025-10-15', '07:30', 180, 285),
       ('Pariz', 'Beograd', '2025-10-20', '18:40', 180, 285),
       ('Beograd', 'Frankfurt', '2025-10-17', '14:50', 120, 195),
       ('Frankfurt', 'Beograd', '2025-10-22', '19:15', 120, 195),
       ('Beograd', 'Istanbul', '2025-10-16', '22:10', 189, 165),
       ('Istanbul', 'Beograd', '2025-10-23', '08:45', 189, 165),
       ('Niš', 'Beč', '2025-10-18', '06:15', 76, 145),
       ('Beč', 'Niš', '2025-10-24', '20:35', 76, 145),
       ('Niš', 'Rim', '2025-10-19', '13:20', 180, 89),
       ('Rim', 'Niš', '2025-10-25', '17:25', 180, 89);
