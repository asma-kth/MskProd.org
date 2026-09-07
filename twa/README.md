# Publishing MskProd Computing to Google Play

The Android app is a **Trusted Web Activity** (TWA): a thin native shell around
the live site. It is Google's own supported route for putting a web app on Play,
and it means **content updates need no new Play release** — push to `main` as
usual and the app picks the change up.

The web side is already done and lives in this repository. What remains is the
Android build and the Play listing, which need a signing key and a Play account,
so they have to be run from your own machine.

---

## Before you start

**HTTPS on mskprod.org must be working.** The app proves it owns the domain by
fetching `https://mskprod.org/.well-known/assetlinks.json`. Until the
certificate is valid, that check fails and the app opens with a browser URL bar
across the top. Check Settings → Pages on the repository and tick **Enforce
HTTPS** once GitHub's DNS check has passed.

**A Play Console account costs $25, once.** Note that if you register as an
*individual* rather than an *organisation*, Google requires a closed test with
**12 testers running for 14 continuous days** before you may publish to
production. Organisation accounts are exempt. Decide which you are registering
as before paying.

You will also need a **privacy policy URL**. The site collects nothing and sets
no cookies, which makes this short, but Play requires the page to exist.

---

## 1. Install the tooling

Requires Node 18+ and a JDK. Bubblewrap will offer to download the Android SDK
on first run; accept.

```bash
npm install -g @bubblewrap/cli
```

## 2. Generate the Android project

From this `twa/` directory:

```bash
bubblewrap init --manifest=https://mskprod.org/site.webmanifest
```

`twa-manifest.json` in this directory holds the settings already worked out
(package id, colours, icons, launcher shortcuts). When Bubblewrap asks, either
point it at that file or accept its prompts and then overwrite the file it
generates with this one, and re-run `bubblewrap update`.

The package id is **`org.mskprod.computing`**. It cannot be changed after the
first upload to Play, so if you want something different, change it now — in
`twa-manifest.json` *and* in `TWA_PACKAGE` in `build.py`.

## 3. Create the signing key

```bash
keytool -genkeypair -v -keystore android.keystore \
  -alias mskprod -keyalg RSA -keysize 2048 -validity 10000
```

**Back this file and its passwords up somewhere safe and permanent.** If you
lose the upload key you cannot ship updates to the same app listing, and there
is no way to recover it. Do not commit it to this repository — `.gitignore`
already excludes `*.keystore`.

## 4. Build

```bash
bubblewrap build
```

This produces `app-release-bundle.aab` (upload this to Play) and
`app-release-signed.apk` (handy for testing on your own phone first).

## 5. Publish the fingerprint so the URL bar disappears

Get the SHA-256 of your signing certificate:

```bash
keytool -list -v -keystore android.keystore -alias mskprod | grep SHA256
```

Put that value — the colon-separated hex, e.g. `AB:CD:12:...` — into
`twa/sha256.txt`, one fingerprint per line, then rebuild and deploy:

```bash
echo "AB:CD:..." > twa/sha256.txt
git add twa/sha256.txt && git commit -m "Add TWA signing fingerprint" && git push
```

`build.py` picks the file up and writes `/.well-known/assetlinks.json`. Without
it the app still works, but always shows the URL bar.

**Important:** if you opt into **Play App Signing** (Google re-signs your app,
and it is the default for new apps), Play will use *its* key, not yours. After
your first upload, take the SHA-256 from
*Play Console → Release → Setup → App integrity → App signing key certificate*
and add that one too. Keeping both lines in `sha256.txt` is correct and normal —
one covers builds you sideload, the other covers what users install from Play.

## 6. Play listing

You will be asked for:

- Store listing: title, short and full description, a 512×512 icon
  (use `static/img/icon-512.png`), a 1024×500 feature graphic, and at least two
  phone screenshots.
- Content rating questionnaire — this is an educational app with no ads, no
  purchases and no user-generated content.
- Data safety form — the honest answer is that no data is collected or shared.
  Quiz scores and progress are kept in the browser's own storage on the device
  and never transmitted.
- Target audience. If you declare that the app targets under-13s you enter the
  Families programme, which brings extra policy requirements. Given the audience
  is GCSE and A Level students, **13 and over** is the accurate and much simpler
  answer.

---

## Updating later

- **Content or design changes** — just push to `main`. The app shows the live
  site, so nothing needs rebuilding or resubmitting.
- **Icon, name, colours or shortcuts** — edit `twa-manifest.json`, bump
  `appVersionCode` and `appVersionName`, run `bubblewrap update && bubblewrap build`,
  and upload the new bundle.

## What runs offline

A service worker (`sw.js`, written to the site root at build time) caches the
app shell on install, then saves each page as it is opened. A topic a student
has already read stays available with no signal; one they have never opened
shows the offline page at `/offline/`.

Pyodide, which powers the runnable Python examples, is tens of megabytes and is
fetched from a CDN only when the Run button is pressed. It is deliberately never
cached, so **runnable code examples need a connection.** Everything else —
explanations, quizzes, exam questions, mark schemes — works from the cache.
