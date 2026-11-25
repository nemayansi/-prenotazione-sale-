# Esame – Seconda parte: test e correzioni del motore, con git

**Consegna:** la cartella `esame2` compressa in un unico file `.zip`,
comprendente `progetto/` con la cartella nascosta `.git`, senza l'ambiente
virtuale.

**Regole di svolgimento:**

- non è consentito nessun tipo di ausilio generato da IA, compresi gli
  strumenti integrati nell'editor e in GitHub, come Copilot;
- non è consentita la collaborazione con colleghi e colleghe;
- è consentito l'uso di risorse web passive e dei motori di ricerca.

**Prerequisito:** un account GitHub personale, con l'autenticazione da riga
di comando già configurata e verificata prima della prova (token di accesso
personale o chiave SSH).

## 1. Obiettivo

Si riceve il codice del motore di prenotazione delle sale, funzionante e
corredato dell'interfaccia web, con un solo file di test. La segreteria ha
segnalato due difetti.

Il lavoro consiste in due attività:

1. per ciascun difetto, seguire le indicazioni fornite per individuarlo,
   scrivere un test che lo riproduce e correggerlo;
2. scrivere alcuni test per le parti del motore che funzionano
   correttamente.

Il lavoro si svolge con git su un repository GitHub personale, come se altre
persone potessero lavorare contemporaneamente sullo stesso repository. La
valutazione si basa sulla storia del repository consegnato: ogni commit,
cambio di ramo, merge e invio a GitHub resta registrato da git con data e
ora, e viene esaminato con uno script.

Le docstring di `prenotazioni.py` costituiscono la **specifica**: i test
verificano che il codice rispetti quanto vi è scritto. Le convenzioni del
`README.md` del progetto su rami, commit e test sono **vincolanti**.

## 2. Materiale fornito

```
esame2/
  TRACCIA.md        questo documento
  progetto/         codice del motore e dell'interfaccia web
```

`progetto/test_orari.py` è un file di test completo, che passa. Serve da
modello per i test da scrivere: struttura, nomi, uso di `subTest` e
`assertRaises`. La cartella `progetto/` non è ancora un repository git.

## 3. Preparazione del repository

1. creare un repository **privato** chiamato `prenotazione-sale` su GitHub.
   Può contenere i file che GitHub propone (README, `.gitignore`, licenza);
2. nella cartella `esame2`, rinominare la cartella fornita `progetto` in
   `codice`, poi clonare il repository con
   `git clone <indirizzo del repository> progetto` e copiare dentro
   `progetto` tutto il contenuto di `codice`, sostituendo eventuali file con
   lo stesso nome;
3. configurare nel repository il proprio nome e la propria email
   (`git config user.name`, `git config user.email`) e il comportamento di
   `git pull` in caso di rami divergenti: `git config pull.rebase false`;
4. creare e attivare un ambiente virtuale `.venv` nella cartella `progetto`;
   installare le dipendenze con `pip install -r requirements.txt`;
5. creare o modificare il file `.gitignore` perché escluda almeno:
   - l'ambiente virtuale;
   - le cartelle `__pycache__`;
   - il file `dati/agenda.json`;
6. verificare con `git status` che compaiano solo i file del progetto e il
   `.gitignore`, poi registrarli in un commit con il messaggio
   `Importa il codice del motore di prenotazione`. È l'unico commit ammesso
   direttamente su `main`, oltre a quelli eventualmente creati da GitHub;
7. inviare `main` con `git push`.

## 4. Modo di lavorare con git

Si assume che altre persone possano inviare in qualsiasi momento modifiche al
repository GitHub. Ogni ramo segue quindi questa sequenza.

**Avvio**, da `main` aggiornato con il remoto:

```
git switch main
git pull
git switch -c <ramo>
```

**Lavoro sul ramo:**

- prima di ogni commit, controllare `git status` e `git diff`;
- aggiungere esplicitamente i file da includere (`git add <file>`);
- dopo i commit, inviare il ramo a GitHub: `git push`.

**Integrazione in `main`:**

```
git switch main
git pull
git merge <ramo>
python -m unittest discover
git push
```

`git pull` aggiorna `main` con le modifiche eventualmente giunte
nel frattempo. Se il merge produce un conflitto, lo si risolve, si
completa il merge con `git commit` e si eseguono i test. Se il `push` viene
rifiutato perché GitHub contiene commit non presenti in locale, si esegue
`git pull`, si rieseguono i test e si ripete il `push`.

**Operazioni non ammesse:**

- `git push --force` e `git push --force-with-lease`;
- `git reset --hard`, `git rebase` e `git commit --amend` su commit già
  inviati;
- commit diretti su `main`, dopo il primo;
- eliminazione di rami, locali o remoti: i rami restano nel repository anche
  dopo l'integrazione, perché la valutazione li ricostruisce da lì.

Se si commette un errore, lo si corregge con un nuovo commit. Tutte le
operazioni git vanno eseguite da riga di comando: le funzioni git
dell'editor, GitHub Desktop e simili non vanno usati. Su GitHub, dal browser,
si esegue solo la creazione del repository.

## 5. Attività 1 – Correzione dei difetti segnalati

> **Segnalazione 1.** Martedì l'Aula 2 è prenotata dalle 9:00 alle 10:00. Se
> provo a prenotarla dalle 10:00 alle 11:00 dello stesso giorno, il sistema
> risponde che la sala è già occupata, anche se la riunione precedente a
> quell'ora sarà finita.
>
> *Indicazioni.* Il rifiuto è un `ConflittoOrario`, sollevato da
> `Agenda.prenota` quando `Prenotazione.si_sovrappone` restituisce `True`.
> La docstring di `si_sovrappone` dice che due prenotazioni contigue non si
> sovrappongono: confrontare il codice del metodo con la docstring.

> **Segnalazione 2.** La sala riunioni ha 10 posti. Non riesco a prenotarla
> per una riunione di 10 persone: il sistema risponde che la capienza non è
> sufficiente.
>
> *Indicazioni.* Il rifiuto è una `CapienzaInsufficiente`, sollevata da
> `Agenda.prenota` al controllo numero 4 della sua docstring. Confrontare la
> condizione scritta nel codice con quella descritta nella docstring.

Per **ciascuna** segnalazione, su un ramo `fix/<descrizione>` avviato come
indicato nella sezione 4:

1. scrivere nel file `test_segnalazioni.py` un test che riproduce il
   problema descritto e verifica il comportamento previsto dalla specifica.
   Registrarlo in un commit, poi eseguirlo: **deve fallire**;
2. correggere `prenotazioni.py` con la modifica minima necessaria e
   registrarla in un commit distinto. Ora tutti i test devono passare;
3. inviare il ramo e integrarlo in `main` come indicato nella sezione 4.

Alla fine, `test_segnalazioni.py` contiene due test, uno per segnalazione.

## 6. Attività 2 – Test delle parti funzionanti

Su un ramo `test/motore`, scrivere due file di test. Ogni file va registrato
in un commit distinto. I test richiesti sono i seguenti; ciascuno può
comprendere più casi, ad esempio con `subTest`.

**`test_prenotazione.py`** – classe `Prenotazione`:

1. il costruttore solleva `ValueError` per orari non ammessi: inizio non
   multiplo di 30 minuti, inizio prima dell'apertura, fine dopo la chiusura,
   fine non successiva all'inizio;
2. il costruttore solleva `TypeError` se il giorno non è un `date`;
3. `durata_minuti` restituisce la durata corretta.

**`test_agenda.py`** – classe `Agenda`:

1. `aggiungi_sala` rifiuta un codice duplicato con `ValueError`; `sala`
   solleva `SalaNonTrovata` per un codice inesistente;
2. `prenota` solleva `DataNonAmmessa` per una data passata, una domenica e
   una data oltre l'orizzonte, e accetta la data di oggi;
3. `cancella` e `prenotazione` sollevano `PrenotazioneNonTrovata` per un id
   inesistente.

Al termine, inviare il ramo e integrarlo in `main` come indicato nella
sezione 4. Durante questa attività `prenotazioni.py` **non va modificato**:
dopo l'attività 1 il motore è conforme alla specifica, e se un test
fallisce va riletta la specifica.

## 7. Requisiti per i test

- Si usa esclusivamente `unittest`. I file `test_*.py` stanno nella cartella
  principale del progetto e la suite si esegue con
  `python -m unittest discover -v`.
- I test verificano il comportamento descritto nelle docstring. Un test che
  fallisce su codice conforme alla specifica è un errore del test.
- I test **non devono dipendere dalla data in cui vengono eseguiti**: a
  `prenota` va sempre passato il parametro `oggi`, con date fisse. Il giorno
  di chiusura (domenica) si usa solo quando è l'oggetto della verifica.
- Ogni test verifica un singolo comportamento e ha un nome che lo descrive.
  Il corpo segue lo schema preparazione, azione, verifica.
- Le eccezioni attese si verificano con `assertRaises`. La preparazione
  comune a più test di una classe va in `setUp`.
- `server.py`, la pagina HTML e il foglio di stile non sono oggetto di test.
- Anche i file di test devono superare `ruff check .` e
  `ruff format --check .`.

## 8. Chiusura e consegna

1. Verificare che tutto sia registrato e inviato: `git status` non deve
   mostrare modifiche, `git branch -vv` non deve indicare rami in anticipo
   (*ahead*) rispetto al remoto.
2. Eliminare la cartella `progetto/.venv`, che si ricrea con
   `pip install -r requirements.txt`.
3. Comprimere la cartella `esame2` in un file `.zip`. Prima di consegnare,
   verificare che l'archivio contenga `progetto/.git`: alcuni strumenti di
   compressione escludono le cartelle nascoste. Senza `.git` la storia del
   lavoro non è valutabile.

## 9. Criteri di valutazione

- **Correzioni.** Per ogni segnalazione: test che riproduce il problema e
  fallisce prima della correzione; correttezza e misura della correzione.
- **Test delle parti funzionanti.** Presenza dei test richiesti, correttezza
  (devono passare sul motore conforme alla specifica), leggibilità.
- **Uso di git.** Rispetto della procedura della sezione 4 e delle
  convenzioni del `README.md`, ricostruito dalla storia e dai registri
  interni del repository consegnato.
