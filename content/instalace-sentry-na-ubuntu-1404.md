Title: 	Instalace Sentry na Ubuntu 14.04
Date: 2016-04-18 14:07
Modified: 2017-03-07 14:27
Category: Python
Tags: python,windows
Summary: Instalace a základní konfigurace nástroje Sentry na Ubuntu pro logování exceptions.
Images: True

## Představení Sentry ##

Sentry ([https://getsentry.com/welcome/](https://getsentry.com/welcome/ "Sentry Homepage")) je jeden z nástrojů, bez kterých si nedovedu představit vývoj a nasazení aplikace v Djangu. Standardní logovací nástroje Djanga jsou dostatečně dobré, ale `django.utils.log.AdminEmailHandler` mě nikdy neoslovil a přitom je kritické, aby se vývojář rychle a pohodlně dozvěděl o chybě v běžící aplikaci. Hlavní nevýhody podle mě jsou:

- Dokud chybu neopravím, valí se na mě jeden e-mail za druhým;
- Ve zprávě je „pouze“ stacktrace bez dodatečných informací – výpisy proměnných, kontext chyby...;
- Vše stojí a padá na e-mailu, u kterého není nijak garantováno, že dorazí anebo že si ho po cestě nepřečte někdo jiný, ostatně o tom píše i Django dokumentace.  

> Note that this HTML version of the email contains a full traceback, with names and values of local variables at each level of the stack, plus the values of your Django settings. This information is potentially very sensitive, and you may not want to send it over email. Consider using something such as Sentry to get the best of both worlds – the rich information of full tracebacks plus the security of not sending the information over email.
<cite>[https://docs.djangoproject.com/en/dev/topics/logging/#django.utils.log.AdminEmailHandler](https://docs.djangoproject.com/en/dev/topics/logging/#django.utils.log.AdminEmailHandler)</cite>


<figure class="figure">

<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/AdminEmailHandler.png" data-lity>
    <img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/AdminEmailHandler.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Zpráva z klasického <code>AdminEmailHandler</code></figcaption>
</figure>

Dle mého názoru má toto dobře [vyřešeno např. nette](https://tracy.nette.org/cs/#toc-produkcni-rezim-a-logovani-chyb "nette – Produkční režim a logování chyb"), které v produkčním režimu (`DEBUG=False`) pošle vývojáři chybovou stránku se všemi důležitými informacemi, zaloguje chybu a dokud se neřekne, další e-mail nepošle.

<figure class="figure">
<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-error-header.png" data-lity>
    <img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-error-header.png"
            class="figure-img img-fluid rounded"
            alt="Zpráva na Sentry">
</a>

<figcaption class="figure-caption">
    Detail zprávy na Sentry, pokud byl uživatel v době chyby přihlášený, informace jsou součástí reportu. Data o prohlížeči a OS se logují vždy.
</figcaption>
</figure>


<figure class="figure">
<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-stacktrace.png" data-lity>
<img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-stacktrace.png" class="figure-img img-fluid rounded" alt="Sentry stacktrace">
</a>
<figcaption class="figure-caption">Stacktrace na Sentry s výpisem lokálních proměnných.</figcaption>
</figure>

<figure class="figure">

<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-replay-request.png" data-lity>
    <img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-replay-request.png"
            class="figure-img img-fluid rounded"
            alt="Replay request">
</a>

<figcaption class="figure-caption">Funkce Replay Request.</figcaption>
</figure>

Sentry můžete začít rovnou používat v placené verzi (*Hosted Sentry*, [https://docs.getsentry.com/hosted/](https://docs.getsentry.com/hosted/ "Hosted Sentry")) anebo si ji nainstalovat na vlastní server (*On-Premise*, [https://docs.getsentry.com/on-premise/](https://docs.getsentry.com/on-premise/ "On-Premise Sentry")). [Kód Sentry je na Githubu](https://github.com/getsentry/sentry) pod licencí BSD.

## Instalace na vlastní server ##

Sentry je napsaná v Djangu, nasazuje se tedy téměř stejně jako jakákoliv jiná Django aplikace. Budeme potřebovat:

- Ubuntu 14.04 (LTS) – neměl by být však problém nasadit Sentry na cokoliv jiného
- PostgreSQL
- Redis 3
- Python 2.7
- Supervisor

Nejprve vytvoříme adresář, kde bude vše žít. Kde přesně je v podstatě jedno, moje Sentry běží spolu s dalšími Django aplikacemi ve `/var/www`.

```
mkdir -p /var/www/sentry
```

Vytvoříme nového uživatele:

```
sudo useradd --system --home /var/www/sentry sentry
sudo chown -R sentry /var/www/sentry/
```

Nyní byste měli nastavit SSH klíč, bash atd., zde ale radit nebudu, protože má každý asi trochu jiné požadavky. V dalším kroku vytvoříme virtualenv v `~/app/...`:

```
su sentry
cd ~
mkdir app 
cd app
virtualenv sentry_env
source sentry_env/bin/activate
```

Ujistíme se, že máme poslední verzi *pipu* a *setuptools*:

```
easy_install -U pip
pip install setuptools wheel –upgrade
```

**A konečně nainstalujeme Sentry:**

```
pip install sentry
```

## Konfigurace ##

Vstupním bodem do Sentry je příkaz `sentry` (překvapivě):

```
which sentry
/var/www/sentry/app/sentry_env/bin/sentry
```

Vygenerujeme prázdné konfigurační soubory:

```
sentry init
```

A otevřeme pro úpravy:

```
nano ~/.sentry/sentry.conf.py
```

Nemělo by vás nic překvapit, jedná se víceméně o Django konfiguraci. Pro základ stačí upravit `DATABASES` a `SENTRY_WEB_HOST`. Druhým konfiguračním souborem je:

```
nano ~/.sentry/config.yml
```

kde se nastavuje odchozí e-mail. Používám jako odchozí e-mail server GMail přes SMTP. Ukázkovou konfiguraci v příslušných dvou souborech přikládám níže, nic dalšího není potřeba nastavit.

**`config.yml`:**

```yaml
###############
# Mail Server #
###############

mail.backend: 'smtp'  # Use dummy if you want to disable email entirely
mail.host: 'smtp.gmail.com'
mail.port: 587
mail.username: '***@gmail.com'
mail.password: '***'
mail.use-tls: true
# The email address to send on behalf of
mail.from: '***@gmail.com'

# ...
# ...
```

**`sentry.conf.py`:**

```python
# ...
# ...

DATABASES = {
    'default': {
        'ENGINE': 'sentry.db.postgres',
        'NAME': '***',
        'USER': '***',
        'PASSWORD': '***',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ...
# ...

SENTRY_WEB_HOST = '198.51.100.3' # TODO IP address of your server

# ...
# ...
```

## První spuštění ##

Nejprve musíme vytvořit tabulky v databázi, Sentry používá Django migrace, které spustíme pomocí:

```
sentry upgrade
```

V průběhu migrací budete požádáni o vytvoření uživatelského účtu. Nezapomeňte ho vytvořit se superuser právy!

Sentry v sobě obsahuje uwsgi server, ten spustíme:

```
sentry start
```

Na `http://{IP_ADRESA_SERVERU}:9000` by měla nyní běžet aplikace, dobrá práce! :-) Odklikejte průvodce, nastavte admin e-mail a kochejte se.

<figure class="figure">

<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-welcome.png" data-lity>
    <img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-welcome.png"
            class="figure-img img-fluid rounded"
            alt="Replay request">
</a>


<figcaption class="figure-caption">Uvítací obrazovka</figcaption>
</figure>

<figure class="figure">

<a href="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-warnings.png" data-lity>
    <img src="https://dl.dropboxusercontent.com/u/80507/blog_vaclavdohnal_cz/images/sentry/sentry-warnings.png"
            class="figure-img img-fluid rounded"
            alt="Replay request">
</a>

<figcaption class="figure-caption"><b>(1)</b> Systém by neměl hlásit žádné upozornění; <b>(2)</b> Je v pořádku, že se <i>background workers</i> nehlásí, žádní zatím neběží</figcaption>
</figure>


## Nastavení Supervisor ##

Supervisor se nám postará o automatické spuštění hlavního procesu Sentry a dále pak o řízení procesů Celery Worker a Celery Beat. Nejprve vytvoříme adresář pro uložení logů:

```
mkdir -p /var/www/sentry/app/log
```

Zde přikládám ukázkovou konfiguraci:

**`sentry.supervisor.conf`:**

```ini
[group:sentry]
programs=sentry-web,sentry-worker,sentry-beat

[program:sentry-web]
directory=/var/www/sentry/
environment=SENTRY_CONF="/var/www/sentry/.sentry/"
command=/var/www/sentry/app/sentry_env/bin/sentry start
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/sentry/app/log/web-stdout.log
stderr_logfile=/var/www/sentry/app/log/web-stderr.log
priority=100
user=sentry

[program:sentry-worker]
directory=/var/www/sentry/
environment=SENTRY_CONF="/var/www/sentry/.sentry/"
command=/var/www/sentry/app/sentry_env/bin/sentry celery worker
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/sentry/app/log/worker-stdout.log
stderr_logfile=/var/www/sentry/app/log/worker-stderr.log
priority=200
user=sentry

[program:sentry-beat]
directory=/var/www/sentry/
environment=SENTRY_CONF="/var/www/sentry/.sentry/"
command=/var/www/sentry/app/sentry_env/bin/sentry celery beat
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/www/sentry/app/log/beat-stdout.log
stderr_logfile=/var/www/sentry/app/log/beat-stderr.log
priority=300
user=sentry
```

Konfiguraci aktivujeme:

```
supervisorctl reread
supervisorctl reload
supervisorctl status
```

> (...) `SENTRY_CONF` should be pointed to the parent directory that contains both the python file and the yaml file. sentry init will generate the right structure needed for the future.
> <cite>[https://docs.getsentry.com/on-premise/server/warnings/#deprecated-settings](https://docs.getsentry.com/on-premise/server/warnings/#deprecated-settings)</cite>

## Závěr ##

Měla by vám běžet základní instalace Sentry. Možností, jak Sentry nakonfigurovat po funkční i výkonové stránce, je celá řada, sám nemám vše zmapované. Moje instance má např. navíc vypnutou veřejnou registraci, do `~/.sentry/sentry.conf.py` jen na konec souboru přidejte: 

```
SENTRY_FEATURES['auth:register'] = True
```

V některém z dalších článků chci podrobněji rozebrat:

- Logování do Sentry z Djanga a front-endu;
- Propojení Sentry a Django error stránky;
- Schování Sentry za nginx a https.