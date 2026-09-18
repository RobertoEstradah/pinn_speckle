# -*- coding: utf-8 -*-
"""Compara cada cifra del paper contra la tesis, que es el documento base.

La tesis proviene de los resultados de los notebooks y de las citas con copia
local, y su contenido esta verificado por verifica_cifras_tesis.py. El paper
deriva de ella: si discrepan, la tesis manda.

Uso:
    python scripts/experiments/verifica_paper_vs_tesis.py
"""

import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

R = pathlib.Path(r"C:\roberto\Tesis_Maestria")
TESIS = R / "tesis" / "Tesis_Actual"
PAPER_ES = R / "paper" / "papers_plantillas" / "CyS" / "fuente" / "es"
PAPER_EN = R / "paper" / "papers_plantillas" / "CyS" / "fuente" / "en"
PAPER_COMIA = R / "paper" / "papers_plantillas" / "COMIA" / "fuente"

ok = fallo = 0


def chk(etiqueta, esperado, real, nota=""):
    global ok, fallo
    bien = esperado == real
    marca = "OK   " if bien else "FALLA"
    print(f"  {marca} {etiqueta:<44} tesis={str(esperado):<12} paper={real}"
          + (f"   {nota}" if nota and not bien else ""))
    ok, fallo = ok + bien, fallo + (not bien)


def texto(carpeta):
    partes = []
    for f in sorted(carpeta.glob("*.tex")) + sorted((carpeta / "sections").glob("*.tex")):
        partes.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(partes)


def busca(t, patron):
    """Devuelve el primer grupo capturado, o None."""
    m = re.search(patron, t)
    return m.group(1) if m else None


def titulo_de(t):
    """Extrae el contenido de \\title{...} en texto plano, o None.

    No basta con un [^}]* : COMIA escribe los acentos como \\'{o}, y un
    patron asi se detendria en la primera llave interna, devolviendo doce
    caracteres. Las guardas del titulo pasarian entonces en vacio, sin mirar
    nada. Hay que equilibrar llaves y luego quitar los escapes.
    """
    i = t.find(r"\title{")
    if i < 0:
        return None
    j, nivel = i + len(r"\title{"), 1
    while j < len(t) and nivel:
        nivel += (t[j] == "{") - (t[j] == "}")
        j += 1
    crudo = t[i + len(r"\title{"):j - 1]
    crudo = crudo.split(r"\thanks")[0]          # el agradecimiento no es titulo
    crudo = re.sub(r"\\[`'^\"~=.]\{(\w)\}", r"\1", crudo)   # \'{o} -> o
    crudo = re.sub(r"\\[`'^\"~=.](\w)", r"\1", crudo)       # \'o   -> o
    return re.sub(r"[%\s]+", " ", crudo).strip()


t_tesis = texto(TESIS) + "\n".join(
    f.read_text(encoding="utf-8", errors="replace")
    for f in (TESIS / "chapters").glob("*.tex"))

for etiqueta_idioma, carpeta in (("CyS ESPAÑOL", PAPER_ES),
                                 ("CyS INGLÉS", PAPER_EN),
                                 ("COMIA", PAPER_COMIA)):
    print(f"\n=== {etiqueta_idioma} ===")
    t = texto(carpeta)

    # ── cifras que deben coincidir literalmente con la tesis ───────────────
    for nombre, patron_paper, valor_tesis in (
            ("L2 1D (%)", r"0\.006", "0.006"),
            ("L2 2D promedio (%)", r"0\.171", "0.171"),
            ("L2 2D real (%)", r"0\.214", "0.214"),
            ("L2 2D imag (%)", r"0\.127", "0.127"),
            ("multisemilla media", r"0\.192", "0.192"),
            ("multisemilla desviacion", r"0\.089", "0.089"),
            ("ablacion d=64 (%)", r"0\.436", "0.436"),
    ):
        presente = re.search(patron_paper, t) is not None
        chk(f"{nombre} presente y coincide", True, presente)

    # ── el coeficiente de variacion: la tesis dice 46 % ────────────────────
    # Acepta las formas "del $46\%$ respecto a la media" y "of $46\%$ about
    # the mean", ademas de la antigua "N\% relativo".
    cv = busca(t, r"(?:coeficiente de variación|coefficient of variation)"
                  r"[^.]{0,40}?(\d+)\s*\\%")
    if cv is None:
        cv = busca(t, r"(\d+)\s*\\%\$?\s*(?:relativo|relative)")
    chk("coeficiente de variacion", "46", cv,
        "la tesis dice 46 % (0.089/0.192); ver Cap4")

    # Guarda: la afirmacion obsoleta del 13 % no debe reaparecer en ninguna
    # version, ni en el cuerpo ni en los resumenes en el otro idioma.
    obsoleta = bool(re.search(r"13\s*\\%\$?\s*(?:relativo|relative)", t)) or \
        bool(re.search(r"(?:varianza|variance)[^.]{0,40}13\s*\\%", t, re.I))
    chk("no reaparece el 13 % obsoleto", False, obsoleta,
        "cifra retirada: el coeficiente de variacion es 46 %, no 13 %")

    # Y 'variance' no debe usarse para lo que es un coeficiente de variacion.
    mal_nombrado = bool(re.search(r"(?:variance|varianza)\s+of\s+\$?\d+\s*\\%", t, re.I))
    chk("no llama 'variance' al coeficiente", False, mal_nombrado,
        "0.089 es desviacion estandar; 46 % es coeficiente de variacion")

    # El paper SI puede mencionar el speckle como trabajo futuro o citar la
    # validacion estadistica de la tesis; lo que no debe es prometerlo en el
    # titulo, que es lo que el lector lee primero.
    titulo = titulo_de(t)

    # Meta-guarda: si el titulo no se lee entero, las dos comprobaciones de
    # abajo pasan en vacio y no vigilan nada. Esto ocurrio de verdad con los
    # acentos escapados de COMIA: se leian doce caracteres y parecia correcto.
    chk("el titulo se pudo leer entero", True, bool(titulo) and len(titulo) > 30,
        f"leido: {titulo!r}")

    dice_acelerada = bool(titulo and re.search(r"acelerad|accelerat", titulo, re.I))
    chk("el titulo no promete aceleracion", False, dice_acelerada,
        "no se mide ningun factor de aceleracion en este paper")

    dice_speckle = bool(titulo and re.search(r"speckle", titulo, re.I))
    chk("el titulo no promete speckle", False, dice_speckle,
        "el speckle aparece solo como trabajo futuro")

print(f"\n==== {ok} verificadas, {fallo} discrepancias ====")
if fallo:
    print("\nLa tesis es el documento base. Donde el paper discrepe, se corrige")
    print("el paper, no la tesis.")
