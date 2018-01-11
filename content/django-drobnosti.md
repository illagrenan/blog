Title: Užitečné funkce Djanga (o kterých jste možná nevěděli)
Date: 2017-05-25 12:21
Modified: 2018-01-11 12:52
Category: Django
Tags: django,python
Summary: Soupis několika drobností pro usnadnění vývoje v Djangu.
Status: published

Do tohoto článku si s dovolením odložím několik drobných ale užitečných funkcí Djanga.

## `defaults` parametr metody `get_or_create`

[Metoda `get_or_create`](https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create) na manageru modelů je známá a používaná &mdash; pokud `get(**params)` query vyhodí `DoesNotExist`, Django uloží do databáze nový objekt. Až doposud jsem však neznal a nepoužíval volitelný argument `defaults`. Pokud jej předáte, Django nepoužije tato data pro dotaz do databáze (`SELECT`), ale **jen pro vytvoření nové instance** (`INSERT`, tj.&nbsp;pokud nebyl záznam v databázi nalezen).

Typický *use case* může být například: u nějakého objektu chcete ukládat informaci o jeho vytvoření. V následující ukázce se Django nejprve pokusí získat existující objekt podle dvou atributů `user` a `foo`, a pokud se mu to nepodaří, založí nový objekt s vyplněným atributem `datetime_created`.

**Tip:** `timezone.now` (bez `()`) není chyba. `get_or_create` přijímá i `callable`, které zavolá v ten správný okamžik.

```python
from django.utils import timezone

my_model_obj, created = MyModel.objects.get_or_create(
                user=request.user,
                foo=bar,
                defaults={'datetime_created': timezone.now}
)
```

## Redirect na detail objektu

Nepsaným (volitelným) pravidlem je definovat metodu `get_absolute_url` na modelu.


```python
from django.core.urlresolvers import reverse
from django.db import models

class MyModel(models.Model):
    # ...

    def get_absolute_url(self) -> str:
        return reverse('my_app:my_model_detail', args=(self.id,))
```

Django tuto metodu zná a například [funkce `redirect`](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#redirect) ji umí sama zavolat a přesměrovat požadavek na detail patřičného objektu.

**Ukázka v praxi:**

```python
from django.views.generic import View
from django.http import HttpRequest, HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import redirect

class MyView(View):
    # ...

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        obj = MyModel.objects.get(pk=42)

        # ...
        # ...

        return redirect(obj) # No need to use reverse(view_name:...)
```

## `get_object_or_404` a vlastní queryset ##


Další běžně známá je [funkce `get_object_or_404`](https://docs.djangoproject.com/en/dev/topics/http/shortcuts/#get-object-or-404). Užitečné na ní je, že kromě třídy modelu **přijímá i queryset**. Můžete tak snadno omezit množinu dat, ve kterých Django hledá daný objekt před vyhozením `404`.


```python
# Get only PUBLISHED objects
my_obj = get_object_or_404(MyModel.objects.filter(is_published=True), pk=42)
```

## Context v šabloně

Vyrenderovaná Django šablona pomocí <abbr title="Class Based Views">CBV</abbr> (Class Based Views) dostává defaultně proměnnou `view` ve svém kontextu. Tato proměnná &mdash; jak napovídá název &mdash; obsahuje instanci view. Tuto funkcionalitu má na starost [`django.views.generic.base.ContextMixin`](https://docs.djangoproject.com/en/dev/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin), od kterého dědí většina tříd z <abbr title="Class Based Views">CBV</abbr>.

Tuto vlastnost je možné využít k volání metod z šablony &mdash; avšak jen takových, které nepřijímají žádné parametry.

**`view.py`:**

```python
from django.views.generic import TemplateView

class IndexTemplateView(TemplateView):
    template_name = "foo/some_page.html"

    def get_world(self):
        return "world"
```

**`foo/some_page.html`:**

```django+html
<h1>Hello {{ view.get_world }}</h1>
```

Obecně však takovýto přístup nemohu doporučit. Volat view metodu z šablony není dobrá praxe &mdash; Django šablony by měly zůstat ideálně velmi hloupé. Více o tomto tématu na [Reinout van Rees: No need to use get_context_data, use `{{ view.some_method }}`](http://reinout.vanrees.org/weblog/2014/05/19/context.html).


