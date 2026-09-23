# -*- coding: utf-8 -*-
"""Gabarits HTML pour infographies 1080x1350, pilotes par les jetons de la charte de l'utilisateur.

Chaque gabarit est une fonction (data: dict, t: dict) -> str HTML complet. `data` vient de data.json
(voir ressources/format-donnees.md), `t` est le dictionnaire de jetons construit par rendre_infographie.py
depuis 03_Branding/charte-visuelle.md : fond, carte, bloc, texte, gris, accent, cta, cta_texte, bloc_texte,
bloc_legende, ligne, ligne_carte, font_titres, font_corps, font_mono, fonts_css, logo.
"""
import html as _html


def e(s):
    return _html.escape(str(s or ""), quote=False)


def base_css(t, densite="normal"):
    k = 0.9 if densite == "serre" else 1.0
    return f"""
{t['fonts_css']}
:root{{--fond:{t['fond']};--carte:{t['carte']};--bloc:{t['bloc']};--texte:{t['texte']};--gris:{t['gris']};
--accent:{t['accent']};--cta:{t['cta']};--cta-texte:{t['cta_texte']};--bloc-texte:{t['bloc_texte']};--bloc-legende:{t['bloc_legende']};
--ligne:{t['ligne']};--ligne-carte:{t['ligne_carte']};--k:{k}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{background:var(--fond);color:var(--gris);font-family:{t['font_corps']};-webkit-font-smoothing:antialiased;font-size:calc(16px*var(--k))}}
.page{{position:relative;width:1080px;height:1350px;padding:56px 56px 48px;display:flex;flex-direction:column}}
.label{{font-family:{t['font_mono']};font-weight:500;font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:var(--gris)}}
h1,h2,.name,.core-t{{font-family:{t['font_titres']};font-weight:700}}
h1{{color:var(--texte);letter-spacing:-.03em;line-height:1.02;font-size:calc(60px*var(--k));margin:14px 0 12px}}
.mark{{color:var(--accent)}} .mkj{{color:var(--cta)}}
.sub{{font-size:calc(21px*var(--k));line-height:1.4;max-width:840px;margin-bottom:calc(26px*var(--k))}}
.mono,.num,.cmd{{font-family:{t['font_mono']};font-weight:500}}
.carte{{background:var(--carte);border-radius:20px}}
.num{{font-size:13px;letter-spacing:.16em;color:var(--gris)}}
.cmd{{color:var(--accent);font-size:12.5px}}
.name{{color:var(--texte);letter-spacing:-.02em;line-height:1.08}}
.desc{{line-height:1.38}}
.q{{font-style:italic;color:var(--texte);line-height:1.35}}
.footer{{margin-top:auto;padding-top:20px;display:flex;align-items:center;justify-content:space-between;min-height:48px}}
.btn{{display:inline-flex;align-items:center;font-family:{t['font_titres']};font-weight:700;font-size:18px;padding:15px 28px;border-radius:999px;
background:var(--cta);color:var(--cta-texte);white-space:nowrap}}
.logo img{{height:40px;display:block}}
.bloc{{background:var(--bloc);color:var(--bloc-texte);border-radius:22px}}
.bloc .name,.bloc h2,.bloc .core-t,.bloc .q{{color:var(--bloc-texte)}} .bloc .desc,.bloc .num,.bloc .label{{color:var(--bloc-legende)}}
"""


def head(d):
    t, a = e(d.get("titre", "")), e(d.get("accent", ""))
    if a:
        titre = (f'<span class="mark">{a}</span><br>{t}' if d.get("accent_position") == "debut" else f'{t}<br><span class="mark">{a}</span>')
    else:
        titre = t
    out = f'<div class="label">{e(d.get("label", ""))}</div><h1>{titre}</h1>'
    if d.get("sous_titre"):
        out += f'<p class="sub">{e(d["sous_titre"])}</p>'
    return out


def footer(d, t):
    logo = f'<div class="logo"><img src="{t["logo"]}" alt=""></div>' if t.get("logo") else "<div></div>"
    cta = f'<div class="btn">{e(d["cta"])}</div>' if d.get("cta") else ""
    return f'<div class="footer">{logo}{cta}</div>'


def page(d, t, body, css):
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{e(d.get("titre"))}</title>'
            f'<style>{base_css(t, d.get("densite", "normal"))}{css}</style></head><body><div class="page">{body}</div></body></html>')


def by_id(d):
    return {it["id"]: it for it in d["items"]}


def grille(d, t):
    n = len(d["items"])
    cols = 2 if n <= 6 else 3
    cards = "".join(f"""<div class="carte c"><div class="top"><span class="num">{e(it['id'])}</span><span class="cmd">{e(it.get('meta',''))}</span></div>
<div class="name">{e(it['nom'])}</div><p class="desc">{e(it.get('desc',''))}</p>{('<p class="q">« '+e(it['cite'])+' »</p>') if it.get('cite') else ''}</div>""" for it in d["items"])
    css = f""".grid{{display:grid;grid-template-columns:repeat({cols},1fr);grid-auto-rows:1fr;gap:16px;flex:1}}
.c{{padding:calc(22px*var(--k)) 22px 20px;display:flex;flex-direction:column}}.top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}}
.name{{font-size:calc({24 if cols == 3 else 28}px*var(--k));margin-bottom:10px}}.desc{{font-size:calc({15.5 if cols == 3 else 17}px*var(--k));flex:1}}
.q{{font-size:calc(15px*var(--k));margin-top:12px;padding-top:12px;border-top:1.5px solid var(--ligne-carte)}}"""
    return page(d, t, head(d) + f'<div class="grid">{cards}</div>' + footer(d, t), css)


def glossaire(d, t):
    cols = d.get("colonnes") or ["Le terme", "Ce que c'est", "Comment l'utiliser"]
    rows = "".join(f"""<div class="row"><div><span class="num">{e(it['id'])}</span><div class="name">{e(it['nom'])}</div><div class="cmd">{e(it.get('meta',''))}</div></div>
<div class="desc">{e(it.get('desc',''))}</div><div class="q">{('« '+e(it['cite'])+' »') if it.get('cite') else ''}</div></div>""" for it in d["items"])
    thead = "".join(f"<span>{e(c)}</span>" for c in cols)
    css = """h1{font-size:calc(54px*var(--k))}.thead,.row{display:grid;grid-template-columns:260px 1fr 330px;gap:22px}
.thead{padding-bottom:10px;border-bottom:1.5px solid var(--ligne);margin-top:6px}.thead span{font-family:inherit;font-size:12px;letter-spacing:.18em;text-transform:uppercase}
.list{flex:1;display:flex;flex-direction:column}.row{align-items:center;padding:7px 0;border-bottom:1.5px solid var(--ligne);flex:1}.row:last-child{border-bottom:none}
.row .name{font-size:calc(20px*var(--k));margin:4px 0}.row .desc,.row .q{font-size:calc(15px*var(--k))}"""
    return page(d, t, head(d) + f'<div class="thead label">{thead}</div><div class="list">{rows}</div>' + footer(d, t), css)


def systeme(d, t):
    by = by_id(d)
    fams = ""
    for g in d["groupes"]:
        its = "".join(f"""<div class="it"><div class="itop"><span class="num">{e(by[k]['id'])}</span><span class="cmd">{e(by[k].get('meta',''))}</span></div>
<div class="name">{e(by[k]['nom'])}</div><p class="desc">{e(by[k].get('desc',''))}</p></div>""" for k in g["ids"])
        fams += f'<div class="carte fam"><div class="fhead"><span class="label">{e(g.get("sous",""))}</span><h2>{e(g["nom"])}</h2></div>{its}</div>'
    c = d.get("coeur")
    core = ""
    if c:
        texte = e(c.get("texte", "")).replace("{accent}", f'<span class="mkj">{e(c.get("accent",""))}</span>')
        chiffres = "".join(f'<div><span class="mono">{e(v)}</span> {e(u)}</div>' for v, u in c.get("chiffres", []))
        core = f"""<div class="bloc core"><div class="label">{e(c.get('label',''))}</div><div class="core-t">{e(c.get('titre',''))}</div>
<p class="core-p">{texte}</p><div class="core-n">{chiffres}</div></div>"""
    css = f""".wrap{{display:grid;grid-template-columns:{'1fr 250px' if c else '1fr'};gap:16px;flex:1;min-height:0}}
.fams{{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:16px}}.fam{{padding:22px 22px 14px;display:flex;flex-direction:column;justify-content:space-between}}
.fhead{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px;padding-bottom:10px;border-bottom:1.5px solid var(--ligne-carte)}}
.fhead h2{{font-size:calc(30px*var(--k));letter-spacing:-.03em;color:var(--texte)}}.it{{padding:10px 0}}.itop{{display:flex;justify-content:space-between;align-items:baseline}}
.it .name{{font-size:calc(21px*var(--k));margin:2px 0 3px}}.desc{{font-size:calc(15.5px*var(--k))}}
.core{{padding:26px 24px;display:flex;flex-direction:column}}.core-t{{font-size:44px;letter-spacing:-.03em;line-height:1;margin:14px 0 18px}}
.core-p{{font-size:17px;line-height:1.45;color:var(--bloc-texte);flex:1}}.core-n{{font-size:15px;color:var(--bloc-legende);line-height:1.5;border-top:1.5px solid var(--bloc-legende);padding-top:16px}}
.core-n .mono{{color:var(--bloc-texte);font-size:26px;margin-right:6px}}"""
    return page(d, t, head(d) + f'<div class="wrap"><div class="fams">{fams}</div>{core}</div>' + footer(d, t), css)


def etapes(d, t):
    rows = "".join(f"""<div class="carte st"><div class="stn"><span class="big mono">{e(it['id'])}</span><span class="cmd">{e(it.get('meta',''))}</span></div>
<div><div class="name">{e(it['nom'])}</div><p class="desc">{e(it.get('desc',''))}</p>{('<p class="q">« '+e(it['cite'])+' »</p>') if it.get('cite') else ''}</div></div>""" for it in d["items"])
    css = """.steps{display:flex;flex-direction:column;gap:14px;flex:1}.st{flex:1;display:grid;grid-template-columns:120px 1fr;gap:20px;padding:22px 26px;align-items:start}
.stn{display:flex;flex-direction:column;gap:6px}.big{font-size:40px;color:var(--accent);line-height:1}
.st .name{font-size:calc(26px*var(--k));margin-bottom:8px}.st .desc{font-size:calc(17px*var(--k))}.st .q{font-size:calc(15.5px*var(--k));margin-top:8px}"""
    return page(d, t, head(d) + f'<div class="steps">{rows}</div>' + footer(d, t), css)


def comparatif(d, t):
    cp = d.get("comparatif") or {"gauche": "Avant", "droite": "Maintenant"}
    g = [it for it in d["items"] if it.get("cote", "gauche") == "gauche"]
    r = [it for it in d["items"] if it.get("cote") == "droite"]

    def col(items, title, cls):
        its = "".join(f'<div class="it"><span class="num">{e(it["id"])}</span><div class="name">{e(it["nom"])}</div><p class="desc">{e(it.get("desc",""))}</p></div>' for it in items)
        return f'<div class="{cls} col"><h2>{e(title)}</h2>{its}</div>'
    css = """.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1}.col{padding:24px;display:flex;flex-direction:column}
.col h2{font-size:calc(30px*var(--k));letter-spacing:-.03em;margin-bottom:8px;padding-bottom:12px;border-bottom:1.5px solid var(--ligne-carte);color:var(--texte)}
.bloc.col h2{border-color:var(--bloc-legende)}.it{padding:12px 0;flex:1}.it .name{font-size:calc(21px*var(--k));margin:3px 0 4px}.desc{font-size:calc(15.5px*var(--k))}"""
    return page(d, t, head(d) + f'<div class="cols">{col(g, cp["gauche"], "carte")}{col(r, cp["droite"], "bloc")}</div>' + footer(d, t), css)


def pyramide(d, t):
    niveaux = d["niveaux"]
    n = len(niveaux)
    layers = ""
    for i, lvl in enumerate(reversed(niveaux)):
        its = [it for it in d["items"] if it.get("tier") == lvl]
        width = 100 - (n - 1 - i) * (40 / max(n - 1, 1))
        cls = "bloc" if i == 0 else "carte"
        body = "".join(f'<div class="it"><div class="name">{e(it["nom"])}</div><p class="desc">{e(it.get("desc",""))}</p></div>' for it in its)
        layers += f'<div class="{cls} lay" style="width:{width}%"><div class="lh"><span class="label">{e(f"Niveau {n - i:02d}")}</span><h2>{e(lvl)}</h2></div><div class="its">{body}</div></div>'
    css = """.pyr{display:flex;flex-direction:column;align-items:center;gap:12px;flex:1}.lay{padding:20px 26px;flex:1;display:grid;grid-template-columns:220px 1fr;gap:20px;align-items:center}
.lh h2{font-size:calc(28px*var(--k));letter-spacing:-.03em;color:var(--texte)}.its{display:flex;gap:18px}.it{flex:1}.it .name{font-size:calc(19px*var(--k));margin-bottom:4px}.desc{font-size:calc(14.5px*var(--k))}"""
    return page(d, t, head(d) + f'<div class="pyr">{layers}</div>' + footer(d, t), css)


def funnel(d, t):
    n = len(d["items"])
    stages = ""
    for i, it in enumerate(d["items"]):
        width = 100 - i * (34 / max(n - 1, 1))
        cls = "bloc" if i == n - 1 else "carte"
        stages += f"""<div class="{cls} stg" style="width:{width}%"><div class="sl"><span class="num">{e(it['id'])}</span><h2>{e(it['nom'])}</h2><span class="cmd">{e(it.get('meta',''))}</span></div>
<div class="sr"><p class="desc">{e(it.get('desc',''))}</p>{('<p class="q">'+e(it['cite'])+'</p>') if it.get('cite') else ''}</div></div>"""
    css = """.fun{display:flex;flex-direction:column;align-items:center;gap:12px;flex:1}.stg{padding:20px 26px;flex:1;display:grid;grid-template-columns:230px 1fr;gap:20px;align-items:center}
.sl h2{font-size:calc(28px*var(--k));letter-spacing:-.03em;color:var(--texte);margin:4px 0}.bloc .cmd{color:var(--cta)}
.desc{font-size:calc(15.5px*var(--k))}.q{font-size:calc(14.5px*var(--k));margin-top:6px;font-style:normal}"""
    return page(d, t, head(d) + f'<div class="fun">{stages}</div>' + footer(d, t), css)


def tierlist(d, t):
    rows = ""
    for i, lvl in enumerate(d["niveaux"]):
        its = [it for it in d["items"] if it.get("tier") == lvl]
        cls = "bloc" if i == 0 else "carte"
        chips = "".join(f'<div class="chip"><div class="name">{e(it["nom"])}</div>{("<p class=desc>" + e(it["desc"]) + "</p>") if it.get("desc") else ""}</div>' for it in its)
        rows += f'<div class="{cls} tr"><div class="tl"><span class="label">{e(f"Rang {i + 1:02d}")}</span><h2>{e(lvl)}</h2></div><div class="chips">{chips}</div></div>'
    css = """.tiers{display:flex;flex-direction:column;gap:12px;flex:1}.tr{padding:18px 24px;flex:1;display:grid;grid-template-columns:200px 1fr;gap:18px;align-items:center}
.tl h2{font-size:calc(28px*var(--k));letter-spacing:-.03em;color:var(--texte);margin-top:4px}.chips{display:flex;flex-wrap:wrap;gap:10px 22px}.chip{min-width:180px;flex:1}
.chip .name{font-size:calc(18px*var(--k))}.chip .desc{font-size:calc(13.5px*var(--k))}"""
    return page(d, t, head(d) + f'<div class="tiers">{rows}</div>' + footer(d, t), css)


GABARITS = {"grille": grille, "glossaire": glossaire, "systeme": systeme, "etapes": etapes,
            "comparatif": comparatif, "pyramide": pyramide, "funnel": funnel, "tierlist": tierlist}
