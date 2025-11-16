#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traducir un bloque específico del diccionario de diálogos
"""

import json
import sys
from collections import OrderedDict

def translate_block(input_file, output_file, start_idx, end_idx, block_num):
    """
    Traduce un bloque específico de entradas

    Args:
        input_file: Archivo JSON de entrada
        output_file: Archivo JSON de salida
        start_idx: Índice de inicio (0-based)
        end_idx: Índice de fin (exclusivo)
        block_num: Número de bloque para el título
    """
    # Cargar el archivo
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    # Obtener las entradas como lista
    entries = list(data.items())
    total = len(entries)

    print(f"\n{'='*60}")
    print(f"Translated part{block_num}")
    print(f"{'='*60}")
    print(f"Traduciendo entradas {start_idx+1} a {min(end_idx, total)} de {total}")
    print(f"{'='*60}\n")

    # Procesar el bloque
    translated_count = 0
    for i in range(start_idx, min(end_idx, total)):
        english_text = entries[i][0]

        # Aquí irá la traducción manual
        # Por ahora, marco las que necesitan traducción
        if entries[i][1] == "":  # Si no está traducido
            # Aquí se hará la traducción manual
            spanish_text = ""  # Placeholder
            entries[i] = (english_text, spanish_text)
            translated_count += 1

    # Reconstruir el diccionario
    result = OrderedDict(entries)

    # Guardar el archivo actualizado
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Bloque {block_num} procesado")
    print(f"  Entradas procesadas: {min(end_idx, total) - start_idx}")
    print(f"  Archivo guardado: {output_file}")

    # Mostrar algunas entradas del bloque para verificar
    print(f"\nPrimeras 5 entradas del bloque:")
    for i in range(start_idx, min(start_idx + 5, end_idx, total)):
        en_text = entries[i][0][:60] + "..." if len(entries[i][0]) > 60 else entries[i][0]
        print(f"  {i+1}. {en_text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 translate_block.py <block_number>")
        print("Ejemplo: python3 translate_block.py 1")
        sys.exit(1)

    block_num = int(sys.argv[1])
    start_idx = (block_num - 1) * 500
    end_idx = block_num * 500

    translate_block(
        'dialogues_translation.json',
        'dialogues_translation.json',
        start_idx,
        end_idx,
        block_num
    )
