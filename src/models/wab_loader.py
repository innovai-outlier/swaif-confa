import json
import logging
import os
from typing import Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

WAB_COLS: Dict[str, str] = {
    'DATA': 'data',
    'VALOR PAGO': 'valor_pago',
    'VALOR TOTAL': 'valor_total',
    'DESCRIÇÃO': 'descricao',
    'MODO DE PAGAMTO': 'forma_pagamento',
    'NOME DO PACIENTE (FORNECEDOR)': 'paciente',
    'OBS': 'obs',
}

def ler_wab_txt(file_path: str) -> pd.DataFrame:
    """Lê arquivo WAB em formato TXT."""
    try:
        registros: List[Dict[str, str]] = []
        with open(file_path, encoding='utf-8') as f:
            bloco: Dict[str, str] = {}
            for linha in f:
                linha = linha.strip()
                if not linha:
                    if bloco:
                        registros.append(bloco)
                        bloco = {}
                    continue
                if ':' in linha:
                    chave, valor = linha.split(':', 1)
                    bloco[chave.strip()] = valor.strip()
            if bloco:
                registros.append(bloco)
        df = pd.DataFrame(registros).rename(columns=WAB_COLS)
        logger.info(
            "Arquivo WAB TXT lido com sucesso: %s - %d registros",
            os.path.basename(file_path),
            len(df),
        )
        return df
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erro ao ler WAB TXT %s: %s", file_path, exc)
        return pd.DataFrame()

def ler_wab_json(file_path: str) -> pd.DataFrame:
    """Lê arquivo WAB em formato JSON."""
    try:
        with open(file_path, encoding='utf-8') as f:
            dados = json.load(f)
        df = pd.DataFrame(dados).rename(columns=WAB_COLS)
        logger.info(
            "Arquivo WAB JSON lido com sucesso: %s - %d registros",
            os.path.basename(file_path),
            len(df),
        )
        return df
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erro ao ler WAB JSON %s: %s", file_path, exc)
        return pd.DataFrame()

def converter_wab_txt_para_json(txt_path: str, json_path: Optional[str] = None) -> Optional[str]:
    """Converte arquivo WAB TXT para JSON."""
    try:
        if json_path is None:
            json_path = txt_path.replace('.txt', '.json')
        registros: List[Dict[str, str]] = []
        with open(txt_path, encoding='utf-8') as f:
            bloco: Dict[str, str] = {}
            for linha in f:
                linha = linha.strip()
                if not linha:
                    if bloco:
                        registros.append(bloco)
                        bloco = {}
                    continue
                if ':' in linha:
                    chave, valor = linha.split(':', 1)
                    bloco[chave.strip()] = valor.strip()
            if bloco:
                registros.append(bloco)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)
        logger.info(
            "Arquivo WAB convertido: %s -> %s (%d registros)",
            os.path.basename(txt_path),
            os.path.basename(json_path),
            len(registros),
        )
        return json_path
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Erro ao converter WAB TXT %s para JSON: %s", txt_path, exc)
        return None
