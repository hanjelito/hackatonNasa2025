from __future__ import annotations
from pathlib import Path
from string import Template
from typing import Dict, Optional, Any
import threading


class PromptLoader:
    """Cargador de prompts en formato Markdown con soporte de variables.

    - Busca archivos .md dentro de un directorio (por defecto: app/prompts).
    - Hace cache del contenido crudo para evitar lecturas repetidas de disco.
    - Permite renderizar variables usando la sintaxis ${nombre} (string.Template).
    - Si una variable no existe en el diccionario, se deja tal cual (safe_substitute).
    """

    def __init__(self, prompts_dir: Optional[Path | str] = None, encoding: str = "utf-8") -> None:
        # Determina la carpeta de prompts por defecto: <raiz>/app/prompts
        if prompts_dir is None:
            app_root = Path(__file__).resolve().parents[1]  # .../app
            prompts_dir = app_root / "prompts"
        self.prompts_dir = Path(prompts_dir)
        self.encoding = encoding

        self._cache: Dict[str, str] = {}
        self._lock = threading.RLock()

    def _file_path(self, name: str) -> Path:
        """Resuelve la ruta del archivo .md a partir del nombre (admite subcarpetas)."""
        path = self.prompts_dir / name
        # Si no trae extensión, asumimos .md
        if path.suffix.lower() != ".md":
            path = path.with_suffix(".md")
        return path

    def load_raw(self, name: str) -> str:
        """Carga el contenido crudo del prompt desde disco (o cache si existe)."""
        with self._lock:
            if name in self._cache:
                return self._cache[name]

        path = self._file_path(name)
        if not path.exists():
            raise FileNotFoundError(f"Prompt '{name}' no encontrado en {self.prompts_dir}")

        text = path.read_text(encoding=self.encoding)
        with self._lock:
            self._cache[name] = text
        return text

    def render(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Renderiza el prompt con variables opcionales usando ${var}.

        - Usa Template.safe_substitute para reemplazo tolerante: si falta una variable,
          se deja el marcador ${var} sin fallar.
        """
        raw = self.load_raw(name)
        if not variables:
            return raw
        try:
            return Template(raw).safe_substitute(variables)
        except Exception as e:
            raise ValueError(f"Error al renderizar prompt '{name}': {e}") from e