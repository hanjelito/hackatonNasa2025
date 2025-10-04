"""
Extractor de texto de artículos científicos desde HTML
Extrae el contenido principal de artículos de PMC (PubMed Central) y otros sitios académicos
"""

import re
from bs4 import BeautifulSoup
import requests
from pathlib import Path


class ExtractorArticulo:
    """
    Clase para extraer texto de artículos científicos desde archivos HTML
    """
    
    def __init__(self):
        self.selectores_contenido = [
            # Selectores específicos para PMC
            'section.body.main-article-body',
            'section[aria-label="Article content"]',
            '.article-body',
            '.main-content',
            
            # Selectores generales
            'main',
            'article',
            '.content',
            '#content',
            '.post-content',
            '.entry-content'
        ]
        
        self.selectores_titulo = [
            'h1.article-title',
            'h1.title',
            '.article-title',
            'h1',
            '.title'
        ]
        
        self.selectores_abstract = [
            'section.abstract',
            '.abstract',
            '#abstract',
            '[id*="abstract"]'
        ]
        
        # Elementos a excluir del contenido
        self.elementos_excluir = [
            'script', 'style', 'nav', 'header', 'footer',
            '.navigation', '.nav', '.sidebar', '.menu',
            '.comments', '.related', '.share', '.social',
            '.advertisement', '.ads', '.banner'
        ]

    def cargar_html_desde_archivo(self, ruta_archivo):
        """
        Carga contenido HTML desde un archivo local
        """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except Exception as e:
            print(f"Error al leer archivo {ruta_archivo}: {e}")
            return None

    def cargar_html_desde_url(self, url):
        """
        Carga contenido HTML desde una URL
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error al cargar URL {url}: {e}")
            return None

    def limpiar_texto(self, texto):
        """
        Limpia y normaliza el texto extraído
        """
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

    def extraer_titulo(self, soup):
        """
        Extrae el título del artículo
        """
        for selector in self.selectores_titulo:
            elemento = soup.select_one(selector)
            if elemento:
                titulo = self.limpiar_texto(elemento.get_text())
                if titulo and len(titulo) > 10:  # Filtrar títulos muy cortos
                    return titulo
        
        # Fallback al title del documento
        title_tag = soup.find('title')
        if title_tag:
            titulo = self.limpiar_texto(title_tag.get_text())
            # Remover sufijos comunes
            titulo = re.sub(r'\s*-\s*(PMC|PubMed|NCBI).*$', '', titulo)
            return titulo
        
        return "Título no encontrado"

    def extraer_abstract(self, soup):
        """
        Extrae el abstract/resumen del artículo
        """
        for selector in self.selectores_abstract:
            elemento = soup.select_one(selector)
            if elemento:
                # Remover el título "Abstract" si existe
                texto = elemento.get_text()
                texto = re.sub(r'^abstract\s*', '', texto, flags=re.IGNORECASE)
                return self.limpiar_texto(texto)
        return ""

    def extraer_contenido_principal(self, soup):
        """
        Extrae el contenido principal del artículo
        """
        # Remover elementos no deseados
        for selector in self.elementos_excluir:
            for elemento in soup.select(selector):
                elemento.decompose()
        
        contenido_completo = ""
        
        # Buscar contenido usando los selectores
        for selector in self.selectores_contenido:
            contenedor = soup.select_one(selector)
            if contenedor:
                # Extraer texto de secciones específicas
                secciones = contenedor.find_all(['section', 'div'], 
                                               class_=lambda x: x and ('section' in x or 'content' in x))
                
                if secciones:
                    for seccion in secciones:
                        texto_seccion = self.extraer_texto_seccion(seccion)
                        if texto_seccion:
                            contenido_completo += texto_seccion + "\n\n"
                else:
                    # Si no hay secciones específicas, extraer todo el texto
                    contenido_completo = self.limpiar_texto(contenedor.get_text())
                
                break
        
        # Si no se encontró contenido específico, buscar en todo el body
        if not contenido_completo.strip():
            body = soup.find('body')
            if body:
                contenido_completo = self.limpiar_texto(body.get_text())
        
        return contenido_completo

    def extraer_texto_seccion(self, seccion):
        """
        Extrae texto de una sección específica del artículo
        """
        texto = ""
        
        # Buscar título de la sección
        titulo_seccion = seccion.find(['h1', 'h2', 'h3', 'h4'])
        if titulo_seccion:
            texto += f"## {self.limpiar_texto(titulo_seccion.get_text())}\n\n"
        
        # Extraer párrafos
        paragrafos = seccion.find_all('p')
        for p in paragrafos:
            texto_p = self.limpiar_texto(p.get_text())
            if texto_p and len(texto_p) > 20:  # Filtrar párrafos muy cortos
                texto += texto_p + "\n\n"
        
        return texto

    def extraer_metadatos(self, soup):
        """
        Extrae metadatos del artículo
        """
        metadatos = {}
        
        # Buscar metadatos en meta tags
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name', '')
            content = meta.get('content', '')
            
            if 'citation_author' in name:
                if 'autores' not in metadatos:
                    metadatos['autores'] = []
                metadatos['autores'].append(content)
            elif 'citation_journal_title' in name:
                metadatos['revista'] = content
            elif 'citation_publication_date' in name:
                metadatos['fecha_publicacion'] = content
            elif 'citation_doi' in name:
                metadatos['doi'] = content
            elif 'citation_pmid' in name:
                metadatos['pmid'] = content
        
        return metadatos

    def extraer_articulo_completo(self, fuente, es_archivo=True):
        """
        Extrae todo el contenido del artículo (título, abstract, contenido, metadatos)
        
        Args:
            fuente: Ruta del archivo HTML o URL
            es_archivo: True si es archivo local, False si es URL
        
        Returns:
            dict: Diccionario con toda la información extraída
        """
        # Cargar HTML
        if es_archivo:
            html_content = self.cargar_html_desde_archivo(fuente)
        else:
            html_content = self.cargar_html_desde_url(fuente)
        
        if not html_content:
            return None
        
        # Parsear HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extraer componentes
        resultado = {
            'titulo': self.extraer_titulo(soup),
            'abstract': self.extraer_abstract(soup),
            'contenido': self.extraer_contenido_principal(soup),
            'metadatos': self.extraer_metadatos(soup),
            'fuente': fuente
        }
        
        return resultado

    def guardar_texto_extraido(self, resultado):
        """
        Guarda el texto extraído en un archivo, creando el directorio si no existe.
        """
        try:
            # Crear ruta relativa al archivo actual
            script_dir = Path(__file__).parent
            assets_dir = script_dir / "assets"
            
            # Modificar el nombre del archivo de salida para incluir el DOI
            doi = resultado['metadatos'].get('doi', 'articulo_sin_doi').replace('/', '_')
            archivo_salida = assets_dir / f"{doi}.txt"
            
            # Crear el directorio si no existe
            Path(archivo_salida).parent.mkdir(parents=True, exist_ok=True)
            
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write(f"## Titulo\n\n")
                f.write(f"{resultado['titulo']}\n\n")
                
                if resultado['abstract']:
                    f.write("## Abstract\n\n")
                    f.write(f"{resultado['abstract']}\n\n")
                
                if resultado['metadatos']:
                    f.write("## Metadatos\n\n")
                    for clave, valor in resultado['metadatos'].items():
                        if isinstance(valor, list):
                            valor = ', '.join(valor)
                        f.write(f"**{clave.title()}:** {valor}\n\n")
                
                f.write("## Contenido\n\n")
                f.write(resultado['contenido'])
                
            print(f"Texto extraído guardado en: {archivo_salida}")
            return True
            
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False


def main():
    """
    Función principal para probar el extractor
    """
    extractor = ExtractorArticulo()
    
    # Archivo de ejemplo en el proyecto
    archivo_html = r"c:\Users\David\buscar_curro\hackathon\hackatonNasa2025\PMC4379453_fuente.html"
    
    print("Extrayendo contenido del artículo...")
    resultado = extractor.extraer_articulo_completo(archivo_html, es_archivo=True)
    
    if resultado:
        print(f"\n--- TÍTULO ---")
        print(resultado['titulo'])
        
        print(f"\n--- ABSTRACT (primeros 300 chars) ---")
        print(resultado['abstract'][:300] + "..." if len(resultado['abstract']) > 300 else resultado['abstract'])
        
        print(f"\n--- METADATOS ---")
        for clave, valor in resultado['metadatos'].items():
            if isinstance(valor, list):
                valor = ', '.join(valor[:3]) + ('...' if len(valor) > 3 else '')
            print(f"{clave}: {valor}")
        
        print(f"\n--- CONTENIDO (primeros 500 chars) ---")
        print(resultado['contenido'][:500] + "..." if len(resultado['contenido']) > 500 else resultado['contenido'])
        
        # Guardar resultado completo
        extractor.guardar_texto_extraido(resultado)
        
        print(f"\n✅ Extracción completada. Total de caracteres: {len(resultado['contenido'])}")
    else:
        print("❌ Error al extraer el contenido del artículo")


if __name__ == "__main__":
    main()