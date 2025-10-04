"""
DEMO LLM EXTRACTION - Bucle simple
=====================================

Bucle simple para iterar archivos y probar llm_extraction
"""

import asyncio
import json
import sys
from pathlib import Path

# Agregar el directorio backend al path para poder importar el paquete 'app'
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.utils.insight_extraction import process_article


async def main():
    """
    Bucle simple para procesar archivos
    """
    # Encontrar la raíz del proyecto navegando hacia arriba hasta encontrar el docker-compose.yml
    current_dir = Path.cwd()
    project_root = current_dir
    
    # Si estamos en backend/, subir un nivel
    if current_dir.name == "backend":
        project_root = current_dir.parent
    
    articles_dir = Path("C:/Users/David/buscar_curro/hackathon/hackatonNasa2025/docs/extracted_articles")
    output_dir = Path("C:/Users/David/buscar_curro/hackathon/hackatonNasa2025/docs/insight_json_results")

    print(f"Buscando archivos en: {articles_dir}")
    
    if not articles_dir.exists():
        print(f"ERROR: Directorio no existe: {articles_dir}")
        return
    
    txt_files = list(articles_dir.glob("*.txt"))
    
    # Límite hardcodeado de 5 archivos
    
    print(f"Encontrados {len(txt_files)} archivos (límite: 5)")

    # Crear el directorio de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, file_path in enumerate(reversed(txt_files), 1):
        output_file = output_dir / f"{file_path.stem}.json"
        
        # Verificar si el archivo ya existe en la carpeta de destino
        if output_file.exists():
            print(f"Archivo ya procesado: {file_path.name}. Omitiendo.")
            continue
        
        print(f"\n--- Procesando {i}/{len(txt_files)}: {file_path.name} ---")
        
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # Procesar con LLM
        try:
            result = await process_article(text_content)
        except Exception as e:
            print(f"ERROR al procesar {file_path.name}: {e}")
            continue
        
        print(f"OK: Resultado obtenido")
        
        # Guardar con formato JSON correcto
        
        
        # Asegurar formato JSON correcto
        with open(output_file, 'w', encoding='utf-8') as f:
            if isinstance(result, str):
                # Si result es una cadena, intentar parsearla como JSON
                try:
                    result_dict = json.loads(result)
                    json.dump(result_dict, f, indent=4, ensure_ascii=False)
                except json.JSONDecodeError:
                    # Si no es JSON válido, guardar como está
                    f.write(result)
            else:
                # Si result es un dict/objeto, guardarlo directamente
                json.dump(result, f, indent=4, ensure_ascii=False)
        
        print(f"GUARDADO en: {output_file}")
        



if __name__ == "__main__":
    asyncio.run(main())
