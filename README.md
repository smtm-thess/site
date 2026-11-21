# Το site του ΣΜΤΜ

Το site του Σωματείου Μισθωτών Τεχνικών Μακεδονίας. Στατικό site με [Astro](https://astro.build),
που ανεβαίνει μόνο του στο GitHub Pages σε κάθε αλλαγή. Χωρίς cookies, χωρίς παρακολούθηση,
με τις γραμματοσειρές μέσα στο ίδιο το site.

## Νέα ανακοίνωση

1. Το κείμενο σε μορφή builder (`@title`, `@sub`, `@p`, `@h`, `@hc`, `@b`, `@box`, `@boxb`, `@boxc`, `@c+`):
   ```
   python3 tools/txt2md.py κείμενο.txt --date 2026-12-03 --slug lexeis-me-paules \
       --kind "Ανακοίνωση" --summary "Μία-δύο προτάσεις σε πεζά." \
       --pdf /pdf/2026-12-03-lexeis-me-paules.pdf
   ```
   Γράφει το `src/content/anakoinoseis/2026-12-03-lexeis-me-paules.md`.
2. Το PDF μπαίνει στο `public/pdf/` με το ίδιο όνομα.
3. Αλλιώς, γράφεις το `.md` με το χέρι: frontmatter όπως στα υπάρχοντα, και κείμενο σε Markdown ή HTML.
4. Commit στο `main`. Σε δύο λεπτά είναι online, με δική του εικόνα κοινοποίησης στο `/og/<όνομα>.png`.
5. Το email για τα μέλη: `python3 tools/email.py src/content/anakoinoseis/<όνομα>.md > email.html`,
   και επικόλληση στο Sender ως δικό σας HTML. Το `{{UNSUBSCRIBE}}` γίνεται ο σύνδεσμος διαγραφής του Sender.

Πεδία στο frontmatter: `title`, `sub` (λίστα), `date`, `kind` (η ετικέτα, π.χ. «Δελτίο τύπου»),
`cat` (`anak`, `apof`, `dt`, `drasi`), `summary`, `pdf`, `event` (`label`, `when`, `where`),
`og` (`title` με `|` για αλλαγή γραμμής, `line`), `external` (κείμενο που μένει στο παλιό site),
`draft: true` (δεν δημοσιεύεται).

## Ο αγώνας της στιγμής

Το κόκκινο μπλοκ της αρχικής ρυθμίζεται στο `src/data/agonas.ts`. Φαίνεται ως και τη μέρα `until`.
Μετά, η αρχική δείχνει στη θέση του το νεότερο κείμενο. Το site ξαναχτίζεται κάθε πρωί.

## Στοιχεία του Σωματείου

Email, τηλέφωνα, διεύθυνση, κανάλι Viber, μισθοί που διεκδικούμε: `src/consts.ts`.

## Τοπικά

```
npm install
npm run dev        # http://localhost:4321
npm run build      # το site στο dist/
```
Χρειάζεται Node 22.23 ή νεότερο.

## Δημοσίευση

Το `.github/workflows/deploy.yml` χτίζει και ανεβάζει το site σε κάθε push στο `main`, κάθε πρωί
και με το χέρι (Actions, «Run workflow»). Μία φορά, στο GitHub: Settings, Pages, Source: **GitHub Actions**.

Η διεύθυνση και ο υποφάκελος έρχονται από τις ρυθμίσεις του Pages. Για το smtm.gr:
Settings, Pages, Custom domain: `smtm.gr`, και στο DNS:

| Τύπος | Όνομα | Τιμή |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<λογαριασμός>.github.io` |

Μετά: Enforce HTTPS.

## Αρχεία

- `src/pages/`: οι σελίδες (αρχική, ανακοινώσεις, ΣΣΕ, γίνε μέλος, γράψε μας, ποιοι είμαστε, δεδομένα)
- `src/content/anakoinoseis/`: τα κείμενα
- `src/components/`, `src/layouts/`: τα κομμάτια που επαναλαμβάνονται
- `src/styles/global.css`: όλη η εμφάνιση
- `src/lib/og.ts`: οι εικόνες κοινοποίησης (satori)
- `tools/`: μετατροπή κειμένων, γραμματοσειρές για τις εικόνες (SIL Open Font License)

Οι φόρμες «Γίνε μέλος» και «Γράψε μας» ανοίγουν το email του επισκέπτη με το μήνυμα έτοιμο.
Δεν περνούν από καμία τρίτη υπηρεσία.
