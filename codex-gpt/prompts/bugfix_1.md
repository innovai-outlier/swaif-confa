# Fix CI: currency parsing, totals scaling, zero‑division, BRL formatting, and non‑interactive pauses

**Goal:** Make `pytest` pass by correcting value parsing/scaling, handling zero‑division, using Brazilian BRL formatting consistently, and preventing `input()` from exploding inside CI.

## Summary of failing expectations (from tests)

- `calcular_totais_*` is over‑scaling by **×10** (e.g., `600.0` expected but `6000.0` calculated).
- GDS parsing should handle strings like `"1.500,75"` → `1500.75`.
- WAB values already numeric must **not** be rescaled (e.g., `15.50` should stay `15.50`, not `155.0`).
- `_comparar_fontes` should return `percentual_diferenca == 0.0` when one total is zero (test’s “division by zero” case).
- `ConciliacaoController.obter_detalhes_fonte` must compute a **positive** `total_principal` for `faturamento_c6` and `pagamento_c6` when CSVs contain values like `"R$ 100,50"`.
- `TerminalView` should print BRL with **dot as thousands** and **comma as decimals**, e.g., `5.500,75`; and must **not** call `input()` in captured/CI mode.

---

## Changes to apply

### 1) `src/models/analisador.py`

**a) Add a safe BRL parser.**  
Create a small utility that converts `"R$ 1.500,75"` or `"1.500,75"` to `1500.75`, and accepts numeric inputs unchanged.

```diff
+def _to_float_brl(value):
+    """
+    Convert BRL-formatted strings to float.
+    Accepts:
+      - 'R$ 1.500,75' -> 1500.75
+      - '1.500,75'    -> 1500.75
+      - 1500.75       -> 1500.75 (numeric passthrough)
+      - '' or None    -> 0.0
+    """
+    if value is None:
+        return 0.0
+    if isinstance(value, (int, float)):
+        return float(value)
+    s = str(value).strip()
+    if not s:
+        return 0.0
+    s = s.replace("R$", "").strip()
+    s = s.replace(".", "").replace(",", ".")
+    try:
+        return float(s)
+    except Exception:
+        return 0.0
```

**b) Fix GDS normalization.**  
Use `_to_float_brl` on GDS “valor”-columns without multiplying.

```diff
- df[col] = df[col].astype(float) * 10
+ df[col] = df[col].map(_to_float_brl)
```

**c) Fix WAB normalization.**  
WAB arrives numeric; do **not** rescale.

```diff
- df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) * 10
+ df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
```

**d) Totals must not be scaled and must use expected columns.**

```diff
- total = df['valor_venda'].sum() * 10
+ total = pd.to_numeric(df['valor_venda'], errors='coerce').fillna(0).sum()
```

**e) Division‑by‑zero safe comparison.**

```diff
- percentual = (diferenca / base * 100.0) if base > 0 else 100.0
+ if base <= 0 or total1 == 0.0 or total2 == 0.0:
+     percentual = 0.0
+ else:
+     percentual = (diferenca / base) * 100.0
```

---

### 2) `src/models/data_loader.py`

Normalize monetary columns when loading C6 CSVs.

```diff
+ from .analisador import _to_float_brl
+ df['valor_venda'] = df['valor_venda'].map(_to_float_brl)
+ df['valor_recebivel'] = df['valor_recebivel'].map(_to_float_brl)
+ df['descontos'] = df['descontos'].map(_to_float_brl)
```

---

### 3) `src/views/terminal_view.py`

**a) Add a BRL formatter without relying on system locale.**

```diff
+def format_brl(value: float) -> str:
+    try:
+        x = float(value)
+    except Exception:
+        x = 0.0
+    s = f"{x:,.2f}"
+    s = s.replace(",", "_").replace(".", ",").replace("_", ".")
+    return s
```

**b) Use `format_brl` everywhere totals are printed.**

```diff
- print(f"   VALOR FATURADO: R$ {total:>20,.2f}")
+ print(f"   VALOR FATURADO: R$ {format_brl(total):>20}")
```

**c) Make `input()` safe under pytest/CI.**

```diff
+import sys
+def safe_pause(prompt: str = "\nPressione ENTER para continuar..."):
+    try:
+        if sys.stdin is None or not sys.stdin.isatty():
+            return
+        input(prompt)
+    except (EOFError, OSError):
+        return
- input("\nPressione ENTER para continuar...")
+ safe_pause("\nPressione ENTER para continuar...")
```

---

## Commit message

```
fix: correct BRL parsing/scaling, zero-division handling, terminal BRL formatting, and CI-safe pauses
```

---

## Sanity checklist

- GDS and WAB normalization fixed
- Totals no longer ×10
- Division by zero returns 0.0%
- CSVs parse BRL correctly
- Terminal prints `5.500,75`
- No CI crash on `input()`
