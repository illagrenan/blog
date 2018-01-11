Title: Ochrana proti rekurzivnímu volání při zpracování Django signálu
Date: 2017-03-09 14:30
Category: Python
Tags: python,django
Summary: Co dělat, chceme-li v receiveru nějakého signálu upravit a uložit instanci a nechceme, aby tato operace opět spustila signál.
Status: published

V některých situacích můžeme při zpracování [Django signálu](https://docs.djangoproject.com/en/dev/topics/signals/#module-django.dispatch) narazit na problém rekurzivního volání jeho receiveru. Typicky se tak děje například u `post_save` signálu, jehož receiver upraví a uloží instanci modelu (přidá timestamp, upraví data&hellip;).

V minulosti jsem často (**špatně!**) používal následující pattern:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=SomeModel)
def do_something_with_instance(instance, **kwargs):
    """
    Do not do this!
    """
    post_save.disconnect(do_something_with_instance, sender=SomeModel)

    instance.foo = bar()
    instance.save()

    post_save.connect(do_something_with_instance, sender=SomeModel)

```

Na první pohled se může zdát, že jde o elegantní řešení &mdash; přijmeme signál, dočasně odpojíme receiver, zpracujeme, co potřebujeme, a&nbsp;receiver znovu připojíme. Kód má však několik nedostatků:

* Zatímco je signál odpojený, nevolá se receiver pro ostatní instance (pro ilustraci si představme, že funkce `bar()` běží „dlouho“).
* Pokud mezi odpojením a opětovným připojením nastane nějaká chyba, signál už zůstane navždy odpojený.
 
Toto téma je podrobně rozebráno na [http://stackoverflow.com/a/28369908/752142](http://stackoverflow.com/a/28369908/752142). Ze&nbsp;stejného vlákna jsem se inspiroval a následující řešení s úspěchem používám ve svých projektech:
 
```python
from functools import wraps
 
 
def prevent_receiver_recursion(receiver_function):
    dirty_attr_name = '_dirty_{}'.format(receiver_function.__name__)
 
    @wraps(receiver_function)
    def wrapper(sender, instance=None, *args, **kwargs):
        if not instance or hasattr(instance, dirty_attr_name):
            # Do nothing
            return
 
        try:
            setattr(instance, dirty_attr_name, True)
            receiver_function(sender, instance, *args, **kwargs)
        finally:
            delattr(instance, dirty_attr_name)
 
    return wrapper 
```

Myšlenka je jednoduchá, po dobu vykonávání receiveru má instance nastavený atribut, který ji „zamkne“. Použití dekorátoru je následující:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=SomeModel)
@prevent_receiver_recursion
def do_something_with_instance(instance, **kwargs):
    instance.foo = bar()
    instance.save()
```