"""
🚀 DEMO SIMPLE - Extractor de Artículos Científicos
===================================================

Demostración super simple del extractor. 
Solo ejecuta este archivo para ver cómo funciona.
"""

from extractor_articulo import ExtractorArticulo
import os


def demo_simple():
    """
    Demo simple que funciona siempre (con archivo local de respaldo)
    """
    
    extractor = ExtractorArticulo()
    
    # Opción 1: Intentar desde URL
    url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4379453/"
    print(f"🌐 Intentando desde URL: {url}")
    
    resultado = None
    try:
        resultado = extractor.extraer_articulo_completo(url, es_archivo=False)
    except:
        print("⚠️  Sin conexión a internet")
    

    # Mostrar resultados
    if resultado:
        # Guardar
        extractor.guardar_texto_extraido(resultado)
        
        return resultado
    
    else:
        print("❌ No se pudo extraer desde URL")

    return None


if __name__ == "__main__":

    resultado = demo_simple()
    
    print(f"\n✨ Demo completada. ¡Listo para el hackathon! 🏆")