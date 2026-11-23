"""Génère les pages d'immersion Les Stratèges : une page par école témoin.

La page est identique partout, seul le bloc « Ils l'ont fait » change.
Remplir CONFIG ci-dessous puis lancer : python3 build.py
Sortie : dist/<slug>/index.html (+ dist/<slug>/assets/).
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# Liens communs à toutes les pages. None = pas encore reçu (repère « à ajouter » affiché).
COMMUN = {
    "domaine": "https://admission.ivy-strategy.co",  # ex. "https://admission.ivy-strategy.co" : sert à l'aperçu WhatsApp (image + titre)
}

# Une entrée par école. « intro » = texte au-dessus des vidéos ; « temoignages » = liste
# de vidéos YouTube (id = ce qui suit youtu.be/). Liste vide = repère « à ajouter » affiché.
ECOLES = {
    "columbia": {"ecole": "Columbia", "logo": "columbia",
                 "intro": "Seth, ingénieur passé par la prépa et l'ESTP, raconte son admission en master à Columbia. Selma, étudiante à Columbia, partage son parcours avec Théotime, admis à Boston College : leur dossier, la vie de campus et leurs conseils.",
                 "temoignages": [{"yt": "xyZ81CK6IoM", "legende": "Seth, admis à Columbia"},
                                 {"yt": "4a3-3BXPFfo", "legende": "Selma (Columbia) et Théotime (Boston College)"}]},
    "princeton": {"ecole": "Princeton", "logo": "princeton",
                  "intro": "Kiara, 17 ans, a été admise à Princeton depuis la France. Elle détaille sa stratégie : ses notes dès la troisième, le SAT, ses essais, l'entretien d'admission et la bourse obtenue.",
                  "temoignages": [{"yt": "qKi9-4O5BEk", "legende": "Kiara, admise à Princeton"}]},
    "harvard": {"ecole": "Harvard", "logo": "harvard",
                "intro": "Deux parcours, deux façons d'y arriver depuis un lycée français : Salomé, diplômée de Harvard, et Stéphanie, aujourd'hui étudiante en génie mécanique.",
                "temoignages": [{"yt": "Lk7-jZFAiQU", "legende": "Salomé, diplômée de Harvard"},
                                {"yt": "dQZCuVhWYF8", "legende": "Stéphanie, étudiante à Harvard"}]},
    "yale": {"ecole": "Yale", "logo": "yale",
             "intro": "Chloé, 18 ans, est entrée à Yale après un bac français. Elle raconte sa méthode : le SAT, ses activités, ses essais et ses lettres de recommandation.",
             "temoignages": [{"yt": "kaiEOG0VBf4", "legende": "Chloé, étudiante à Yale"}]},
    # Autres écoles possibles (blasons déjà dans src/assets) : upenn, cornell, brown, dartmouth
    # "upenn": {"ecole": "UPenn", "logo": "upenn", "intro": None, "temoignages": []},
}

# Pages vidéo simples (titre + vidéo) à envoyer aux familles. Clé = adresse (/piliers/ ...).
VIDEOS = {
    "piliers":          {"titre": "Les 6 piliers d'un dossier admis",  "yt": "IOaZ134qCHU"},  # VSL 1, avant le R1
    "plans-b":          {"titre": "Les plans B de luxe",               "yt": "b8jjvQ4zTvk"},  # VSL 2, entre R1 et R2
    "plan-de-reussite": {"titre": "Présentation du plan de réussite",  "yt": "UYbjRTaa7lc"},  # VSL 3, entre R1 et R2
}

TODO = '<span class="todo">À AJOUTER</span>'


def video(yt, tag, attente):
    if yt:
        return f'<div class="video" data-yt="{yt}" data-tag="{tag}"></div>'
    return (f'<div class="video pending"><span class="play"><svg aria-hidden="true" width="28" height="28" '
            f'viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z" fill="#111111"/></svg></span>'
            f'<span>{attente}</span>{TODO}</div>')


def bloc_temoignages(e):
    if not e["temoignages"]:
        return video(None, "", f"Témoignage {e['ecole']} à venir")
    cartes = "".join(
        f'<div>{video(v["yt"], v["legende"], "")}<p class="caption">{v["legende"]}</p></div>'
        for v in e["temoignages"])
    return f'<div class="grid2">{cartes}</div>'


def intro(e):
    return e["intro"] or (f"Le témoignage d'un élève aujourd'hui à {e['ecole']} : "
                          "son parcours, ses doutes, et ce qui a fait la différence.")


def og_image(slug):
    if not COMMUN["domaine"]:
        return ""
    url = f'{COMMUN["domaine"].rstrip("/")}/{slug}/assets/apercu.jpg'
    return (f'<meta property="og:image" content="{url}">\n<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">')


ACCUEIL = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Les Stratèges · Espace d'admission</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@400&display=swap" rel="stylesheet">
</head><body style="margin:0;min-height:100vh;background:#111;color:#F7F4EC;font-family:Inter,Arial,sans-serif;display:flex;align-items:center;justify-content:center;text-align:center;padding:24px;box-sizing:border-box">
<div><img src="{slug}/assets/logo.png" alt="Les Stratèges" style="width:96px;height:96px">
<div style="font-family:Cinzel,Georgia,serif;font-weight:700;letter-spacing:6px;color:#C9A24D;margin:20px 0 12px">LES STRATÈGES</div>
<p style="color:#D9D4C7;font-size:17px;max-width:420px;margin:0 auto">Votre espace d'admission est personnel.<br>Utilisez le lien envoyé par votre chargé d'admission.</p>
</div></body></html>
"""


def main():
    src = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "index.html").write_text(ACCUEIL.replace("{slug}", next(iter(ECOLES))), encoding="utf-8")
    for slug, e in ECOLES.items():
        html = (src
                .replace("{{VIDEO_TEMOIGNAGE}}", bloc_temoignages(e))
                .replace("{{INTRO_TEMOIGNAGE}}", intro(e))
                .replace("{{OG_IMAGE}}", og_image(slug))
                .replace("{{ECOLE}}", e["ecole"])
                .replace("{{SLUG}}", e["logo"]))
        out = dist / slug
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(ROOT / "src" / "assets", out / "assets")
        (out / "index.html").write_text(html, encoding="utf-8")
        manque = [k for k, v in (("témoignage", e["temoignages"]),
                                  ("domaine (aperçu WhatsApp)", COMMUN["domaine"])) if not v]
        etat = "PRÊTE" if not manque else "manque : " + ", ".join(manque)
        print(f"{slug:10} -> dist/{slug}/index.html   {etat}")

    gabarit = (ROOT / "src" / "video.html").read_text(encoding="utf-8")
    for slug, v in VIDEOS.items():
        out = dist / slug
        if out.exists():
            shutil.rmtree(out)
        (out / "assets").mkdir(parents=True)
        for f in ("logo.png", "apercu.jpg", "player.js"):
            shutil.copy(ROOT / "src" / "assets" / f, out / "assets" / f)
        html = (gabarit.replace("{{OG_IMAGE}}", og_image(slug))
                .replace("{{TITRE}}", v["titre"]).replace("{{YT}}", v["yt"]))
        (out / "index.html").write_text(html, encoding="utf-8")
        print(f"{slug:16} -> dist/{slug}/index.html   vidéo : {v['titre']}")


if __name__ == "__main__":
    main()
