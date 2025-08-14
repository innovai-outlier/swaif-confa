# Repository Inventory

## Repo Tree (depth 2)
```
.
├── main.py
├── scripts/
│   ├── conciliacao.py
│   └── extract_headers.py
├── src/
│   ├── controllers/
│   │   └── conciliacao_controller.py
│   ├── models/
│   │   ├── analisador.py
│   │   └── data_loader.py
│   └── views/
│       └── terminal_view.py
├── tests/
│   ├── fixtures/
│   │   └── test_data.py
│   ├── integration/
│   │   └── test_integration.py
│   ├── unit/
│   │   ├── test_analisador.py
│   │   ├── test_controller.py
│   │   ├── test_data_loader.py
│   │   └── test_terminal_view.py
│   ├── test_runner.py
│   └── test_runner_new.py
├── test_conversao_wab.py
├── test_debug_valores.py
├── test_formatacao.py
├── teste_fluxo.py
├── teste_simples.py
└── teste_totais.py
```

## Tools & Versions
- Python: 3.12.10
- Pytest: 8.4.1
- Ruff: 0.12.7
- Mypy: 1.17.1

## Scripts & Entry Points
- `main.py` – possible CLI entry
- `scripts/conciliacao.py`
- `scripts/extract_headers.py`

## CLI/UI Entry Paths
- CLI: `main.py`
- UI: `src/views/terminal_view.py` (terminal interface)

## Dependencies (from imports)
- `pandas`
- standard library modules (`os`, `logging`, etc.)

## MVC Structure
- Models: `src/models/`
- Controllers: `src/controllers/`
- Views: `src/views/`
