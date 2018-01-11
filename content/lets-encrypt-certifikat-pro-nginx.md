Title: Let's Encrypt certifikát pro nginx
Date: 2016-03-09 00:31
Modified: 2017-03-07 11:23
Category: Python
Tags: python,windows
Summary: Instalace Let's Encrypt klienta a generování SSL certifikátu pro nginx (ačkoliv pro Apache je postup totožný).

* * *
**Edit 8\. září 2016:** Let's Encrypt klient se nově jmenuje cerbot a nachází se na nové URL [https://github.com/certbot/certbot](https://github.com/certbot/certbot). Článek byl na příslušných místech upraven, avšak kromě jména a adresy se nic jiného nemění.
* * *

Díky [službě Let's Encrypt](https://letsencrypt.org/) už nemůže být TLS/SSL zabezpečení webu jednodušší. Kdo nezná, v krátkosti představím. Let's Encrypt je v první řadě certifikační autorita, která **zdarma** nabízí certifikáty pro libovolné množství vašich domén. Certifikáty jsou [_cross-signed_ IdenTrustem](https://letsencrypt.org/certificates/), takže je přijímají prohlížeče na Windows, Linuxu, Macu, Androidu... [zde je seznam zařízení](https://community.letsencrypt.org/t/which-browsers-and-operating-systems-support-lets-encrypt/4394), které jsou OK a které mohou mít naopak problémy.

Let's Encrypt však není jen certifikační autorita, bezúplatný certifikát nabízí např. i [StarSSL](https://www.startssl.com/). Tou revoluční funkcí je automatizace. Let's Encrypt má klienta (jinak než bez klienta stejně certifikát nedostanete), který spustíte na svém serveru a on udělá vše za vás. Žádné ověřování domény, generování <abbr title="Certificate Signing Request">CSR</abbr> a dokonce ani žádná registrace.

## Zabezpečujeme nginx

[Klient Let's Encrypt](https://github.com/letsencrypt/letsencrypt) umí pracovat v módu, kdy se děje vše automaticky na pozadí – prodlužování certifikátů (ty jsou mimochodem platné jen 90 dní), ověřování domény, ale i automatická aktualizace nginx/Apache konfigurace. To poslední se mi zrovna dvakrát nezamlouvá, nechci, aby se třetí strana vrtala v mé konfiguraci serveru, stejně mám veškerou konfiguraci verzovanou na gitu, takže bych jen zahazoval změny na serveru.

Ukážeme si, jak pracovat s Let's Encrypt bez magie okolo. V závěru z klienta vypadne soubor certifikátu a privátní klíč a další kroky uděláme ručně.

### Co potřebujeme před startem

*   Git, Python
*   root práva na serveru
*   Testováno na Ubuntu 14.04.x LTS

## Instalace a spuštění klienta

Jako root naklonujeme repositář s klientem:

```
sudo git clone https://github.com/certbot/certbot /opt/cerbot
service nginx stop # Musíme dočasně zastavit nginx, LE ověřuje doménu přes port 80
cd /opt/cerbot
```

Spustíme Let's Encrypt klienta. První spuštění může chvíli zabrat, klient instaluje `virtualenv`, kontroluje systém atp.

```
./certbot-auto certonly --standalone
```

Po spuštění odsouhlasíme licenční podmínky, zadáme e-mail a **seznam domén (včetně subdomén)**, pro které chceme vygenerovat certifikát. O vše další se postará Let's Encrypt.

## Nastavení nginx

Vygenerované certifikáty se nacházejí ve složce `/etc/letsencrypt/***/fullchain.pem` a `/etc/letsencrypt/***/privkey.pem`. Např. pro tento web je tedy cesta `/etc/letsencrypt/blog.vaclavdohnal.cz/fullchain.pem`. Certifikáty nikam nepřesouvejte, klient by pak nevěděl, pro jaké weby má certifikáty obnovit, nově vygenerovat...

Poslední fází je úprava konfigurace nginx. Pro inspiraci předkládám důležité části z konfigurace pro tento web, kdy jsou všechny požadavky na port `80` přesměrovány na `443`. Vhodnější je samozřejmě použít <abbr title="HTTP Strict Transport Security">HSTS</abbr>, ale myslím si, že pro blog je řešení _good-enough_. Dále vřele doporučuji [článek od Filipa Procházky na téma nginx a https](https://filip-prochazka.com/blog/nginx-https-spdy-hsts-security).

Server poslouchá i na protokolu `spdy`, pokud máte [novější nginx (od verze 1.9.5)](http://nginx.org/en/docs/http/ngx_http_v2_module.html), změnte `spdy` na `http2`. Poslední dvě direktivy `include` odkazují na dva soubory z projektu [https://github.com/h5bp/server-configs-nginx](https://github.com/h5bp/server-configs-nginx), kde jsou skvěle okomentované a popsané _best practice_ pro nginx. Viz [server-configs-nginx/h5bp/directive-only/**ssl.conf**](https://github.com/h5bp/server-configs-nginx/blob/master/h5bp/directive-only/ssl.conf) a [server-configs-nginx/h5bp/directive-only/**ssl-stapling.conf**](https://github.com/h5bp/server-configs-nginx/blob/master/h5bp/directive-only/ssl-stapling.conf).

A to je vše, už jen stačí znovu spustit nginx:

```
service nginx start
```