Title: 	Instalace psycopg2 na&nbsp;Windows
Date: 2016-03-08 12:53
Modified: 2017-03-07 11:23
Category: Python
Tags: python,windows
Summary: Stručný návod na instalaci ```psycopg2``` (Python adaptér pro PostgreSQL) na Windows.

Mnoho Python balíčků je nutné při instalaci _zbuildit_ – typicky protože obsahují kód v `C` (z hlavy mě napadá např.: [cryptography](https://pypi.python.org/pypi/cryptography/) nebo [numpy](https://pypi.python.org/pypi/numpy)). Windows bohužel nemají vestavěný `C` kompilátor a ač `pip` umí pracovat v určité verzi, konfiguraci a postavení planet s Visual Studiem, ne vždy to funguje. S tímto problémem se potýká i balíček `psycopg2<=2.6.0`, Python standard pro připojení k PostgreSQL. Aktuální verze `psycopg2==2.6.1` už naštěstí tímto problémem netrpí a i na Windows stačí:

```
pip install --upgrade psycopg2
```

Co když chceme **nainstalovat starší verzi** `psycopg2`? Dobrou zprávou je, že při distribuci balíčků může jeho autor distribuovat kód už ve _zbuilděné_ podobě (`*.exe`) bez dalších závislostí. Špatnou zprávou je, že instalaci tohoto formátu `pip` nepodporuje. Naštěstí je zde starší, ale stále používaný `easy_install` ze `setuptools`. Pokud máte správně nainstalovaný `pip`, máte i `easy_install`. Mezi _pipem_ a `easy_install` jsou rozdíly, ale pro jednoduchost nám bude stačit informace, že se s oběma nástroji pracuje víceméně stejně.

Osvědčily se mi buildy `psycopg2` pro Windows z [http://stickpeople.com/projects/python/win-psycopg/index.html](http://stickpeople.com/projects/python/win-psycopg/index.html). Používáte-li Python 2.7, stačí stáhnout požadovanou verzi a v aktivovaném `virtualenv` spustit:

```
easy_install path/to/file.exe
```

Užitečnou funkcí `easy_install` instalace rovnou z URL:

```
easy_install http://stickpeople.com/projects/python/win-psycopg/2.6.1/psycopg2-2.6.1.win32-py2.7-pg9.4.4-release.exe
```
