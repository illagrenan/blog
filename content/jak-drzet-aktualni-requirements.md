Title: Jak držet aktuální requirements
Date: 2016-04-30 16:16
Modified: 2017-03-07 11:23
Category: Python
Tags: python,windows
Summary: Zamyšlení nad specifikací verzí v requirements a představení pypiup.

Vždy při specifikaci `requirements.txt` se rozhoduji, zda jít cestou volně (tj. bez *pinned* verzí) definovaných závislostí anebo striktně definovat, kterou verzi projekt požaduje.

Ani jedna cesta není ideální, volné závislosti sice umožňují rychlejší *updaty* a projekt se při vývoji posouvá se svými závislostmi dopředu, ale mohou se do kódu zavést nové a nečekané chyby. Na druhé straně přijít po roce či dvou k projektu, který má všechny závislosti definované přes `==` také není OK – na update pak často není prostor a projekt může záviset na již nepodporovaném/zabugovaném/jinak rozbitém kódu třetích stran.

Snažím se tedy vždy najít nějaký kompromis. Zásadní závislosti definuji přesně a jejich update provádím ručně, např.:

```ini
Django[bcrypt]==1.9.5
psycopg2==2.6.1
```

Na druhé straně u některých závislostí vím, že i po špatném updatu se mi projekt nerozbije, ty pak definuji takto:

```ini
django-extensions>=1.6.1,<2.0.0
```

Tedy spodní verze je ta naposledy nainstalovaná/odzkoušená a horní verze je omezena nejbližším MAJOR/MINOR (podle toho, jak hodně jsem si jistý, že to projekt zvládne) releasem dle semver (viz [http://semver.org/][1]).

## Kontrola aktualizací

Nedávno jsem objevil užitečný nástroj `pypiup` [https://github.com/ekonstantinidis/pypiup][2]. Ten vezme soubor s `requirements` a zkontroluje, zda jsou definované závislosti aktuální:

```
pypiup -r .\requirements\base.txt
```

Nutno podotknout, že `pypiup` zvládá kontrolu jen těch balíčků, které podporují sémantické verzování, ale těch už je dnes naštěstí většina.


  [1]: http://semver.org/
  [2]: https://github.com/ekonstantinidis/pypiup