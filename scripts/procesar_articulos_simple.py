#!/usr/bin/env python3
"""
Script simple para procesar algunos artículos del CSV de muestra
Extrae contenido usando requests y BeautifulSoup directamente
"""

import csv
import requests
import re
import time
from pathlib import Path
from bs4 import BeautifulSoup
import json
from datetime import datetime


def limpiar_texto(texto):
    """Limpia y normaliza el texto extraído"""
    if not texto:
        return ""
    
    # Eliminar espacios extra y normalizar
    texto = re.sub(r'\s+', ' ', texto.strip())
    
    # Eliminar caracteres de control
    texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto)
    
    # Normalizar comillas y guiones
    texto = texto.replace('"', '"').replace('"', '"')
    texto = texto.replace(''', "'").replace(''', "'")
    texto = texto.replace('–', '-').replace('—', '-')
    
    return texto


def extraer_contenido_pmc(url):
    """
    Extrae contenido de un artículo de PMC
    """
    try:
        # Headers para simular un navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Hacer request
        print(f"🌐 Descargando: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer título
        titulo = "Sin título"
        for selector in ['h1.article-title', 'h1.title', '.article-title', 'h1']:
            elemento = soup.select_one(selector)
            if elemento:
                titulo = limpiar_texto(elemento.get_text())
                if titulo and len(titulo) > 10:
                    break
        
        # Extraer abstract
        abstract = ""
        for selector in ['section.abstract', '.abstract', '#abstract']:
            elemento = soup.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                texto = re.sub(r'^abstract\s*', '', texto, flags=re.IGNORECASE)
                abstract = limpiar_texto(texto)
                break
        
        # Extraer contenido principal
        contenido = ""
        
        # Selectores específicos para PMC
        selectores_contenido = [
            'section.body.main-article-body',
            'section[aria-label="Article content"]',
            '.article-body',
            '.main-content',
            'main',
            'article'
        ]
        
        for selector in selectores_contenido:
            contenedor = soup.select_one(selector)
            if contenedor:
                # Remover elementos no deseados
                for elemento_basura in contenedor.select('script, style, nav, header, footer'):
                    elemento_basura.decompose()
                
                contenido = limpiar_texto(contenedor.get_text())
                if contenido and len(contenido) > 100:
                    break
        
        # Si no se encuentra contenido específico, usar todo el body
        if not contenido:
            body = soup.find('body')
            if body:
                contenido = limpiar_texto(body.get_text())
        
        # Extraer algunos metadatos básicos
        metadatos = {}
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name', '')
            content = meta.get('content', '')
            
            if 'citation_journal_title' in name:
                metadatos['revista'] = content
            elif 'citation_publication_date' in name:
                metadatos['fecha_publicacion'] = content
            elif 'citation_doi' in name:
                metadatos['doi'] = content
            elif 'citation_pmid' in name:
                metadatos['pmid'] = content
        
        return {
            'titulo': titulo,
            'abstract': abstract,
            'contenido': contenido,
            'metadatos': metadatos,
            'url': url,
            'estado': 'exitoso'
        }
        
    except Exception as e:
        return {
            'titulo': 'Error al extraer',
            'abstract': '',
            'contenido': '',
            'metadatos': {},
            'url': url,
            'estado': 'error',
            'error': str(e)
        }


def generar_nombre_archivo(titulo, url):
    """Genera un nombre de archivo válido"""
    # Extraer PMC ID
    pmc_id = ""
    if "PMC" in url:
        match = re.search(r'PMC(\d+)', url)
        if match:
            pmc_id = f"PMC{match.group(1)}_"
    
    # Limpiar título
    titulo_limpio = titulo[:50]
    titulo_limpio = "".join(c for c in titulo_limpio if c.isalnum() or c in (' ', '-', '_')).strip()
    titulo_limpio = titulo_limpio.replace(' ', '_')
    
    return f"{pmc_id}{titulo_limpio}.txt"


def guardar_articulo(resultado, directorio_salida):
    """Guarda el artículo extraído en un archivo"""
    nombre_archivo = generar_nombre_archivo(resultado['titulo'], resultado['url'])
    ruta_archivo = directorio_salida / nombre_archivo
    
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(f"# {resultado['titulo']}\n\n")
            f.write(f"**URL Original:** {resultado['url']}\n")
            f.write(f"**Estado:** {resultado['estado']}\n\n")
            
            if resultado.get('error'):
                f.write(f"**Error:** {resultado['error']}\n\n")
            
            # Abstract
            if resultado['abstract']:
                f.write("## Abstract\n\n")
                f.write(f"{resultado['abstract']}\n\n")
            
            # Metadatos
            if resultado['metadatos']:
                f.write("## Metadatos\n\n")
                for key, value in resultado['metadatos'].items():
                    f.write(f"**{key.title()}:** {value}\n")
                f.write("\n")
            
            # Contenido principal
            f.write("## Contenido\n\n")
            f.write(resultado['contenido'] if resultado['contenido'] else 'No se pudo extraer contenido')
        
        print(f"✅ Guardado: {nombre_archivo}")
        return str(ruta_archivo)
        
    except Exception as e:
        print(f"❌ Error al guardar {nombre_archivo}: {e}")
        return None


def main():
    """Función principal"""
    # Configurar rutas
    script_dir = Path(__file__).parent
    csv_path = script_dir.parent / "docs" / "data" / "SB_publication_PMC.csv"
    output_dir = script_dir.parent / "docs" / "extracted_articles"
    
    # Crear directorio de salida
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Verificar que existe el CSV
    if not csv_path.exists():
        print(f"❌ No se encontró el archivo CSV en: {csv_path}")
        return
    
    print("🔬 Procesador Simple de Artículos PMC")
    print("=" * 40)
    
    # Leer CSV
    articulos = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                articulos.append({
                    'titulo': fila.get('Title', '').strip(),
                    'url': fila.get('Link', '').strip()
                })
        print(f"📄 Se encontraron {len(articulos)} artículos en el CSV")
    except Exception as e:
        print(f"❌ Error al leer CSV: {e}")
        return
    
    # Preguntar cuántos procesar
    try:
        cantidad_str = input(f"\n¿Cuántos artículos procesar? (máximo {len(articulos)}, default 5): ").strip()
        cantidad = int(cantidad_str) if cantidad_str else 5
        cantidad = min(cantidad, len(articulos))
    except ValueError:
        cantidad = 5
    
    print(f"\n🚀 Procesando {cantidad} artículos...")
    print(f"📁 Guardando en: {output_dir}")
    
    # Procesar artículos
    resultados = []
    exitosos = 0
    errores = 0
    
    for i, articulo in enumerate(articulos[:cantidad], 1):
        print(f"\n--- Artículo {i}/{cantidad} ---")
        print(f"📰 {articulo['titulo'][:60]}...")
        
        # Extraer contenido
        resultado = extraer_contenido_pmc(articulo['url'])
        
        # Guardar resultado
        archivo_guardado = guardar_articulo(resultado, output_dir)
        
        if resultado['estado'] == 'exitoso' and archivo_guardado:
            exitosos += 1
        else:
            errores += 1
            print(f"❌ Error: {resultado.get('error', 'Error desconocido')}")
        
        resultados.append(resultado)
        
        # Pausa entre requests
        if i < cantidad:
            print("⏳ Esperando 2 segundos...")
            time.sleep(2)
    
    # Guardar log de resultados
    log_path = output_dir / "procesamiento_log.json"
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'total_procesados': cantidad,
        'exitosos': exitosos,
        'errores': errores,
        'resultados': resultados
    }
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    # Resumen final
    print(f"\n📊 RESUMEN FINAL")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Errores: {errores}")
    print(f"📁 Archivos en: {output_dir}")
    print(f"📋 Log en: {log_path}")


if __name__ == "__main__":
    main()