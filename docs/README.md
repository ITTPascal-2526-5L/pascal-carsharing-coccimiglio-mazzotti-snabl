# Documentazione Progetto Pascal Car Sharing

Benvenuti nella documentazione completa del progetto Pascal Car Sharing.

## Indice Documentazione

### 📘 [Documentazione Completa](./DOCUMENTAZIONE.md)
Documentazione dettagliata del progetto che include:
- Panoramica del progetto
- Architettura del sistema
- Documentazione delle feature implementate
- Diagramma delle classi
- Guida ai test
- Installazione e configurazione

### 📊 [Diagramma delle Classi](./DIAGRAMMA_CLASSI.md)
Documentazione dettagliata del diagramma delle classi con:
- Diagramma UML in formato Mermaid
- Descrizione di ogni classe
- Relazioni tra classi
- Pattern di design utilizzati
- Flusso di dati

### 📐 [Diagramma PlantUML](./DIAGRAMMA_CLASSI.puml)
File PlantUML per generare il diagramma delle classi. Può essere visualizzato con:
- [PlantUML Online](http://www.plantuml.com/plantuml/uml/)
- Plugin per IDE (IntelliJ, VS Code, ecc.)
- Tool da linea di comando

### 🧪 [Guida ai Test](../tests/README.md)
Documentazione completa sui test:
- Come eseguire i test
- Struttura dei test
- Coverage target
- Best practices

## Quick Start

### Leggere la Documentazione

1. Inizia con la [Documentazione Completa](./DOCUMENTAZIONE.md) per una panoramica generale
2. Consulta il [Diagramma delle Classi](./DIAGRAMMA_CLASSI.md) per capire l'architettura
3. Leggi la [Guida ai Test](../tests/README.md) per eseguire i test

### Eseguire i Test

```bash
# Installare dipendenze
pip install -r requirements.txt

# Eseguire tutti i test
pytest

# Eseguire con coverage
pytest --cov=app --cov-report=html
```

### Visualizzare il Diagramma

1. Aprire `DIAGRAMMA_CLASSI.puml` in un editor che supporta PlantUML
2. Oppure copiare il contenuto di `DIAGRAMMA_CLASSI.md` in un editor Markdown che supporta Mermaid

## Struttura Documentazione

```
docs/
├── README.md                    # Questo file (indice)
├── DOCUMENTAZIONE.md            # Documentazione completa
├── DIAGRAMMA_CLASSI.md          # Diagramma classi (Mermaid)
└── DIAGRAMMA_CLASSI.puml        # Diagramma classi (PlantUML)
```

## Contatti

Per domande o chiarimenti sulla documentazione, contattare il team di sviluppo.

