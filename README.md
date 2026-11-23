# Pages d'immersion · Les Stratèges

Les pages « Votre espace d'admission » que le closer envoie à la famille entre le R1 et le R2.

Toutes les pages sont identiques. Seul le bloc **3 · Ils l'ont fait** change : le témoignage d'un élève admis dans l'université visée par la famille. On fait donc **une page par école qui a un témoignage** (Columbia, Princeton, Harvard, Yale pour commencer).

Ce sont des pages HTML statiques. Elles n'ont pas de base de données ni de formulaire, et ne demandent aucune clé API. Elles sont en `noindex` : Google ne les référence pas, seules les familles qui ont le lien y accèdent.

---

## 1. Ce qu'il y a dans le repo

```
dist/                  ← LES PAGES À METTRE EN LIGNE (déjà générées)
  index.html             (racine du domaine : renvoie vers le lien du chargé d'admission)
  columbia/index.html
  princeton/index.html
  harvard/index.html
  yale/index.html
  (chaque dossier contient aussi son dossier assets/ : logo, blasons, fiche PDF)

src/page.html          ← le gabarit commun à toutes les pages
src/assets/            ← logo, 8 blasons, fiche « point en famille » (PDF)
build.py               ← régénère dist/ à partir du gabarit et de la liste des écoles
vercel.json            ← réglage prêt si vous hébergez sur Vercel
```

---

## 2. Brancher les pages sur votre nom de domaine

Proposition d'adresses (à adapter) :

```
https://admission.ivy-strategy.co/columbia
https://admission.ivy-strategy.co/princeton
https://admission.ivy-strategy.co/harvard
https://admission.ivy-strategy.co/yale
```

### Option A : Vercel (le plus simple, gratuit)
1. Sur vercel.com : **Add New → Project → Import** ce repo GitHub.
2. Aucun réglage à toucher : `vercel.json` sert directement le dossier `dist/`.
3. **Settings → Domains** : ajoutez `admission.ivy-strategy.co`.
4. Chez votre registrar (DNS), créez l'enregistrement que Vercel indique, en général :
   `CNAME  admission  →  cname.vercel-dns.com`
5. Chaque modification poussée sur le repo se met en ligne toute seule.
6. **Indispensable une fois le domaine choisi** : renseignez-le dans `build.py` (`"domaine": "https://admission.ivy-strategy.co"`), lancez `python3 build.py`, puis poussez. C'est ce qui fait apparaître l'image et le titre quand le closer colle le lien sur WhatsApp. Sans ça, le lien arrive nu chez la famille.

### Option B : votre hébergement actuel
Copiez le **contenu du dossier `dist/`** à la racine du sous-domaine (ou dans un sous-dossier de votre site). Chaque dossier (`columbia/`, `harvard/`…) devient une adresse. Rien d'autre à installer.

### Option C : Netlify, Cloudflare Pages, etc.
Pas de commande de build, dossier publié = `dist`.

> Si vous utilisez un constructeur de site (Webflow, Framer, Systeme.io…), créez plutôt un sous-domaine dédié (`admission.`) qui pointe vers Vercel (option A). Coller ces pages dans un constructeur casserait la mise en page.

---

## 3. État des pages (23/11)

Les 4 pages écoles sont complètes : témoignages en ligne, fiche « point en famille » finale (version d'Enzo du 23/11) en PDF téléchargeable, avec son aperçu sur la page.

Retirés à la demande d'Enzo (23/11) : la vidéo de Léa sur la fiche (pas de Loom prévu) et le bloc des conditions générales d'admission (document inexistant).

Pour changer la fiche : remplacer `src/assets/fiche-point-en-famille.pdf` et `src/assets/fiche-apercu.jpg` (image de la page 1), puis régénérer.

---

## 4. Ajouter un élément manquant

Tout se règle en haut de `build.py`, puis on régénère.

**Les vidéos** se mettent en ligne sur YouTube en **non répertorié**. Pour chaque vidéo, on colle seulement l'identifiant, c'est-à-dire ce qui suit `youtu.be/` (exemple : `youtu.be/UYbjRTaa7lc` → `UYbjRTaa7lc`).

```python
COMMUN = {
    "domaine": "https://admission.ivy-strategy.co",  # votre sous-domaine final
}

ECOLES = {
    "columbia": {"ecole": "Columbia", "logo": "columbia",
                 "intro": "Texte au-dessus des vidéos",
                 "temoignages": [{"yt": "IDENTIFIANT_YOUTUBE", "legende": "Prénom, admis à Columbia"}]},
    # plusieurs vidéos possibles : elles s'affichent côte à côte
    ...
}
```

Ajouter une école : décommentez sa ligne dans `ECOLES` (les 8 blasons sont déjà là).

Puis régénérez :

```bash
python3 build.py
```

Le script affiche l'état de chaque page (`PRÊTE` ou ce qui manque). Ensuite, commitez et poussez : si c'est hébergé sur Vercel, tout se met en ligne automatiquement.

Si vous préférez ne pas toucher au code, envoyez les liens à Yakine et il régénère les pages.

---

## 5. Lien à donner aux closers

Une fois en ligne, le closer envoie à la famille la page de **l'école visée par l'élève** (son plan A), avec le message de relance entre R1 et R2. Si l'école visée n'a pas encore de témoignage, il envoie la page de l'école la plus proche (Harvard en priorité).


---

## 6. Pages vidéo simples (VSL)

Trois pages « titre + vidéo » à envoyer aux familles, pour ne jamais envoyer le lien brut de l'hébergeur :

| Adresse | Vidéo | Quand l'envoyer |
|---|---|---|
| `/piliers/` | Les 6 piliers d'un dossier admis (VSL 1) | avant le R1 |
| `/plans-b/` | Les plans B de luxe (VSL 2) | entre le R1 et le R2 |
| `/plan-de-reussite/` | Présentation du plan de réussite (VSL 3) | entre le R1 et le R2 |

Elles se règlent dans `VIDEOS` en haut de `build.py`.
