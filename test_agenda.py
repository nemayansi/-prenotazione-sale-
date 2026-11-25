import unittest
from datetime import date, timedelta
from prenotazioni import (
    Agenda,
    Sala,
    SalaNonTrovata,
    DataNonAmmessa,
    Prenotazione,
    ORIZZONTE_GIORNI,
    PrenotazioneNonTrovata,
)
class TestAgenda(unittest.TestCase):

    def setUp(self):
        self.agenda = Agenda()
        self.sala = Sala("Sala1", "Piano 1", 10)
        self.agenda.aggiungi_sala(self.sala)
        # 2026-11-18 e' un mercoledi'
        self.oggi = date(2026, 11, 18)

    def test_sale(self):
        sala_duplicata = Sala("Sala1", "Piano 1", 15)
        with self.assertRaises(ValueError):
            self.agenda.aggiungi_sala(sala_duplicata)

        with self.assertRaises(SalaNonTrovata):
            self.agenda.sala("XX")

    def test_prenota_data_passata(self):
        ieri = self.oggi - timedelta(days=1)
        pren = Prenotazione("Sala1", ieri, "09:00", "12:00", "Giovanni", 1)
        with self.assertRaises(DataNonAmmessa):
            self.agenda.prenota(pren, oggi=self.oggi)

    def test_prenota_domenica(self):
        # 2026-11-22 e' domenica
        domenica = date(2026, 11, 22)
        pren = Prenotazione("Sala1", domenica, "09:00", "12:00", "Giovanni", 1)
        with self.assertRaises(DataNonAmmessa):
            self.agenda.prenota(pren, oggi=self.oggi)

    def test_prenota_oltre_orizzonte(self):
        oltre_orizzonte = self.oggi + timedelta(days=ORIZZONTE_GIORNI + 1)
        pren = Prenotazione("Sala1", oltre_orizzonte, "09:00", "12:00", "Giovanni", 1)
        with self.assertRaises(DataNonAmmessa):
            self.agenda.prenota(pren, oggi=self.oggi)

    def test_prenota_accetta_oggi(self):
        pren = Prenotazione("Sala1", self.oggi, "09:00", "12:00", "Giovanni", 1)
        id_pren = self.agenda.prenota(pren, oggi=self.oggi)
        self.assertEqual(self.agenda.prenotazione(id_pren), pren)

    def test_id_inesistenti(self):
        with self.assertRaises(PrenotazioneNonTrovata):
            self.agenda.prenotazione("x")
        with self.assertRaises(PrenotazioneNonTrovata):
            self.agenda.cancella("x")


if __name__ == "__main__":
    unittest.main()