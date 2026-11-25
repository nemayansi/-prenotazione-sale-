import unittest
from datetime import date
from prenotazioni import Agenda, Sala, Prenotazione, ConflittoOrario


class Segnalazione1(unittest.TestCase):

    def setUp(self):
        self.agenda = Agenda()
        self.aula2 = Sala("Aula2", "Piano 1", 20)
        self.agenda.aggiungi_sala(self.aula2)
        # 2026-11-18 e' un mercoledi'; 2026-11-24 e' un martedi'
        self.oggi = date(2026, 11, 18)

    def test_prenotazioni_contigue_stesso_giorno_non_in_conflitto(self):
        martedi = date(2026, 11, 24)
        p1 = Prenotazione("Aula2", martedi, "09:00", "10:00", "Giulia", 2)
        p2 = Prenotazione("Aula2", martedi, "10:00", "11:00", "Marco", 2)

        self.assertFalse(p1.si_sovrappone(p2))
        self.assertFalse(p2.si_sovrappone(p1))

        id_1 = self.agenda.prenota(p1, oggi=self.oggi)
        id_2 = self.agenda.prenota(p2, oggi=self.oggi)

        self.assertEqual(self.agenda.prenotazione(id_1), p1)
        self.assertEqual(self.agenda.prenotazione(id_2), p2)

    def test_prenotazioni_sovrapposte_sollevano_conflitto_orario(self):
        martedi = date(2026, 11, 24)
        p1 = Prenotazione("Aula2", martedi, "09:00", "10:30", "Giulia", 2)
        p2 = Prenotazione("Aula2", martedi, "10:00", "11:00", "Marco", 2)

        self.assertTrue(p1.si_sovrappone(p2))
        self.agenda.prenota(p1, oggi=self.oggi)

        with self.assertRaises(ConflittoOrario):
            self.agenda.prenota(p2, oggi=self.oggi)
import unittest
from datetime import date
from prenotazioni import Agenda, Sala, Prenotazione, ConflittoOrario, CapienzaInsufficiente


class Segnalazione1(unittest.TestCase):

    def setUp(self):
        self.agenda = Agenda()
        self.aula2 = Sala("Aula2", "Piano 1", 20)
        self.agenda.aggiungi_sala(self.aula2)
        # 2026-11-18 e' un mercoledi'; 2026-11-24 e' un martedi'
        self.oggi = date(2026, 11, 18)

    def test_prenotazioni_contigue_stesso_giorno_non_in_conflitto(self):
        martedi = date(2026, 11, 24)
        p1 = Prenotazione("Aula2", martedi, "09:00", "10:00", "Giulia", 2)
        p2 = Prenotazione("Aula2", martedi, "10:00", "11:00", "Marco", 2)

        self.assertFalse(p1.si_sovrappone(p2))
        self.assertFalse(p2.si_sovrappone(p1))

        id_1 = self.agenda.prenota(p1, oggi=self.oggi)
        id_2 = self.agenda.prenota(p2, oggi=self.oggi)

        self.assertEqual(self.agenda.prenotazione(id_1), p1)
        self.assertEqual(self.agenda.prenotazione(id_2), p2)

    def test_prenotazioni_sovrapposte_sollevano_conflitto_orario(self):
        martedi = date(2026, 11, 24)
        p1 = Prenotazione("Aula2", martedi, "09:00", "10:30", "Giulia", 2)
        p2 = Prenotazione("Aula2", martedi, "10:00", "11:00", "Marco", 2)

        self.assertTrue(p1.si_sovrappone(p2))
        self.agenda.prenota(p1, oggi=self.oggi)

        with self.assertRaises(ConflittoOrario):
            self.agenda.prenota(p2, oggi=self.oggi)
class Segnalazione2(unittest.TestCase):

    def setUp(self):
        self.oggi = date(2026, 11, 18)
        self.agenda = Agenda()
        self.sala = Sala("Sala1", "Piano 1", 10)
        self.agenda.aggiungi_sala(self.sala)

    def test_prenota_capienza_esatta_consentita(self):
        pren = Prenotazione("Sala1", self.oggi, "09:00", "10:00", "Elena", 10)
        id_pren = self.agenda.prenota(pren, oggi=self.oggi)
        self.assertEqual(self.agenda.prenotazione(id_pren), pren)

    def test_prenota_capienza_superata_solleva_capienza_insufficiente(self):
        pren = Prenotazione("Sala1", self.oggi, "10:00", "11:00", "Elena", 11)
        with self.assertRaises(CapienzaInsufficiente):
            self.agenda.prenota(pren, oggi=self.oggi)