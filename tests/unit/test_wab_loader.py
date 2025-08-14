import json
import os

from src.models import wab_loader


def test_ler_wab_json(tmp_path):
    dados = [{'DATA': '01/07/2025', 'VALOR PAGO': 'R$10,00', 'VALOR TOTAL': 'R$10,00',
              'DESCRIÇÃO': 'Teste', 'MODO DE PAGAMTO': 'PIX',
              'NOME DO PACIENTE (FORNECEDOR)': 'Paciente', 'OBS': ''}]
    arquivo = tmp_path / 'teste.json'
    with arquivo.open('w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    df = wab_loader.ler_wab_json(str(arquivo))
    assert not df.empty
    assert 'valor_pago' in df.columns


def test_converter_wab_txt_para_json(tmp_path):
    txt = tmp_path / 'teste.txt'
    with txt.open('w', encoding='utf-8') as f:
        f.write('DATA: 01/07/2025\n')
        f.write('VALOR PAGO: R$10,00\n')
        f.write('VALOR TOTAL: R$10,00\n')
        f.write('DESCRIÇÃO: Teste\n')
        f.write('MODO DE PAGAMTO: PIX\n')
        f.write('NOME DO PACIENTE (FORNECEDOR): Paciente\n')
        f.write('OBS: \n')
        f.write('\n')
    json_path = wab_loader.converter_wab_txt_para_json(str(txt))
    assert json_path is not None
    assert os.path.exists(json_path)
    df = wab_loader.ler_wab_json(json_path)
    assert len(df) == 1
