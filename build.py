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
    "fiche_video_yt": None,   # vidéo de Léa sur la fiche point en famille (YouTube)
    "fiche_video_loom": None, # ou lien Loom embed (https://www.loom.com/embed/...)
    "cga_pdf": None,          # nom du PDF des conditions générales posé dans src/assets/
}

# Une entrée par témoignage reçu. temoignage_yt = identifiant YouTube (youtu.be/<id>).
ECOLES = {
    "columbia":  {"ecole": "Columbia",  "logo": "columbia",  "temoignage_yt": None},
    "princeton": {"ecole": "Princeton", "logo": "princeton", "temoignage_yt": None},
    "harvard":   {"ecole": "Harvard",   "logo": "harvard",   "temoignage_yt": None},
    "yale":      {"ecole": "Yale",      "logo": "yale",      "temoignage_yt": None},
    # Autres écoles possibles (blasons déjà dans src/assets) :
    # "upenn":     {"ecole": "UPenn",     "logo": "upenn",     "temoignage_yt": None},
    # "cornell":   {"ecole": "Cornell",   "logo": "cornell",   "temoignage_yt": None},
    # "brown":     {"ecole": "Brown",     "logo": "brown",     "temoignage_yt": None},
    # "dartmouth": {"ecole": "Dartmouth", "logo": "dartmouth", "temoignage_yt": None},
}

TODO = '<span class="todo">À AJOUTER</span>'


def video(yt, tag, attente):
    if yt:
        return f'<div class="video" data-yt="{yt}" data-tag="{tag}"></div>'
    return (f'<div class="video pending"><span class="play"><svg aria-hidden="true" width="28" height="28" '
            f'viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z" fill="#111111"/></svg></span>'
            f'<span>{attente}</span>{TODO}</div>')


def video_fiche():
    if COMMUN["fiche_video_yt"]:
        return video(COMMUN["fiche_video_yt"], "Votre point en famille", "")
    if COMMUN["fiche_video_loom"]:
        return (f'<div class="video"><iframe src="{COMMUN["fiche_video_loom"]}" title="Votre point en famille" '
                f'allow="fullscreen" allowfullscreen></iframe></div>')
    return video(None, "", "Vidéo de Léa sur la fiche, en cours de tournage")


def bouton_cga():
    svg = ('<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C9A24D" '
           'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v11"/>'
           '<path d="M7 10l5 5 5-5"/><path d="M5 20h14"/></svg>')
    label = "Télécharger les conditions générales d'admission (PDF)"
    if COMMUN["cga_pdf"]:
        return f'<a class="btn" href="assets/{COMMUN["cga_pdf"]}" download>{svg}{label}</a>'
    return f'<div><a class="btn" aria-disabled="true">{svg}{label}</a>{TODO}</div>'


def main():
    src = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
    dist = ROOT / "dist"
    for slug, e in ECOLES.items():
        html = (src
                .replace("{{VIDEO_FICHE}}", video_fiche())
                .replace("{{BOUTON_CGA}}", bouton_cga())
                .replace("{{VIDEO_TEMOIGNAGE}}", video(e["temoignage_yt"], f"Témoignage · {e['ecole']}",
                                                       f"Témoignage {e['ecole']} à venir"))
                .replace("{{ECOLE}}", e["ecole"])
                .replace("{{SLUG}}", e["logo"]))
        out = dist / slug
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(ROOT / "src" / "assets", out / "assets")
        (out / "index.html").write_text(html, encoding="utf-8")
        manque = [k for k, v in (("témoignage", e["temoignage_yt"]),
                                  ("vidéo fiche", COMMUN["fiche_video_yt"] or COMMUN["fiche_video_loom"]),
                                  ("PDF conditions générales", COMMUN["cga_pdf"])) if not v]
        etat = "PRÊTE" if not manque else "manque : " + ", ".join(manque)
        print(f"{slug:10} -> dist/{slug}/index.html   {etat}")


if __name__ == "__main__":
    main()
