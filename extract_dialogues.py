#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer todos los diálogos únicos de Troops.json
y crear un diccionario de traducción en formato JSON
"""

import json
import sys
from collections import OrderedDict

def extract_dialogues(data, dialogue_codes=None):
    """
    Extrae todos los textos de diálogo del archivo Troops.json

    Args:
        data: Datos cargados del JSON
        dialogue_codes: Lista de códigos que identifican diálogos en RPG Maker

    Returns:
        Set de diálogos únicos
    """
    if dialogue_codes is None:
        # Códigos comunes para texto en RPG Maker MV/MZ
        # 101: Show Text (primer línea)
        # 401: Show Text (líneas adicionales)
        # 102: Show Choices
        # 402: When [Choice]
        # 405: Show Scrolling Text
        dialogue_codes = [101, 401, 102, 402, 405]

    dialogues = set()

    def traverse(obj, depth=0):
        """Recorre recursivamente el JSON buscando diálogos"""
        if depth > 30:  # Límite de profundidad para evitar recursión infinita
            return

        if isinstance(obj, dict):
            # Si tiene 'code' y 'parameters', podría ser un comando de evento
            if 'code' in obj and 'parameters' in obj:
                code = obj['code']
                params = obj['parameters']

                # Verificar si es un código de diálogo
                if code in dialogue_codes and isinstance(params, list):
                    for param in params:
                        # Solo agregar strings que no sean código JavaScript
                        if isinstance(param, str) and len(param.strip()) > 0:
                            # Excluir código JavaScript y variables
                            if not param.startswith('$') and not param.startswith('!$'):
                                # Limpiar espacios
                                clean_text = param.strip()
                                if clean_text:
                                    dialogues.add(clean_text)

            # Continuar la búsqueda recursiva
            for value in obj.values():
                traverse(value, depth + 1)

        elif isinstance(obj, list):
            for item in obj:
                traverse(item, depth + 1)

    # Iniciar la búsqueda
    traverse(data)

    return dialogues

def create_translation_dict(dialogues):
    """
    Crea un diccionario ordenado alfabéticamente para traducción

    Args:
        dialogues: Set de textos únicos

    Returns:
        OrderedDict con formato "texto original": ""
    """
    # Ordenar alfabéticamente
    sorted_dialogues = sorted(dialogues)

    # Crear diccionario ordenado
    translation_dict = OrderedDict()
    for dialogue in sorted_dialogues:
        translation_dict[dialogue] = ""

    return translation_dict

def main():
    print("Extrayendo diálogos de Troops.json...")

    # Cargar el archivo JSON
    try:
        with open('Troops.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ Archivo cargado correctamente")
    except FileNotFoundError:
        print("✗ Error: No se encontró el archivo Troops.json")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error al parsear el JSON: {e}")
        sys.exit(1)

    # Extraer diálogos
    print("Extrayendo textos únicos...")
    dialogues = extract_dialogues(data)
    print(f"✓ Se encontraron {len(dialogues)} diálogos únicos")

    # Crear diccionario de traducción
    print("Creando diccionario de traducción...")
    translation_dict = create_translation_dict(dialogues)

    # Guardar en archivo JSON
    output_file = 'dialogues_translation.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translation_dict, f, ensure_ascii=False, indent=2)

    print(f"✓ Archivo '{output_file}' creado exitosamente")
    print(f"  Total de entradas: {len(translation_dict)}")

    # Mostrar algunos ejemplos
    print("\nPrimeros 10 diálogos:")
    for i, dialogue in enumerate(list(translation_dict.keys())[:10], 1):
        preview = dialogue[:80] + "..." if len(dialogue) > 80 else dialogue
        print(f"  {i}. \"{preview}\"")

    print("\nÚltimos 5 diálogos:")
    for i, dialogue in enumerate(list(translation_dict.keys())[-5:], 1):
        preview = dialogue[:80] + "..." if len(dialogue) > 80 else dialogue
        print(f"  {i}. \"{preview}\"")

if __name__ == "__main__":
    main()
