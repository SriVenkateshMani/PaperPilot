# PaperPilot

PaperPilot is a production-grade, agentic RAG system for research papers.

The idea is simple: research papers are useful, but reading 47 PDFs to answer one question is a deeply questionable life choice. PaperPilot continuously ingests papers from arXiv, turns them into searchable knowledge, retrieves the right evidence, and generates grounded answers with citations.

In other words:

```text
arXiv publishes papers
        ↓
PaperPilot quietly does a suspicious amount of work
        ↓
You ask a question
        ↓
You get an answer grounded in actual papers
```

No Ctrl+F marathon. No 19 browser tabs. No pretending you read the appendix.

## What it actually does

PaperPilot runs a full ingestion, retrieval, and reasoning pipeline.

### 1. Airflow keeps the knowledge base alive

Airflow orchestrates the ingestion workflow on a schedule instead of relying on someone to remember to run a Python script every morning like it is 2007.

A typical DAG handles:

```text
search arXiv
→ filter/select papers
→ store metadata
→ download PDFs
→ parse documents
→ chunk content
→ generate embeddings
→ index searchable content
```

Airflow gives the pipeline scheduling, dependency management, retries, observability, and task-level failure handling. If PDF #83 decides to ruin everyone's day, the entire pipeline does not need to become emotionally involved.

The ingestion jobs are designed to be idempotent, so rerunning a failed or scheduled workflow should not create a small army of duplicate papers.

## 2. Scientific PDFs get turned into usable knowledge

Research PDFs are not exactly famous for being machine-friendly. Two-column layouts, equations, tables, headings, references, captions... beautiful for academia, mildly hostile to software.

PaperPilot uses **Docling** to parse papers into structured document content before converting that content into text suitable for retrieval.

The parsed content is then split into overlapping chunks so retrieval happens at the useful passage level instead of throwing an entire 28-page paper at an LLM and wishing it luck.

```text
PDF
→ structured document
→ normalized text
→ chunks
```

Each chunk keeps enough metadata to trace it back to its source paper, which later allows answers to point back to the evidence they came from.

## 3. Chunks become searchable in two completely different ways

Each chunk is indexed for both lexical and semantic retrieval.

**BM25** handles classic keyword relevance. It is great when terminology matters and the user's query contains words that also appear in the paper.

**Vector search** handles semantic similarity. The chunk and the user's query are converted into embeddings, allowing PaperPilot to retrieve relevant passages even when the wording is different.

Then PaperPilot combines both signals using **hybrid retrieval**.

```text
User query
   ├── BM25 search
   └── vector search
          ↓
    merged / ranked results
          ↓
      best evidence
```

Because sometimes exact words matter, sometimes meaning matters, and betting the entire retrieval system on only one of them feels unnecessarily brave.

## 4. Retrieval becomes RAG

Once PaperPilot retrieves the strongest chunks, those passages become context for the LLM.

```text
question
→ retrieve relevant chunks
→ construct grounded context
→ LLM generates answer
→ return answer + supporting sources
```

The important part is that the model is not supposed to freestyle its way through research knowledge. The answer is generated from retrieved evidence and is designed to remain traceable to the underlying papers.

That is the **Retrieval-Augmented Generation** part of PaperPilot.

## 5. Then things get agentic 🤖

Not every research question should be solved with one search call and one prompt.

PaperPilot adds a **LangGraph-based agentic retrieval layer** that can reason about the retrieval process itself.

Depending on the question, the workflow can:

- rewrite a weak or ambiguous query,
- retrieve evidence,
- grade whether retrieved passages are actually relevant,
- retry retrieval when evidence is poor,
- gather additional context,
- and only then generate the final grounded response.

Conceptually:

```text
User asks question
        ↓
understand / rewrite query
        ↓
retrieve evidence
        ↓
Is the evidence good enough?
     ↙             ↘
   nope             yep
    ↓                ↓
retrieve again     generate answer
    ↓                ↓
    └──────────────→ citations
```

So instead of:

> search once → hope for the best

PaperPilot moves toward:

> search → evaluate → correct → answer

Much healthier.

## High-level production architecture

```text
                         ┌─────────────────┐
                         │      arXiv      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Airflow     │
                         │ ingestion DAGs  │
                         └────────┬────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
            metadata         PDF parsing       embeddings
           PostgreSQL          Docling        Transformer
                 │                │                │
                 └────────────────┴────────┬───────┘
                                           ▼
                                   ┌───────────────┐
                                   │  OpenSearch   │
                                   │ BM25 + vector │
                                   └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │    Hybrid     │
                                   │   Retrieval   │
                                   └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │   LangGraph   │
                                   │ agentic RAG   │
                                   └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │    FastAPI    │
                                   └───────┬───────┘
                                           │
                                           ▼
                                    grounded answer
                                     + citations
```

That is the whole game.

One side continuously **builds the knowledge base**.

The other side **answers questions against it**.

Airflow owns the recurring ingestion work. OpenSearch powers retrieval. LangGraph handles the "hmm, that retrieval was terrible, maybe try again" intelligence. FastAPI exposes the system to whatever frontend or client eventually decides to bother it.

## Production-minded behavior

PaperPilot is being built as more than a notebook demo where everything works beautifully until someone refreshes the page.

The production version is designed around:

- scheduled and restartable ingestion workflows,
- idempotent processing,
- retries and failure isolation,
- structured logging,
- persistent metadata,
- reproducible document processing,
- searchable chunk-level provenance,
- hybrid retrieval,
- relevance evaluation,
- grounded generation,
- source attribution,
- API boundaries between retrieval and clients,
- and containerized services for reproducible environments.

Basically, the goal is not:

```text
"look mom, similarity search"
```

The goal is:

```text
"this thing can ingest new research continuously,
recover when parts fail,
find useful evidence,
and answer questions without hallucinating the plot."
```

## Tech stack

**Backend**

Python 3.12, FastAPI, Uvicorn, SQLAlchemy, psycopg

**Data + Search**

PostgreSQL 16, OpenSearch 2.19.3

**AI / Retrieval**

Docling, Sentence Transformers, LangChain text splitters, BM25, vector search, hybrid retrieval, LangGraph

**Workflow orchestration**

Apache Airflow

**Infrastructure**

Docker, Docker Compose

## Running locally

Start the stack:

```bash
docker compose up --build -d
```

Check that everything is alive and not having a crisis:

```bash
docker compose ps
```

Run the ingestion pipeline manually while developing:

```bash
docker compose exec api python -m app.ingestion.run_ingestion
```

Airflow takes over scheduled orchestration as the production ingestion workflow is wired in.

## Where PaperPilot is headed

The finished flow looks like this:

```text
arXiv
→ scheduled Airflow ingestion
→ parse + chunk + embed
→ lexical + vector indexing
→ hybrid retrieval
→ relevance grading / query rewriting
→ LangGraph agentic workflow
→ grounded RAG generation
→ answer with supporting sources
```

Which is admittedly a lot of machinery for asking research papers questions.

But if we are going to overengineer something, it might as well be useful. 😌
