Title: Hostování statického webu na S3 a Cloudfront
Date: 2018-01-16 14:41
Category: AWS
Tags: aws,s3,cloudfront
Summary: Návod, jak hostovat statický obsah na AWS (pomocí S3 a Cloudfront) s&nbsp;minimálními náklady. 
Status: published
Images: True
ShowToc: True

[TOC]

## Motivace ##

Dlouhá léta jsem na [Digital Ocean](https://www.digitalocean.com/) držel minimální VPS s Ubuntu pro experimenty, testování a hostování vlastních projektů. Postupem času na serveru zůstal pouze nginx a&nbsp;několik statických html s&nbsp;mojí vizitkou a&nbsp;tímto blogem. Už mě nebavilo platit nezanedbatelnou částku za hostování statického obsahu s minimální návštěvností a&nbsp;hlavně jsem se chtěl zbavit povinností se správou serveru. 

Hledal jsem tedy řešení, které splní:

1. Nízká cena;
2. Podpora vlastní domény;
3. Podpora TLS.

Ideálním kandidátem by byly [Github Pages](https://pages.github.com/), bohužel nepodporují (leden 2018) <abbr title="Transport Layer Security">TLS</abbr> na&nbsp;vlastní doméně.

## S3 ##

S3 z rodiny <abbr title="Amazon Web Services">AWS</abbr> netřeba sáhodlouze představovat. Jedná se o cloudové úložiště pro data (*objects*), která jsou organizovaná v *bucketech*. Uložit a hostovat pár souborů na S3 nás vyjde měsíčně na zlomky Korun &mdash; např. v regionu `eu-west-1` stojí uložení jednoho GB $0,023 ([https://aws.amazon.com/s3/pricing/](https://aws.amazon.com/s3/pricing/)).

Postup je následující:

1. Vytvoříme nový bucket ve zvoleném regionu (já např. vše umisťuji do `eu-west-1`). Jméno můžete zvolit libovolné (nikdo jej stejně neuvidí), ideální je např. název webu, který chcete takto hostovat. **Žádná jiná nastavení neupravujte**. Ještě jednou: v&nbsp;průvodci nastavíme **pouze** název bucketu a region, zbytek odklikejte.
2. Nahrajte do nového bucketu `index.html` s nějakou *Hello world* hláškou.


Pokud bychom nyní souboru `index.html` nastavili Permissions na public-read, bude obsah dostupný na adrese ve tvaru `https://s3-eu-west-1.amazonaws.com/{BUCKET_NAME}/index.html`. Víceméně jsme právě vytvořili vlastní Github Pages. S3 v nastavení (Bucket &gt; Properties) obsahuje volbu Static website hosting. Tím bychom sice dostali adresu ve tvaru `http://{BUCKET_NAME}.s3-website-eu-west-1.amazonaws.com`, na kterou už je možné vytvořit DNS CNAME záznam, avšak bez TLS.

## Cloudfront ##

Dalším produktem, který z AWS využijeme, je Cloudfront ([https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)) &mdash; globální <abbr title="Content Delivery Network">CDN</abbr> pro distibuci obsahu. Cloudfront se umí postavit před naši S3, hostovat z ní data a **hlavně vše zabezpečit vlatním certifikátem**. Jako bonus bude váš web skvěle dostupný ze všech koutů světa.

Výsledek tedy bude vypadat zhruba takto:

```
  O
 /|\   <--- index.html ---< [Cloudfront] <--- index.html ---< [S3]
 / \
```

### Vytvoření nové distribuce na Cloudfront ###

<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_1.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_1.png"
            class="figure-img img-fluid rounded"
            alt="Nová distribuce na Cloudfront">
</a>

<figcaption class="figure-caption">Vytvoříme novou distribuci</figcaption>
</figure>

<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_2.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_2.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Máme web, chceme web.</figcaption>
</figure>


<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_3.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_3.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Po kliknutí do pole <strong>Origin Domain Name</strong> nám nabídne formulář S3 buckety. Vybereme ten, který jsme v předešlém kroku vytvořili.</figcaption>
</figure>


<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_4.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_4.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Necháme Cloudfront, aby upravil Bucket Policy za nás. Bucket tak zůstane privátní, ale naše nová distribute k němu získá přístup.</figcaption>
</figure>


<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_5.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_5.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">(volitelné) Povolíme kompresi objektů.</figcaption>
</figure>

<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_6.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_6.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Do Alternate Domain Names zadáme název domény, přes kterou budou návštěvníci přicházet. Dále vybereme TLS certifikát z AWS Certificate Manager. Pokud žádný nemáme, požádáme o&nbsp;jeho vydání. Více o tom v následující sekci.</figcaption>
</figure>

<figure class="figure">

<a href="{filename}/images/cloudfront/cloudfront_7.png" data-lity>
    <img src="{filename}/images/cloudfront/cloudfront_7.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">(volitelné) Jako výchozí objekt zvolíme <code>index.html</code>. Díky tomu bude výchozí stránka webu dostupná na <code>https://example.com</code>. Volitelně povolíme IPv6.</figcaption>
</figure>

### SSL/TLS Certifikát ###

V předchozím kroku jsme použili certifikát z ACM (AWS Certificate Manager, [https://aws.amazon.com/certificate-manager/](https://aws.amazon.com/certificate-manager/)). Ty vystavuje Amazon podobným způsobem jako Let's&nbsp;Encrypt. Jejich ohromnou výhodou je, že se o celý proces validace, vystavení a prodlužování certifikátu stará Amazon automaticky. Vy sice nemáte přístup k privátnímu klíči, ale používáte tyto certifikáty zdarma.

Pozor, abyste mohli zabezpečit Cloudfront na vlastní doméně, je **nutné požádat o certifikát z regionu N.&nbsp;Virginia (US&nbsp;East)**. Region Cloudfrontu, S3 a dalších služeb nehraje roli.

> Please visit the AWS Global Infrastructure pages to see the current Region availability for AWS services. To use an ACM certificate with Amazon CloudFront, you must request or import the certificate in the US East (N. Virginia) region. ACM certificates in this region that are associated with a CloudFront distribution are distributed to all the geographic locations configured for that distribution. <cite>[https://aws.amazon.com/certificate-manager/faqs/](https://aws.amazon.com/certificate-manager/faqs/)</cite>


### Nastavení domény v Route53 ###

Rekapitulace:

* V S3 máme obsah našeho statického webu (`index.html`).
* Na S3 je nasměrovaná Cloudfront distribuce s&nbsp;certifikátem z&nbsp;ACM.

Posledním krokem je tedy nasměrování domény `example.com` v Route53 (DNS manager v&nbsp;AWS) na vytvořenou Cloudfront distirbuci.

<figure class="figure">

<a href="{filename}/images/cloudfront/route53_1.png" data-lity>
    <img src="{filename}/images/cloudfront/route53_1.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Zvolíme Hosted Zone naší domény</figcaption>
</figure>

<figure class="figure">

<a href="{filename}/images/cloudfront/route53_2.png" data-lity>
    <img src="{filename}/images/cloudfront/route53_2.png"
            class="figure-img img-fluid rounded"
            alt="Defaultní Django error report">
</a>

<figcaption class="figure-caption">Vytoříme nový záznam &mdash; alias na Cloudfront distribuci</figcaption>
</figure>

A to je vše. Gratuluji. Na `example.com` by měl být dostupný obsah z S3.

## Závěr ##

Navržené řešení se skvěle hodí i pro hostování <abbr title="Single-page application
">SPA</abbr>. Nevýhodou je chybějící podpora pokročilejší konfigurace: mně při přesunu blogu na S3/Cloudfront chyběla možnost nastavit rewrite pravidla, přesměrování a některé hlavičky. Na druhou stranu vše funguje jednoduše a téměř nic se při provozu nemůže pokazit. 

Některé drobnosti se mi nepodařilo vyřešit. Například **Default Root Object** na Cloudfrontu správně zobrazí obsah `index.html` při požadavku na&nbps;`/`, ale už **nedovede** přesměrovat `example.com/index.html` zpět na `/`. Pokud se na `index.html` dostane Google, zaindexuje duplicitní obsah. Jediné, co mě napadlo, je nastavit `canonical` URL: 

```html
<link rel="canonical" href="https://www.example.com/">
```

A cena? Nejdražší na celém řešení je Route53 ($0,5 za jednu Hosted Zone), zbytek je téměř zdarma. 

<figure class="figure">
  <a href="{filename}/images/cloudfront/billing.png" data-lity>
      <img src="{filename}/images/cloudfront/billing.png"
              class="figure-img img-fluid rounded"
              alt="Defaultní Django error report">
  </a>
  <figcaption class="figure-caption">Celková měsíční cena za hostování blogu a webové vizitky.</figcaption>
</figure>

V některém dalším článku rozepíšu přesměrování z non-www na www a hostování stránek bez `.html` v URL.


