"""Witryna na klonie, jednym procesem ze standardowej biblioteki.

    python3 -m witryna

Serwerem jest tu ``wsgiref``, a na dynie gunicorn (``Procfile``).
Aplikacja jest w obu ta sama funkcja, więc różnicę między klonem a dynem robi
liczba żądań naraz, a nie kod.
"""

from __future__ import annotations

import os
from wsgiref.simple_server import make_server

from witryna.serwer import aplikacja


def main() -> int:
    #  PORT nazywa platforma, więc nazwy tej nie wybieramy; na klonie nie ma go
    #  w środowisku i wtedy port jest przyzwyczajeniem, a nie ustawieniem.
    port = int(os.environ.get("PORT", 8000))
    #  Nasłuch na samym localhoście, bo ten serwer jest dla tego, kto go
    #  uruchomił; adresu z sieci daje gunicorn na dynie (``Procfile``).
    with make_server("localhost", port, aplikacja) as serwer:
        print(f"witryna: http://localhost:{port}")
        serwer.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
