import unittest
from datetime import date, timedelta
from prenotazioni import Prenotazione, GIORNO_CHIUSURA, DataNonAmmessa, Agenda, Sala

class TestPrenotazioni(unittest.TestCase):
    def test_orari_non_ammessi(self):
        with self.assertRaises(ValueError):
            Prenotazione("Sala1", date(2026, 11, 19), "10:00", "10:00","Nouhaila", 1)
        orari_non_ammessi = [
            ("07:15", "08:00"),
            ("04:00", "12:00"),
            ("12:00", "23:00"),
            ("12:00", "11:00")
        ]
        for inizio, fine in orari_non_ammessi:
            with self.assertRaises(ValueError):
                Prenotazione("Sala1", date(2026, 11, 18), inizio, fine,"Nouhaila", 1)
    def test_giorno_non_data(self):
            with self.assertRaises(TypeError):
                Prenotazione("Sala1", "2026-11-06", "07:00", "08:00","Nouhaila", 1)
    def test_durata_minuti(self):
            prenotazione = Prenotazione("Sala1", date(2026, 11, 18), "09:00", "12:30","Nouhaila", 1)
            self.assertEqual(prenotazione.durata_minuti(), 210)
