"""
🚀 DEMO LLM EXTRACTION - Extracción y Estructuración con IA
===========================================================

Demo para mostrar cómo usar llm_extraction para extraer texto de artículos
y estructurar los datos usando LLM con un límite de 5 artículos.
"""

import asyncio
import json
from pathlib import Path
from .llm_extraction import process_article
from .extractor_articulo import ExtractorArticulo


# URLs de ejemplo para probar (máximo 5)
SAMPLE_URLS = [
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC4379453/",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC3572453/",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC2917851/",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC3419059/",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC2816917/"
]


async def demo_single_article(url: str, index: int):
    """
    Procesa un solo artículo y devuelve los datos estructurados
    
    Args:
        url: URL del artículo
        index: Índice del artículo (para mostrar progreso)
        
    Returns:
        dict: Datos estructurados del artículo
    """
    print(f"\n📄 Procesando artículo {index}/5...")
    print(f"🔗 URL: {url}")
    
    try:
        # 1. Extraer HTML desde URL
        extractor = ExtractorArticulo()
        html_content = extractor.cargar_html_desde_url(url)
        
        if not html_content:
            print(f"❌ Error: No se pudo cargar HTML desde {url}")
            return None
        
        print("✅ HTML cargado correctamente")
        
        # 2. Procesar con LLM
        print("🤖 Procesando con LLM...")
        structured_data = await process_article(html_content)
        
        print("✅ Datos estructurados obtenidos")
        print(f"📋 Título: {structured_data.get('title', 'N/A')[:80]}...")
        
        return structured_data
        
    except Exception as e:
        print(f"❌ Error procesando artículo {index}: {str(e)}")
        return None


async def demo_batch_processing(limit: int = 5) -> list:
    """
    Procesa múltiples artículos con límite especificado
    
    Args:
        limit: Número máximo de artículos a procesar
        
    Returns:
        list: Lista de datos estructurados de los artículos
    """
    print(f"🚀 Iniciando demo de LLM Extraction (límite: {limit} artículos)")
    print("=" * 60)
    
    results = []
    urls_to_process = SAMPLE_URLS[:limit]  # Aplicar límite
    
    for i, url in enumerate(urls_to_process, 1):
        result = await demo_single_article(url, i)
        if result:
            results.append(result)
        
        # Pausa pequeña entre artículos
        if i < len(urls_to_process):
            print("⏳ Pausa de 2 segundos...")
            await asyncio.sleep(2)
    
    return results


def save_demo_results(results: list):
    """
    Guarda los resultados del demo en un archivo JSON
    
    Args:
        results: Lista de resultados estructurados
    """
    if not results:
        print("⚠️  No hay resultados para guardar")
        return
    
    # Crear directorio de resultados
    results_dir = Path(__file__).parent / "demo_results"
    results_dir.mkdir(exist_ok=True)
    
    # Guardar resultados
    output_file = results_dir / "llm_extraction_demo.json"
    
    demo_data = {
        "timestamp": "2025-10-04",
        "total_processed": len(results),
        "articles": results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {output_file}")


def print_demo_summary(results: list):
    """
    Imprime un resumen de los resultados obtenidos
    
    Args:
        results: Lista de resultados del demo
    """
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DEMO")
    print("=" * 60)
    
    if not results:
        print("❌ No se procesaron artículos exitosamente")
        return
    
    print(f"✅ Artículos procesados exitosamente: {len(results)}")
    print(f"📈 Tasa de éxito: {len(results)}/5 ({len(results)*20}%)")
    
    print("\n📋 Títulos procesados:")
    for i, article in enumerate(results, 1):
        title = article.get('title', 'Sin título')
        print(f"  {i}. {title[:70]}{'...' if len(title) > 70 else ''}")
    
    # Estadísticas adicionales
    authors_found = sum(1 for article in results if article.get('authors'))
    abstracts_found = sum(1 for article in results if article.get('abstract'))
    dois_found = sum(1 for article in results if article.get('doi'))
    
    print("\n📊 Estadísticas de extracción:")
    print(f"  • Artículos con autores: {authors_found}/{len(results)}")
    print(f"  • Artículos con abstract: {abstracts_found}/{len(results)}")
    print(f"  • Artículos con DOI: {dois_found}/{len(results)}")


async def main():
    """
    Función principal del demo
    """
    try:
        # Procesar artículos (límite de 5)
        results = await demo_batch_processing(limit=5)
        
        # Guardar resultados
        save_demo_results(results)
        
        # Mostrar resumen
        print_demo_summary(results)
        
        print("\n🎉 Demo completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en el demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Ejecutar demo
    print("🚀 Iniciando Demo LLM Extraction...")
    asyncio.run(main())