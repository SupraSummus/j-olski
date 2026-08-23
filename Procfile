#  Boczny tor na jednym dynie: gunicorn woła aplikację WSGI z witryny.
#  --pythonpath . dlatego, że witryna stoi poza paczką, tak jak harness.
#  --preload buduje gramatykę raz, w procesie nadrzędnym, więc worker dostaje ją
#  przez fork; słownik Morfeusza dzieli się i tak, bo wchodzi z pliku.
#  Workerów jest dwóch, żeby rozbiór trwający sekundę nie wstrzymywał strony,
#  a nie po to, żeby liczyć więcej naraz. Co to kosztuje w pamięci i skąd ta
#  liczba, mówi docs/witryna.md.
web: gunicorn --preload --pythonpath . --workers 2 --timeout 10 --bind 0.0.0.0:$PORT witryna.serwer:aplikacja
