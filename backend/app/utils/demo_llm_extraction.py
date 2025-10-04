"""
🚀 DEMO LLM EXTRACTION - Bucle simple
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

from app.utils.llm_extraction import process_article


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
    
    articles_dir = project_root / "docs" / "extracted_articles"
    
    print(f"Buscando archivos en: {articles_dir}")
    
    if not articles_dir.exists():
        print(f"❌ Directorio no existe: {articles_dir}")
        return
    
    txt_files = list(articles_dir.glob("*.txt"))
    
    # Límite hardcodeado de 5 archivos
    txt_files = txt_files[:5]
    
    print(f"Encontrados {len(txt_files)} archivos (límite: 5)")
    
    for i, file_path in enumerate(txt_files, 1):
        print(f"\n--- Procesando {i}/{len(txt_files)}: {file_path.name} ---")
        
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # Procesar con LLM
        result = await process_article(text_content)
        
        print(f"✅ Resultado: {result}")
        
        # Guardar directamente en txt
        output_file = project_root / f"resultado_{file_path.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result))
        
        print(f"💾 Guardado en: {output_file}")
        



if __name__ == "__main__":
    asyncio.run(main())
