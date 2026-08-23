"""Witryna nad werdyktem: boczny tor, bez którego olski działa tak samo.

Pakiet stoi poza paczką, jak ``harness/`` obok niego, i importuje w jedną stronę:
witryna woła olskiego, a olski o witrynie nie wie.
Po co ten tor jest i czego nie robi, mówi ``docs/witryna.md``.

Warstwy są dwie i granica między nimi jest granicą wiedzy.
``witryna/werdykty.py`` wie o olskim i o HTTP nie wie nic;
``witryna/serwer.py`` wie o HTTP i o gramatyce nie wie nic.
"""
