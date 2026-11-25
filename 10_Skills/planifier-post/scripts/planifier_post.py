#!/usr/bin/env python3
"""planifier_post : programme un post LinkedIn (ou un brouillon) sur Publora, avec les controles de bonnes pratiques,
puis tient le calendrier local 05_Departements/Marketing/Content-Brain/05_Calendrier-editorial/Calendrier.md.

Cle : PUBLORA_API_KEY dans .env (connecter-outils). Le compte LinkedIn est connecte dans le tableau de bord Publora
(OAuth), jamais par l'API. Abonnement Publora, aucun cout par appel (palier gratuit : 15 posts par mois).

Exemples :
  python3 planifier_post.py --comptes                              (les comptes connectes et leur etat)
  python3 planifier_post.py --test                                 (sante de la connexion LinkedIn)
  python3 planifier_post.py --post "05_Departements/Marketing/Content-Brain/05_Calendrier-editorial/Brouillons/Post-Signaux_2026-09-22.md" --quand "2026-09-23 08:00" --dry-run
  python3 planifier_post.py --post <fichier.md> --quand "2026-09-23 08:00" --premier-commentaire "Le guide complet : https://..."
  python3 planifier_post.py --texte "..." --brouillon              (un brouillon dans Publora, sans date)
  python3 planifier_post.py --post <fichier.md> --media carrousel.pdf --quand "2026-09-24 08:00"
  python3 planifier_post.py --liste --jours 14                     (ce qui est programme)
  python3 planifier_post.py --decaler <postGroupId> --quand "2026-09-25 08:00"
  python3 planifier_post.py --annuler <postGroupId>
  python3 planifier_post.py --commenter <postGroupId> --texte "..." (le premier commentaire, une fois le post publie)
  python3 planifier_post.py --stats <postGroupId>                  (impressions, portee, reactions, commentaires, partages)
Chaque action qui ecrit chez Publora s'annonce en --dry-run d'abord.
"""
from __future__ import annotations

import argparse
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

_racine = next((d for d in Path(__file__).resolve().parents if (d / "CLAUDE.md").exists() and (d / "10_Skills").is_dir()), None)
if _racine is None:
    sys.exit("Racine du workspace introuvable (CLAUDE.md + 10_Skills/) : ce script doit vivre dans 10_Skills/ de Superfounder OS.")
sys.path.insert(0, str(_racine / "10_Skills" / "_commun"))
from gtm_common import Publora, afficher, arret, bandeau_dry_run, racine  # noqa: E402

CALENDRIER = "05_Departements/Marketing/Content-Brain/05_Calendrier-editorial/Calendrier.md"
ENTETE = ("# Calendrier editorial\n\n## Par semaine\n\n<!-- calendrier:debut -->\nAucun post pour l'instant.\n<!-- calendrier:fin -->\n\n"
          "## Programmation\n\n> Tenu par `planifier-post` : une ligne par post programme sur Publora. "
          "Statut mis a jour par `--liste`. Heures locales.\n\n"
          "| Programme pour | Compte | Sujet ou fichier | postGroupId | Statut | Premier commentaire |\n|---|---|---|---|---|---|\n")
MAX_CARACTERES = 3000
HOOK_MAX = 210
DELAI_MIN_MINUTES = 15
CRENEAUX = {1: ((7, 30), (9, 30)), 2: ((7, 30), (9, 30)), 3: ((7, 30), (9, 30)), 0: ((8, 0), (9, 30)), 4: ((7, 30), (9, 0))}
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def jour_local(d: datetime) -> str:
    return f"{JOURS[d.weekday()]} {d.strftime('%d/%m/%Y %H:%M')}"


# ------------------------------------------------------------------ contenu

def contenu_depuis_fichier(chemin: Path) -> str:
    """Le texte du post : le bloc 'POST COMPLET' s'il existe, sinon le corps sans frontmatter."""
    t = chemin.read_text(encoding="utf-8")
    m = re.search(r"^##\s*(?:\S+\s+)?POST COMPLET[^\n]*\n(.*?)(?=^##\s|\Z)", t, re.M | re.S | re.I)
    if m:
        corps = m.group(1)
    else:
        corps = re.sub(r"\A---\n.*?\n---\n", "", t, count=1, flags=re.S)
        corps = re.sub(r"^#\s[^\n]*\n", "", corps, count=1)
    corps = re.sub(r"```[a-zA-Z]*\n(.*?)```", r"\1", corps, flags=re.S)
    return corps.strip()


def controler(contenu: str, quand_local: datetime | None) -> tuple[list[str], list[str]]:
    """(bloquants, avertissements) selon les bonnes pratiques du master linkedin."""
    bloquants, avert = [], []
    n = len(contenu)
    if not contenu.strip():
        bloquants.append("le post est vide")
    if n > MAX_CARACTERES:
        bloquants.append(f"{n} caracteres : LinkedIn en accepte {MAX_CARACTERES}")
    if chr(0x2014) in contenu or chr(0x2013) in contenu:
        bloquants.append("tiret cadratin ou demi-cadratin dans le texte (regle du workspace) : remplacez avant de programmer")
    hook = contenu.split("\n\n")[0].strip() if contenu.strip() else ""
    if len(hook) > HOOK_MAX:
        avert.append(f"les {len(hook)} premiers caracteres precedent le premier saut de paragraphe : au-dela de {HOOK_MAX}, le hook est coupe par \"voir plus\"")
    if re.search(r"https?://\S+", contenu):
        avert.append("un lien dans le corps du post reduit la portee : mettez-le en premier commentaire (--premier-commentaire) et ecrivez \"lien en commentaire\"")
    if contenu.lstrip().startswith("#"):
        avert.append("le post commence par un hashtag")
    emojis = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", contenu))
    if emojis > 3:
        avert.append(f"{emojis} emojis : le socle du master en conseille 0 ou 1")
    if n < 400 and quand_local is not None:
        avert.append(f"{n} caracteres : court pour un post texte (1 500 a 2 500 conseilles), normal pour un texte de carrousel")
    if quand_local is not None:
        fen = CRENEAUX.get(quand_local.weekday())
        hm = (quand_local.hour, quand_local.minute)
        if fen is None:
            avert.append("week-end : moins de concurrence mais moins de lecteurs B2B ; le samedi 9h-11h et le dimanche soir marchent le mieux")
        elif not (fen[0] <= hm <= fen[1]):
            avert.append(f"hors du creneau conseille ce jour-la ({fen[0][0]:02d}h{fen[0][1]:02d} a {fen[1][0]:02d}h{fen[1][1]:02d}, heure locale) ; mardi a jeudi 7h30-8h30 restent les meilleurs")
    return bloquants, avert


def parser_quand(texte: str, fuseau: str) -> datetime:
    t = texte.strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(t, fmt).replace(tzinfo=ZoneInfo(fuseau))
        except ValueError:
            continue
    arret(f"date illisible : {texte} (attendu AAAA-MM-JJ HH:MM, heure locale {fuseau})")


def vers_utc(d: datetime) -> str:
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_depuis_iso(iso: str | None, fuseau: str) -> str:
    if not iso:
        return "brouillon"
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ZoneInfo(fuseau))
        return f"{JOURS[d.weekday()][:3]} {d.strftime('%d/%m %H:%M')}"
    except ValueError:
        return iso


# ------------------------------------------------------------------ calendrier local

def ajouter_calendrier(quand: str, compte: str, sujet: str, pgid: str, statut: str, commentaire: str) -> None:
    p = racine() / CALENDRIER
    if not p.exists():
        p.write_text(ENTETE, encoding="utf-8")
    ligne = f"| {quand} | {compte} | {sujet} | {pgid} | {statut} | {(commentaire or '').replace('|', '/').replace(chr(10), ' ')[:120]} |\n"
    p.write_text(p.read_text(encoding="utf-8").rstrip("\n") + "\n" + ligne, encoding="utf-8")
    afficher(f"  [calendrier] ligne ajoutee dans {CALENDRIER}")


def maj_calendrier(statuts: dict[str, str]) -> None:
    p = racine() / CALENDRIER
    if not p.exists():
        return
    lignes, n = [], 0
    for l in p.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in l.split("|")]
        if l.startswith("|") and len(cells) >= 7 and cells[4] in statuts and cells[5] != statuts[cells[4]]:
            cells[5] = statuts[cells[4]]; l = "| " + " | ".join(cells[1:-1]) + " |"; n += 1
        lignes.append(l)
    if n:
        p.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        afficher(f"  [calendrier] {n} statut(s) mis a jour")


# ------------------------------------------------------------------ actions

def choisir_compte(pub: Publora, voulu: str | None) -> dict:
    comptes = pub.comptes_linkedin()
    if not comptes:
        arret("aucun compte LinkedIn connecte dans Publora : connectez-le dans le tableau de bord (Connections, LinkedIn), puis relancez")
    if voulu:
        for c in comptes:
            if c.get("platformId") == voulu or voulu.lower() in str(c.get("username", "")).lower() or voulu.lower() in str(c.get("displayName", "")).lower():
                return c
        arret(f"compte {voulu} introuvable parmi : " + ", ".join(f"{c.get('platformId')} ({c.get('displayName')})" for c in comptes))
    if len(comptes) > 1:
        arret("plusieurs comptes LinkedIn connectes, precisez --compte : " + ", ".join(f"{c.get('platformId')} ({c.get('displayName')})" for c in comptes))
    return comptes[0]


def collisions(pub: Publora, platform_id: str, quand: datetime, fuseau: str) -> list[str]:
    """Les posts deja programmes sur ce compte a moins de 20 heures de l'heure voulue."""
    try:
        rep = pub.lister(statut="scheduled", plateforme="linkedin", depuis=vers_utc(quand - timedelta(hours=20)), jusqu_a=vers_utc(quand + timedelta(hours=20)), limite=100)
    except RuntimeError as e:
        return [f"impossible de verifier les collisions ({e})"]
    out = []
    for p in rep.get("posts") or []:
        if any(pl.get("platformId") == platform_id for pl in p.get("platforms") or []) or not p.get("platforms"):
            out.append(f"deja programme le {local_depuis_iso(p.get('scheduledTime'), fuseau)} : {(p.get('content') or '')[:60]!r} ({p.get('postGroupId')})")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--comptes", action="store_true", help="lister les comptes connectes")
    g.add_argument("--test", action="store_true", help="tester la connexion LinkedIn")
    g.add_argument("--post", help="fichier .md du post (bloc POST COMPLET, ou corps sans frontmatter)")
    g.add_argument("--liste", action="store_true", help="les posts programmes (et mise a jour du calendrier local)")
    g.add_argument("--decaler", metavar="POSTGROUPID", help="changer la date d'un post programme (avec --quand)")
    g.add_argument("--annuler", metavar="POSTGROUPID", help="supprimer un post programme")
    g.add_argument("--voir", metavar="POSTGROUPID", help="detail et statut d'un post")
    g.add_argument("--commenter", metavar="POSTGROUPID", help="poster le premier commentaire d'un post publie (avec --texte)")
    g.add_argument("--stats", metavar="POSTGROUPID", help="statistiques LinkedIn d'un post publie")
    ap.add_argument("--texte", help="texte du post (au lieu de --post), ou du commentaire avec --commenter")
    ap.add_argument("--quand", help="date et heure locales, AAAA-MM-JJ HH:MM")
    ap.add_argument("--brouillon", action="store_true", help="creer un brouillon dans Publora, sans date")
    ap.add_argument("--compte", help="platformId ou nom du compte LinkedIn si plusieurs sont connectes")
    ap.add_argument("--media", action="append", help="image (jpg, png) ou PDF (carrousel) a joindre, repetable")
    ap.add_argument("--premier-commentaire", help="texte a poster en premier commentaire apres publication (note dans le calendrier)")
    ap.add_argument("--sujet", help="libelle pour le calendrier (defaut : nom du fichier)")
    ap.add_argument("--fuseau", default="Europe/Paris", help="fuseau des heures locales (defaut Europe/Paris)")
    ap.add_argument("--jours", type=int, default=14, help="avec --liste : fenetre en jours (defaut 14)")
    ap.add_argument("--force", action="store_true", help="programmer malgre les avertissements (jamais malgre un bloquant)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not any([a.comptes, a.test, a.post, a.texte, a.liste, a.decaler, a.annuler, a.voir, a.commenter, a.stats]):
        ap.print_help(); return
    pub = Publora(exiger_cle=not a.dry_run)

    if a.comptes:
        for c in pub.comptes():
            afficher(f"  {c.get('platformId')}  {c.get('displayName')} ({c.get('username')})  etat : {c.get('tokenStatus', '?')}  {c.get('profileUrl') or ''}")
        return
    if a.test:
        c = choisir_compte(pub, a.compte)
        r = pub.tester_compte(c["platformId"])
        afficher(f"  [{r.get('status', '?')}] {c.get('displayName')} : {r.get('message', '')} ; jeton : {r.get('tokenExpiresIn') or 'n/a'} ; dernier post reussi : {r.get('lastSuccessfulPost') or 'aucun'}")
        if r.get("lastError"):
            afficher(f"  derniere erreur : {r['lastError']}")
        return
    if a.liste:
        depuis = vers_utc(datetime.now(timezone.utc) - timedelta(days=1))
        jusqu_a = vers_utc(datetime.now(timezone.utc) + timedelta(days=a.jours))
        rep = pub.lister(plateforme="linkedin", depuis=depuis, jusqu_a=jusqu_a, limite=100)
        posts = rep.get("posts") or []
        if not posts:
            afficher(f"  aucun post LinkedIn dans les {a.jours} prochains jours")
        for p in posts:
            afficher(f"  {local_depuis_iso(p.get('scheduledTime'), a.fuseau):<16} {p.get('status', ''):<12} {p.get('postGroupId')}  {(p.get('content') or '')[:70]!r}")
        maj_calendrier({p.get("postGroupId"): p.get("status", "") for p in posts if p.get("postGroupId")})
        return
    if a.voir:
        p = pub.lire(a.voir)
        afficher(f"  statut {p.get('status')} ; programme {local_depuis_iso(p.get('scheduledTime'), a.fuseau)} ; comptes {p.get('platforms')}")
        for x in p.get("posts") or []:
            afficher(f"  - {x.get('platform')} {x.get('status')} postedId={x.get('postedId') or '-'} {x.get('permalink') or ''}")
        for m in p.get("media") or []:
            afficher(f"  - media {m.get('type')} {m.get('status')} {m.get('fileName') or ''}")
        return
    if a.annuler:
        if a.dry_run:
            bandeau_dry_run(f"Publora DELETE /delete-post/{a.annuler}", ["le post programme serait supprime"]); return
        pub.supprimer(a.annuler); afficher(f"  [ok] {a.annuler} supprime"); maj_calendrier({a.annuler: "annule"}); return
    if a.decaler:
        if not a.quand:
            arret("--decaler demande --quand")
        q = parser_quand(a.quand, a.fuseau)
        if q < datetime.now(timezone.utc) + timedelta(minutes=DELAI_MIN_MINUTES):
            arret(f"l'heure doit etre au moins {DELAI_MIN_MINUTES} minutes dans le futur")
        if a.dry_run:
            bandeau_dry_run(f"Publora PUT /update-post/{a.decaler}", [f"scheduledTime : {vers_utc(q)} (local {q.strftime('%d/%m %H:%M')})", "status : scheduled"]); return
        r = pub.modifier(a.decaler, scheduledTime=vers_utc(q), status="scheduled")
        afficher(f"  [ok] decale au {local_depuis_iso(r.get('scheduledTime') or vers_utc(q), a.fuseau)}"); return
    if a.commenter:
        if not a.texte:
            arret("--commenter demande --texte")
        p = pub.lire(a.commenter)
        cible = next((x for x in p.get("posts") or [] if x.get("platform") == "linkedin" and x.get("postedId")), None)
        if not cible:
            arret("ce post n'est pas encore publie sur LinkedIn (pas de postedId) : relancez apres la publication")
        pid = cible.get("platformId") or (p.get("platforms") or [""])[0]
        pid = pid if str(pid).startswith("linkedin") else f"linkedin-{pid}"
        if a.dry_run:
            bandeau_dry_run("Publora POST /linkedin-comments", [f"post : {cible.get('permalink') or cible.get('postedId')}", f"commentaire : {a.texte[:120]!r}"]); return
        pub.commenter_linkedin(pid, cible["postedId"], a.texte); afficher("  [ok] commentaire poste"); return
    if a.stats:
        p = pub.lire(a.stats)
        cible = next((x for x in p.get("posts") or [] if x.get("platform") == "linkedin" and x.get("postedId")), None)
        if not cible:
            arret("post non publie : pas de statistiques")
        pid = cible.get("platformId") or (p.get("platforms") or [""])[0]
        pid = pid if str(pid).startswith("linkedin") else f"linkedin-{pid}"
        m = pub.stats_post_linkedin(pid, cible["postedId"])
        afficher(f"  impressions {m.get('IMPRESSION', '?')} ; personnes atteintes {m.get('MEMBERS_REACHED', '?')} ; reactions {m.get('REACTION', '?')} ; commentaires {m.get('COMMENT', '?')} ; partages {m.get('RESHARE', '?')}")
        return

    # ---- programmer ou brouillon
    if a.post:
        chemin = Path(a.post)
        if not chemin.is_absolute():
            chemin = racine() / chemin if not chemin.exists() else chemin
        if not chemin.exists():
            arret(f"fichier introuvable : {a.post}")
        contenu, sujet = contenu_depuis_fichier(chemin), a.sujet or chemin.stem
    else:
        contenu, sujet = a.texte.strip(), a.sujet or a.texte.strip()[:40]
    if not a.brouillon and not a.quand:
        arret("donnez --quand \"AAAA-MM-JJ HH:MM\" (heure locale) ou --brouillon")
    quand = None if a.brouillon else parser_quand(a.quand, a.fuseau)
    if quand and quand < datetime.now(timezone.utc) + timedelta(minutes=DELAI_MIN_MINUTES):
        arret(f"l'heure doit etre au moins {DELAI_MIN_MINUTES} minutes dans le futur (Publora ramene une heure passee a maintenant)")
    bloquants, avert = controler(contenu, quand)
    medias = [Path(m) for m in (a.media or [])]
    for m in medias:
        if not m.exists():
            arret(f"media introuvable : {m}")
        if m.suffix.lower() not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".mp4", ".mov"):
            bloquants.append(f"media non pris en charge : {m.name} (image, PDF ou video)")
    for b in bloquants:
        afficher(f"  [bloquant] {b}")
    for w in avert:
        afficher(f"  [attention] {w}")
    if bloquants:
        arret("corrigez les points bloquants avant de programmer")
    if a.dry_run:
        lignes = [f"compte : {a.compte or 'le compte LinkedIn connecte'}", f"sujet : {sujet}",
                  f"quand : {'brouillon' if not quand else jour_local(quand) + ' (' + a.fuseau + ', soit ' + vers_utc(quand) + ')'}",
                  f"texte : {len(contenu)} caracteres, hook : {contenu.split(chr(10)+chr(10))[0][:80]!r}"]
        if medias:
            lignes.append("medias : " + ", ".join(m.name for m in medias) + " (brouillon, televersement, puis programmation)")
        if a.premier_commentaire:
            lignes.append(f"premier commentaire (a poster apres publication avec --commenter) : {a.premier_commentaire[:80]!r}")
        lignes.append("cout : aucun par appel (abonnement Publora ; palier gratuit 15 posts par mois)")
        if avert and not a.force:
            lignes.append(f"{len(avert)} avertissement(s) ci-dessus : corrigez, ou relancez avec --force")
        bandeau_dry_run("Publora POST /create-post" + (" + get-upload-url + update-post" if medias else ""), lignes)
        return
    if avert and not a.force:
        arret(f"{len(avert)} avertissement(s) : corrigez le post, ou relancez avec --force pour programmer quand meme")
    compte = choisir_compte(pub, a.compte)
    pid = compte["platformId"]
    if quand:
        for c in collisions(pub, pid, quand, a.fuseau):
            afficher(f"  [attention] {c}")
    if medias:
        rep = pub.creer(contenu, [pid], None, idempotence=str(uuid.uuid4()))
        pgid = rep.get("postGroupId")
        afficher(f"  [ok] brouillon {pgid} cree")
        for m in medias:
            r = pub.televerser(pgid, m, "document" if m.suffix.lower() == ".pdf" else None)
            afficher(f"  [ok] {m.name} televerse (media {r.get('mediaId')})")
        if quand:
            rep = pub.modifier(pgid, scheduledTime=vers_utc(quand), status="scheduled")
    else:
        rep = pub.creer(contenu, [pid], vers_utc(quand) if quand else None, idempotence=str(uuid.uuid4()))
        pgid = rep.get("postGroupId")
    for w in rep.get("warnings") or []:
        afficher(f"  [avertissement Publora] {w.get('code')} : {w.get('message', '')}")
    effectif = rep.get("scheduledTime")
    statut = "scheduled" if quand else "draft"
    afficher(f"  [ok] {statut} {pgid} pour {local_depuis_iso(effectif, a.fuseau) if effectif else 'brouillon'} sur {compte.get('displayName')}")
    ajouter_calendrier(quand.strftime("%Y-%m-%d %H:%M") if quand else "brouillon", compte.get("displayName") or pid, sujet, pgid or "?", statut, a.premier_commentaire or "")
    if a.premier_commentaire:
        afficher(f"  [a faire] apres la publication : planifier_post.py --commenter {pgid} --texte \"...\" (le texte est dans le calendrier)")


if __name__ == "__main__":
    main()
