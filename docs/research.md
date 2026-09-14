# Research: site wrapper SEO/AEO pentru Marina Metzak (asistent în brokeraj, Destine Broker)

Data: 2026-09-14. Pregătit pentru sesiunea de brainstorming.

## 1. Ce este metzak-marina.smartsales.ro

- Platformă white-label BrokerNet Software (ASP.NET Core). Fiecare asistent în brokeraj primește un subdomeniu = „carte de vizită electronică" + flux de vânzare online.
- Broker principal: **DESTINE BROKER DE ASIGURARE-REASIGURARE SRL**, Ploiești, Str. Torcători nr. 4, et. 1, ap. 2. CUI 21678074, J29/1143/2007, **RBK-425/20.08.2007**, Decizia ASF 577/17.08.2007. Tel 0344 801 880, office@destine-broker.com.
- Site-ul NU afișează numele Marinei, telefon, cod RAF, zonă. Zero identitate personală.

### Inventar URL-uri (stabile, pe subdomeniu) — ținte pentru linkurile din wrapper

| Produs | URL stabil | Categorie internă |
|---|---|---|
| RCA | `/rca` | RCA |
| Locuință facultativă | `/locuinta` | LOCUINTE |
| PAD (obligatorie) | `/pad` | PAD |
| Călătorie (medicală + storno) | `/travel` | TRAVEL |
| Sănătate | `/sanatate` | |
| Malpraxis | `/malpraxis` | |
| ROTR (transportatori) | `/rotr` (+ `/rotr/detalii`) | |
| Accidente Taxi/Uber/Bolt (SIGNAL) | `/accidente` | |
| Asistență domiciliu | `/asistentaladomiciliu` | |
| Asistență rutieră | `/asistentarutiera` | |
| Catalog complet | `/home/asigurari` (ancore `#auto #locuinte #sanatate #turism #asigurariPf #asigurariPj`) | |
| Asistență (hub) | `/home/asistenta` | |
| CASCO, Viață, Pensii Pilon III, Răspundere legală | doar în catalog `/home/asigurari` — butonul „Cumpără" duce la formular lead (nume/telefon/email), nu flux online | |

### Mecanica fluxului
- `/rca` → 302 → `/presale/create/<token>` (token nou per sesiune). Pagina „Informarea clientului": tip persoană, nume, prenume, 3 checkbox-uri (renunțare consultanță, termeni + mandat brokeraj, informare retragere RCA 14 zile OUG 34/2014) → „Continuă".
- Câmp hidden `ReturnUrl=/rca` → linkăm mereu la path-ul scurt, nu la token.
- Atribuirea către Marina = **subdomeniul**. Cookie `.SmartSalesBroker` domeniu `.smartsales.ro`. Concluzie: toate CTA-urile din wrapper trebuie să pointeze la `https://metzak-marina.smartsales.ro/<path>`; niciodată la `destine.smartsales.ro`.
- Există și formular contact `/home/cererecontact` (POST, recaptcha) — nu se poate folosi cross-origin din wrapper.

### De ce smartsales nu face SEO (justificarea wrapper-ului)
- Title generic „Home - SmartSales", meta description identică pe toate paginile, fără robots.txt, fără sitemap, fără schema, fără H1 relevant, paginile de produs = redirect la formular (conținut zero indexabil), fără `hreflang`/canonical, og:image = logo SmartSales.
- Sute de subdomenii identice (`destine.`, `domas.`, `olaru-andrei.`…) → duplicate content la nivel de platformă.

## 2. Cadru legal pentru un site propriu de asistent în brokeraj

Verificat pe Norma ASF 19/2018 (legislatie.just.ro, lege5.ro) + căutări; Legea 236/2018 art. 15 (comercializare electronică) și art. 22 (informații către client) NU au fost citite integral — de confirmat cu Destine Broker (departament conformitate) înainte de lansare.

Obligatoriu / recomandat pe site:
- Cod unic RAF + mențiunea exactă **„Înregistrat la Autoritatea de Supraveghere Financiară"** (Norma 19/2018 art. 5 (10), art. 6 (5)) — pe toate documentele oficiale; practic: footer + pagina Despre.
- Denumirea intermediarului principal (Destine Broker, RBK-425) și faptul că Marina acționează „în numele și pe seama" acestuia, sub răspunderea lui.
- Link către registrul ASF (asfromania.ro) pentru verificare.
- Politică GDPR + cookies (Legea 506/2004, GDPR), ANPC + SOL (link-uri obligatorii pentru comerț electronic), Termeni.
- Fără prețuri/tarife afișate în wrapper (tarifele vin din platformă; evităm publicitate înșelătoare).
- Precedent de piață: **IASIASIG ASISTENT IN BROKERAJ S.R.L.** rulează asigurari-iasi.ro cu „Cod RAF: 143944" afișat public — modelul exact pe care îl construim.

Necesar de la Marina: codul RAF, forma juridică (PFA / SRL, CUI), telefon/WhatsApp, e-mail, zona de acoperire, poză, text scurt biografie, eventual aprobare scrisă de la Destine pentru folosirea logo-ului.

## 3. Cuvinte cheie & intenție (Google Autocomplete RO, 2026-09-14)

- `asigurari iasi` → auto, pacurari, program, broker asigurari iasi, asigurari rca iasi. Intenție locală clară.
- `broker asigurari iasi` → broker asigurari auto iasi, broker asigurari rca iasi.
- `asigurare rca online` → ieftina, verificare, in rate, 1 luna, remorca, **moldova** (sic — Republica Moldova, dar și regiunea).
- `asigurare pad` → online, pret, ce acopera, ce inseamna, pret 2026.
- `asigurare malpraxis` → asistent medical, medici rezidenti, psiholog, kinetoterapeut, farmacist, fizioterapeut — nișă bogată, long-tail, concurență mică. Iași = oraș universitar-medical (UMF). Oportunitate mare.
- `asigurare uber bolt` → bagaje, calatori si bagaje. Produs SIGNAL taxi/rideshare = diferențiator, aproape nimeni nu are landing dedicat.
- `asigurare rotr` → pret, online, ce inseamna, calculator.
- `asigurare calatorie` → grecia, turcia, pret, online. Landing-uri pe destinație = long-tail ieftin.
- `asigurare sanatate privata` → pret, copii, cost, medlife/regina maria.
- Volume exacte: nu avem tool (fără Keyword Planner). Autocomplete = proxy calitativ.

## 4. Competiție locală Iași (SERP „broker asigurari iasi")

- asigurari.ro (`/asigurare/rca/iasi` — pagini per oraș, generat programatic), transilvaniabroker.ro (`/locatii/judet/iasi`, 19 asistenți), asigurari-iasi.ro (IASIASIG, asistent în brokeraj, +10 ani), cumpar-asigurare.ro (DAW, `/agentie/iasi`), destine-broker.ro/retea/iasi/ (un singur agent listat: Postelnicu Andrei; Marina nu apare).
- destine-broker.ro/asigurari/asigurare-rca/ = ~4.500 cuvinte, 7 FAQ, CTA → destine.smartsales.ro/RCA (nu subdomeniul Marinei). Nu concurăm cu ei pe „asigurare rca" national; concurăm pe local + nișe + persoană.
- Nicio pagină de asistent Destine Iași nu are: persoană reală cu poză, WhatsApp, FAQ structurat, schema Person/LocalBusiness. Asta e golul.

## 5. Domenii

Preț .ro: 12 €/an la RoTLD direct; registrari acreditați 6,4–8,5 €/an (host-age.ro, datahost.ro, iphost.ro). .com ~10–13 €/an. Bugetul e irelevant — orice opțiune < 15 €/an.

Verificat whois RoTLD (răspuns ferm) / DNS:

**Libere .ro (confirmate whois):**
- `asigurariiasi.ro` ★ (local, exact-match, dar „asigurari-iasi.ro" e luat de competitor IASIASIG din 2009 → risc confuzie de brand)
- `marinaasigurari.ro` / `asigurarimarina.ro` / `asigurari-marina.ro` / `marina-asigurari.ro` ★ (personal, memorabil, „asigurări cu Marina" — brand pe persoană, unic, portabil dacă schimbă brokerul)
- `asigurarisimplu.ro` / `asigurari-simplu.ro` (brand generic; `asigurarisimple.ro` luat mai 2026)
- `politamea.ro` / `polita-mea.ro` (scurt, brandabil)
- `rcaiasi.ro` / `rca-iasi.ro` (prea îngust — doar RCA)
- `asigurarimoldova.ro` / `asigurari-moldova.ro` (regional; ambiguu cu Rep. Moldova)
- `asigurariusor.ro` / `asigurari-usor.ro`, `asigurarirapide.ro`, `metzak.ro`, `asiguratcumarina.ro`, `asigurari-online-iasi.ro`
- Probabil libere (DNS NXDOMAIN, whois nereconfirmat din cauza rate-limit RoTLD): `asigurareiasi.ro`, `politaiasi.ro`, `marinametzak.ro`, `asigurarinordest.ro`, `asiguraricumarina.ro`, `asigurariclare.ro`, `asigurarisigure.ro`, `asigurarilinistite.ro`, `asigurareamarina.ro`

**Libere .com (whois):** asigurariiasi.com, marinaasigurari.com, asigurarimarina.com, asigurarisimplu.com, politamea.com, rcaiasi.com, asigurarimoldova.com. (`metzak.com` luat din 2004.)

**Luate:** asigurari-iasi.ro (2009), asigurat.ro, asigurate.ro, polita.ro, asigurareonline.ro, asigurari24.ro, asigurari-ieftine.ro, asigurari-rapide.ro (sept 2025), politaonline.ro (iul 2026), asigurarisimple.ro (mai 2026), asigurareata.ro, asigurarea-ta.ro.

Recomandare preliminară: **marinaasigurari.ro** (brand pe persoană + categorie; E-E-A-T pentru AI; nu depinde de Iași dacă vinde online în toată țara) + opțional `asigurariiasi.ro` redirect 301 (protecție + exact-match local). Sub 20 €/an pentru ambele.

## 6. Ce înseamnă SEO + AEO/AIO aici (tactici concrete)

- Static site, HTML curat, <1s LCP, fără JS greu. Fiecare produs = pagină proprie cu: răspuns direct 40–60 cuvinte sus, H2 sub formă de întrebare, FAQ 5–8 întrebări, CTA „Calculează/Cumpără online" → smartsales, CTA secundar WhatsApp.
- Schema.org JSON-LD: `Person` (Marina, jobTitle „Asistent în brokeraj", worksFor Destine Broker, areaServed), `InsuranceAgency`/`LocalBusiness` (dacă are adresă/telefon), `FAQPage` pe fiecare produs, `BreadcrumbList`, `Service` per produs, `Organization` cu `sameAs` (Facebook, LinkedIn, registrul ASF).
- Google Business Profile pentru Marina (cea mai rapidă sursă pentru AI Overviews local) — necesită adresă fizică sau „service area business".
- `llms.txt` + `robots.txt` care permite GPTBot/ClaudeBot/PerplexityBot, sitemap.xml, canonical, og:image personalizat.
- Pagini locale: Iași + cartiere/orașe din județ (Pacurari, Tătărași, Nicolina, Pașcani, Hârlău...) DOAR dacă avem conținut real distinct, altfel thin-content. Regiune Moldova (Bacău, Vaslui, Botoșani, Suceava, Neamț) — doar dacă acoperă efectiv.
- Nișe cu concurență mică: malpraxis pe profesie (asistent medical, rezident, psiholog, kinetoterapeut, farmacist), taxi/Uber/Bolt, ROTR, călătorie pe destinație.
- Blog/ghiduri „actualizat 2026" (prospețime = 83% din citările AI sunt pe pagini <12 luni).
- Măsurare: Search Console, GA4/Plausible, UTM pe linkurile către smartsales (`?utm_source=marinaasigurari` — de verificat că smartsales tolerează query-string pe `/rca`).

## 7. Stack / hosting (din proiectele tale existente)

- metzcode: **Eleventy + Firebase Hosting** (static, multi-language, sitemap). metz-platform: Next.js + Tailwind + Supabase.
- Pentru wrapper: site static e ideal (SEO, zero backend, gratis pe Firebase Hosting / Cloudflare Pages). Opțiuni: Eleventy (reutilizezi setup metzcode) sau Astro (content collections, i18n, imagini optimizate nativ). Decizie la brainstorming.

## 8. Întrebări deschise pentru brainstorming

1. Brand: pe persoană („Marina Asigurări") sau generic/local („Asigurări Iași")?
2. Zonă: doar Iași, regiunea Moldova, sau toată România (vânzarea e online oricum)?
3. „Regiuni" în cerința ta = secțiuni de produs (RCA/locuințe…) sau pagini geografice? Ambele?
4. Date Marina: cod RAF, PFA/SRL, telefon/WhatsApp, adresă birou (da/nu → decide LocalBusiness vs Person), poză, acord Destine pentru logo.
5. Produse prioritare: RCA aduce trafic dar comision mic; malpraxis/sănătate/călătorie = marjă. Ce vrea ea să vândă?
6. Limbă: doar RO? (EN pentru expați Iași?)
7. Stack: Eleventy vs Astro; hosting Firebase vs Cloudflare Pages.
8. Conținut: cine scrie textele (eu generez draft, ea validează tehnic)?

## Surse
- https://metzak-marina.smartsales.ro/ (+ /home/asigurari, /rca etc.)
- https://destine-broker.ro/ , /retea/iasi/ , /asigurari/asigurare-rca/
- https://termene.ro/firma/21678074-DESTINE-BROKER-DE-ASIGURARE-REASIGURARE-SRL
- https://legislatie.just.ro/Public/DetaliiDocumentAfis/209094 (Norma ASF 19/2018)
- https://lege5.ro/Gratuit/gmydkmrqgmza/legea-nr-236-2018-privind-distributia-de-asigurari
- https://www.asigurari-iasi.ro/broker-asigurari-iasi/ (precedent asistent cu site propriu, cod RAF afișat)
- https://rotld.ro/register-a-new-ro-domain/ , https://www.host-age.ro/inregistrare-domenii/
- https://almcorp.com/blog/answer-engine-optimization-2026/ , https://www.airops.com/blog/aeo-answer-engine-optimization
