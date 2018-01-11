Title: Testovací PYPI pro vyladění releasu balíčků
Date: 2016-08-15 18:48:21
Modified: 2017-03-07 11:23
Category: Python
Tags: python,windows
Summary: Při vývoji open-source balíčku pro PYPI (the Python Package Index) se mohou i přes veškeré testování projevit chyby až po *releasu*. V tomto článku představíme testovací PYPI, který slouží autorům jako *sandbox*.

Při vývoji open-source balíčků pro [PYPI][1] (the Python Package Index) se mi i přes veškeré automatické testování kódu často stává, že objevím nějakou chybu související s releasem až po releasu. Typicky se jedná o chybně naformátované `README.rst` (parser na PYPI je extrémně citlivý a [podpora Markdownu se bohužel nekoná][2]), omylem zveřejněnou `__pycache__` atd. 

Soubory na PYPI je možné smazat, ale od [ledna 2015 už není možné soubory se stejnou verzí znovu nahrát](https://mail.python.org/pipermail/distutils-sig/2015-January/025687.html). 

Nezbývá tedy než vydat novou verzi balíčku (v kontextu [sémantického verzování](http://semver.org/) se jedná o inkrementaci `x.x.PATCH` segmentu). Bohužel v&nbsp;případě zmiňovaného formátování `README.rst` se stejně nedozvíte, kde reálně chyba je, opravujete tak naslepo... a verze mohou přibývat.

## Test PYPI ##

Pro otestování samotného releasu přichází ke slovu testovací PYPI, o kterém jsem se nedávno dozvěděl. Nachází se na adrese [https://testpypi.python.org/pypi](https://testpypi.python.org/pypi) a funguje stejně jako jeho „ostrá“ verze – tj. zaregistrujete svou osobu a package, vytváříte releasy atd.

Registrace balíčku:

```
python setup.py register -r https://testpypi.python.org/pypi
```

Release balíčku:

```
python setup.py sdist upload -r https://testpypi.python.org/pypi
python setup.py bdist_wheel upload -r https://testpypi.python.org/pypi
```

Ačkoliv je testovací PYPI skvělý pomocník, stoprocentně na něj spoléhat nelze. V době psaní článku např. neuměl testovací PYPI tagy pro nové Django 1.10:

```
running register
running egg_info
...
running check
Registering ... to https://testpypi.python.org/pypi
Server response (400): Invalid classifier "Framework :: Django :: 1.10"
```

  [1]: https://pypi.python.org/pypi
  [2]: https://bitbucket.org/pypa/pypi/issues/148/support-markdown-for-readmes