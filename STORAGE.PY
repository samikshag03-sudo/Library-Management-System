"""
Simple JSON file storage layer.

Each entity type (books, members, issue records) is stored in its own
JSON file under the `data/` directory. This keeps the persistence layer
dependency-free (no external database needed) while still being a real,
durable storage mechanism between program runs.
"""

import json
import os
import shutil
import tempfile

from .exceptions import StorageError


class JSONStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self._atomic_write([])

    def load(self) -> list:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as exc:
            raise StorageError(
                f"Data file '{self.filepath}' is corrupted and could not be read: {exc}"
            ) from exc
        except OSError as exc:
            raise StorageError(f"Could not read data file '{self.filepath}': {exc}") from exc

    def save(self, records: list):
        try:
            self._atomic_write(records)
        except OSError as exc:
            raise StorageError(f"Could not write data file '{self.filepath}': {exc}") from exc

    def _atomic_write(self, records: list):
        """Write via a temp file + rename so a crash mid-write never
        corrupts the existing data file."""
        directory = os.path.dirname(self.filepath) or "."
        os.makedirs(directory, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            shutil.move(tmp_path, self.filepath)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
