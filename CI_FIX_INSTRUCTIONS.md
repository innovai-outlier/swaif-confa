# CI Job Failure: Fix Instructions

## Context

- **Repository:** `innovai-outlier/swaif-confa`
- **CI Job:** [GitHub Actions Run](https://github.com/innovai-outlier/swaif-confa/actions/runs/16969435665/job/48102108970?pr=2)
- **Reference:** `48c4be745b89f423df9bc6ef22673dfc6999c92b`

---

## Summary of Failures

The following issues were identified in the CI job logs ([full log ref: 48c4be745b89f423df9bc6ef22673dfc6999c92b](48c4be745b89f423df9bc6ef22673dfc6999c92b)):

1. `ResultadoAnalise.__init__() got an unexpected keyword argument 'percentual_diferenca'`
2. `AttributeError: 'ResultadoAnalise' object has no attribute 'percentual_diferenca'`
3. `KeyError: 'faturamento_c6'` and `KeyError: 'pagamento_c6'`
4. `AttributeError: 'DataLoader' object has no attribute '_mapear_colunas'`
5. Assertion errors (value mismatches, e.g., "julho" != "072025")
6. `ZeroDivisionError: division by zero`
7. CSV column errors (e.g., `'coluna1' not found in Index(['coluna1,coluna2,valor'], dtype='object')`)

---

## Action Items

### 1. Update `ResultadoAnalise` Class

- Add a `percentual_diferenca` argument to the `__init__` method and set it as an attribute.
```python
class ResultadoAnalise:
    def __init__(self, ..., percentual_diferenca=None):
        self.percentual_diferenca = percentual_diferenca
        # existing initializations
```
- Alternatively, if this argument is not needed, remove its usage from all instantiations.

### 2. Prevent `KeyError` for Data Dictionaries

- Use `.get()` when accessing optional keys like `'faturamento_c6'` or `'pagamento_c6'`, or handle missing keys:
```python
valor = dados.get('faturamento_c6', 0)  # or appropriate default
```

### 3. Implement `_mapear_colunas` in `DataLoader`

- Ensure `DataLoader` has the `_mapear_colunas` method or update references to the correct method name.

### 4. Fix Format/Value Assertion Errors

- Ensure the logic for month formatting returns the expected values (`'072025'` instead of `'julho'`) or update test expectations for the actual output.

### 5. Handle Division by Zero

- Check divisors before dividing:
```python
if divisor == 0:
    percentual_diferenca = 0  # or handle appropriately
else:
    percentual_diferenca = valor / divisor
```

### 6. CSV Column Parsing

- Ensure correct CSV parsing so columns are properly recognized:
```python
df = pd.read_csv(filename, sep=",")
```

---

## References

- [CI Job Log](48c4be745b89f423df9bc6ef22673dfc6999c92b) (ref)
- [GitHub Actions Run](https://github.com/innovai-outlier/swaif-confa/actions/runs/16969435665/job/48102108970?pr=2)

---

## Instructions for Coding Agent

1. Review the failures listed above.
2. Make the recommended code changes.
3. Ensure all tests pass locally before pushing commits.
4. Reference the CI logs and this instruction file to verify fixes.

---

**End of Instructions**