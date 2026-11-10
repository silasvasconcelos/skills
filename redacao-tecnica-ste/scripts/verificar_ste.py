#!/usr/bin/env python3
"""Verificador de redação técnica STE em português brasileiro.

Analisa arquivos Markdown ou texto e informa violações das regras da skill
redacao-tecnica-ste. As verificações são heurísticas: cada AVISO exige
análise humana ou do agente. Código, tabelas, títulos e texto entre aspas
não passam pela verificação de termos.

Uso:
    python3 verificar_ste.py documento.md [outro.md pasta/ ...]
    python3 verificar_ste.py - < documento.md
    python3 verificar_ste.py --help

Códigos de saída:
    0  nenhum ERRO (ou nenhum AVISO com --estrito)
    1  há ERRO (ou AVISO com --estrito)
    2  erro de uso ou de leitura de arquivo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple

ERRO = "ERRO"
AVISO = "AVISO"
EXTENSOES = {".md", ".markdown", ".txt"}

# (padrão, sugestão, regra, severidade). Mantenha em sincronia com DICIONARIO.md.
TERMOS_NAO_APROVADOS: List[Tuple[str, str, str, str]] = [
    (r"\butiliz\w*", "use 'usar'", "R1.5", ERRO),
    (r"\bposs(?:ui|uem|uir|uía|uíam|uirá|ua|uam)\b", "use 'ter'", "R1.5", ERRO),
    (r"\befetu\w*", "use o verbo da ação", "R2.3", ERRO),
    (r"\bproced\w*\s+(?:com|à|ao)\b", "use o verbo da ação", "R2.3", ERRO),
    (r"\bencontra(?:m)?-se\b|\bse\s+encontra(?:m)?\b", "use 'está' ou 'fica'", "R1.5", ERRO),
    (r"\bdisponibiliz\w*", "use 'oferecer' ou 'publicar'", "R1.5", AVISO),
    (r"\bviabiliz\w*", "use 'permitir'", "R1.5", AVISO),
    (r"\b(?:deverá|deverão|poderá|poderão)\b", "use 'deve' ou 'pode'", "R3.4", ERRO),
    (r"\b(?:é|será)\s+necessário\s+que\b|\bfaz-se\s+necessário\b|\bse\s+faz\s+necessário\b",
     "use 'deve' ou o imperativo", "R3.4", ERRO),
    (r"\b(?:vou|vai|vamos|vão|irá|irão|estarei|estará|estaremos|estarão)\s+estar\s+\w+ndo\b",
     "gerundismo: use o presente ou o futuro do presente", "R3.3", ERRO),
    (r"\bdelet\w*", "use 'excluir'", "R1.7", ERRO),
    (r"\bset(?:ar|ou|ado|ada|ados|adas|ando|amos)\b", "use 'definir' ou 'configurar'", "R1.7", ERRO),
    (r"\bstart(?:ar|e|ou|ado|ada|ando)\b|\bd(?:ar|ê|e)\s+(?:o\s+)?start\b", "use 'iniciar'", "R1.7", ERRO),
    (r"\b(?:des)?log(?:ar|ue|uei|ou|ado|ada|ando|amos)\b", "use 'entrar' ou 'sair'", "R1.7", ERRO),
    (r"\bprint(?:ar|e|ou|ado|ada|ando)\b", "use 'capturar a tela' ou 'imprimir'", "R1.7", ERRO),
    (r"\bbuild(?:ar|e|ou|ado|ada|ando)\b", "use 'compilar'", "R1.7", ERRO),
    (r"\bdebug(?:ar|ue|ou|ado|ando)\b", "use 'depurar'", "R1.7", ERRO),
    (r"\bchec(?:ar|ou|ado|ada|ando|amos)\b|\bcheque\b", "use 'verificar'", "R1.7", ERRO),
    (r"\brod(?:ar|e|ou|ando)\b", "use 'executar'", "R1.7", AVISO),
    (r"\bvisando\b|\bobjetivando\b|\bcom\s+o\s+objetivo\s+de\b|\bno\s+intuito\s+de\b|\bno\s+sentido\s+de\b",
     "use 'para'", "R4.5", ERRO),
    (r"\batravés\s+d[eoa]s?\b", "use 'por', 'com' ou 'pelo' (exceto sentido físico)", "R4.5", AVISO),
    (r"\b(?:a|em)\s+nível\s+d[eoa]s?\b", "use 'em' ou 'no'", "R4.5", ERRO),
    (r"\btendo\s+em\s+vista\b|\bhaja\s+vista\b|\bem\s+virtude\s+d[eoa]s?\b|\bdevido\s+ao\s+fato\b",
     "use 'porque'", "R4.5", ERRO),
    (r"\buma\s+vez\s+que\b", "use 'porque' ou 'depois que'", "R4.5", AVISO),
    (r"(?:^|(?<=[,:] ))caso\s+(?!de\b|d[oa]s?\b|n[oa]s?\b|contrário\b)", "use 'se'", "R4.5", ERRO),
    (r"\bcaso\s+contrário\b", "use 'se não'", "R4.5", AVISO),
    (r"\bmediante\b", "use 'com' ou 'por'", "R4.5", ERRO),
    (r"\bsendo\s+que\b", "use 'e', 'mas', 'porque' ou uma frase nova", "R4.5", ERRO),
    (r"\b(?:destarte|outrossim|ademais|conquanto)\b|\bnão\s+obstante\b",
     "use 'por isso', 'também' ou 'mas'", "R4.5", ERRO),
    (r"\bassim\s+sendo\b|\bdessa\s+forma\b|\bdesta\s+forma\b", "use 'por isso' ou 'então'", "R4.5", AVISO),
    (r"\beventualmente\b", "use 'às vezes' ou 'no fim'", "R1.2", AVISO),
    (r"\b(?:o|a|os|as|do|da|dos|das|no|na|nos|nas|pelo|pela|ao|à)\s+mesm[oa]s?\b"
     r"(?=\s*(?:[.,:)]|$|\s+(?:é|são|foi|foram|está|estão|será|deve|pode|não|se|for|tem|em|no|na|para|com|por)\b))",
     "'o mesmo' como pronome: repita o substantivo", "R2.4", AVISO),
    (r"\babaixo\b(?!\s+de\s+\d)|\bacima\b(?!\s+de\s+\d)", "use 'a seguir', 'anterior' ou o nome do item",
     "R9.5", AVISO),
    (r"\bsegue(?:m)?\s+(?:em\s+anexo|abaixo|acima)\b", "cite o item: 'A tabela 1 mostra...'", "R9.3", ERRO),
    (r"\bpor\s+favor\b|\bfavor\s+\w+(?:ar|er|ir)\b|\bgentileza\b", "omita a fórmula de cortesia", "R5.8", ERRO),
    (r"\bvimos\s+por\s+meio\s+desta\b|\binformamos\s+que\b", "omita a fórmula burocrática", "R9.3", ERRO),
    (r"\ba\s+gente\b", "use o imperativo", "R9.2", ERRO),
    (r"\be/ou\b", "use 'A, B ou os dois'", "R8.8", ERRO),
    (r"\b(?:alguns|algumas|vários|várias|diversos|diversas|rapidamente)\b|\bem\s+breve\b",
     "termo vago: escreva o valor exato", "R9.4", AVISO),
    (r"\bblacklist\w*", "use 'lista de bloqueio'", "R9.6", AVISO),
    (r"\bwhitelist\w*", "use 'lista de permissão'", "R9.6", AVISO),
    (r"\bslaves?\b", "use 'réplica'", "R9.6", AVISO),
]

PADRAO_PASSIVA = re.compile(
    r"\b(?:é|são|foi|foram|será|serão|seja|sejam|ser|sido|sendo|era|eram|fosse|fossem|for|forem)"
    r"\s+(?:\w+mente\s+)?(?:\w+(?:ado|ada|ados|adas|ido|ida|idos|idas)"
    r"|(?:feit|escrit|abert|post|vist|dit|cobert|aceit|impress|suspens|expost)[oa]s?|entregues?|pag[oa]s?)\b",
    re.IGNORECASE,
)
PADRAO_PASSIVA_SE = re.compile(r"\b\w+(?:a|e|am|em)-se\b", re.IGNORECASE)
EXCECOES_SE = {
    "certifique-se", "lembre-se", "inscreva-se", "cadastre-se", "conecte-se",
    "desconecte-se", "assegure-se", "dirija-se", "informe-se", "esqueça-se",
}
PADRAO_GERUNDIO = re.compile(r"\b\w{2,}(?:ando|endo|indo)\b", re.IGNORECASE)
EXCECOES_GERUNDIO = {
    "quando", "comando", "contrabando", "mando", "bando", "brando", "lindo", "vindo",
    "infindo", "tremendo", "horrendo", "estupendo", "dividendo", "adendo", "remendo",
    "doutorando", "mestrando", "formando", "graduando", "minuendo", "subtraendo",
    "fernando", "armando", "orlando", "rolando", "rondando",
}
PADRAO_NOMINALIZACAO = re.compile(
    r"\b(?:realiz|efetu|proced|promov|fa[zç]|fe[zi])\w*\s+(?:a|o|as|os|à|ao)\s+"
    r"\w+(?:ção|ções|são|sões|mento|mentos)\b",
    re.IGNORECASE,
)
PADRAO_CADEIA_DE = re.compile(r"\b\w+(?:\s+(?:de|do|da|dos|das)\s+\w+){3,}", re.IGNORECASE)
PADRAO_CITACAO = re.compile(r"\"[^\"]*\"|“[^”]*”")
PADRAO_PALAVRA = re.compile(r"\w+(?:[-'’./:,]\w+)*")
PADRAO_FIM_FRASE = re.compile(r"[.!?…][\"”')\]]*\s+(?=[\"“(\[]?[A-ZÀ-ÖØ-Þ0-9])")
PADRAO_LISTA_NUMERADA = re.compile(r"^\s*\d+[.)]\s+")
PADRAO_LISTA_MARCADOR = re.compile(r"^\s*[-*+]\s+(?:\[[ xX]\]\s+)?")
PADRAO_AVISO_SEGURANCA = re.compile(r"\b(?:ATENÇÃO|CUIDADO)\s*:")
ABREVIATURAS = [
    "p. ex.", "ex.", "etc.", "sr.", "sra.", "dr.", "dra.", "nº.", "n.º", "pág.", "págs.",
    "aprox.", "vs.", "e.g.", "i.e.", "cf.", "art.", "fig.", "obs.", "min.", "máx.",
]
MARCA_PONTO = "\u2024"

TERMOS_COMPILADOS = [
    (re.compile(p, re.IGNORECASE), sugestao, regra, sev) for p, sugestao, regra, sev in TERMOS_NAO_APROVADOS
]


@dataclass
class Achado:
    arquivo: str
    linha: int
    severidade: str
    regra: str
    mensagem: str
    trecho: str


@dataclass
class Bloco:
    linha: int
    texto: str
    procedimento: bool
    paragrafo: bool


def limpar_linha(linha: str) -> str:
    linha = re.sub(r"^\s*>+\s?", "", linha)
    linha = PADRAO_LISTA_NUMERADA.sub("", linha)
    linha = PADRAO_LISTA_MARCADOR.sub("", linha)
    linha = re.sub(r"`[^`]+`", "CODIGO", linha)
    linha = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", linha)
    linha = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", linha)
    linha = re.sub(r"https?://\S+", "URL", linha)
    linha = re.sub(r"<[^>]+>", "", linha)
    linha = re.sub(r"(\*\*|__)(.+?)\1", r"\2", linha)
    linha = re.sub(r"(?<!\w)([*_])(\S.*?)\1(?!\w)", r"\2", linha)
    return linha.strip()


def extrair_blocos(texto: str, tipo: str) -> Iterator[Bloco]:
    linhas = texto.splitlines()
    inicio = 0
    if linhas and linhas[0].strip() == "---":
        for i in range(1, len(linhas)):
            if linhas[i].strip() == "---":
                inicio = i + 1
                break

    atual: List[str] = []
    linha_atual = 0
    procedimento_atual = False
    paragrafo_atual = False
    em_lista_numerada = False
    em_codigo = False

    def fechar() -> Optional[Bloco]:
        nonlocal atual
        if not atual:
            return None
        bloco = Bloco(linha_atual, "\n".join(atual), procedimento_atual, paragrafo_atual)
        atual = []
        return bloco

    def tipo_do_bloco(numerado: bool, aviso: bool) -> bool:
        if tipo == "procedimento":
            return True
        if tipo == "descricao":
            return False
        return numerado or aviso

    for indice in range(inicio, len(linhas)):
        bruta = linhas[indice]
        numero = indice + 1
        sem_espaco = bruta.strip()

        if re.match(r"^(```|~~~)", sem_espaco):
            bloco = fechar()
            if bloco:
                yield bloco
            em_codigo = not em_codigo
            continue
        if em_codigo:
            continue

        if not sem_espaco or sem_espaco.startswith(("#", "|", "<!--")) or re.match(r"^[-*_]{3,}$", sem_espaco):
            bloco = fechar()
            if bloco:
                yield bloco
            if sem_espaco.startswith("#"):
                em_lista_numerada = False
            continue

        numerado = bool(PADRAO_LISTA_NUMERADA.match(bruta))
        marcador = bool(PADRAO_LISTA_MARCADOR.match(bruta))
        recuado = bruta.startswith(("  ", "\t"))

        if numerado or marcador or not atual:
            bloco = fechar()
            if bloco:
                yield bloco
            if numerado:
                em_lista_numerada = True
            elif not recuado and not marcador:
                em_lista_numerada = False
            limpa = limpar_linha(bruta)
            aviso = bool(PADRAO_AVISO_SEGURANCA.search(limpa))
            linha_atual = numero
            procedimento_atual = tipo_do_bloco(numerado or (recuado and em_lista_numerada), aviso)
            paragrafo_atual = not (numerado or marcador or recuado)
            atual = [limpa]
        else:
            atual.append(limpar_linha(bruta))

    bloco = fechar()
    if bloco:
        yield bloco


def proteger_abreviaturas(texto: str) -> str:
    for abreviatura in ABREVIATURAS:
        padrao = re.compile(r"(?<!\w)" + re.escape(abreviatura), re.IGNORECASE)
        texto = padrao.sub(lambda m: m.group(0).replace(".", MARCA_PONTO), texto)
    return texto


def dividir_frases(texto: str) -> Iterator[Tuple[int, str]]:
    texto = proteger_abreviaturas(texto)
    inicio = 0
    for fim in PADRAO_FIM_FRASE.finditer(texto):
        yield inicio, texto[inicio:fim.end()].strip()
        inicio = fim.end()
    if texto[inicio:].strip():
        yield inicio, texto[inicio:].strip()


def resumir(frase: str, limite: int = 70) -> str:
    frase = " ".join(frase.replace(MARCA_PONTO, ".").split())
    return frase if len(frase) <= limite else frase[: limite - 3] + "..."


def verificar_frase(frase: str, procedimento: bool, args: argparse.Namespace) -> Iterator[Tuple[str, str, str]]:
    palavras = len(PADRAO_PALAVRA.findall(frase))
    maximo = args.max_procedimento if procedimento else args.max_descricao
    if palavras > maximo:
        tipo = "procedimento" if procedimento else "descrição"
        yield ERRO, "R4.2", f"frase de {tipo} com {palavras} palavras (máximo {maximo})"

    if ";" in frase:
        yield ERRO, "R8.1", "ponto e vírgula: divida a frase ou use uma lista"
    if "!" in frase:
        yield AVISO, "R8.7", "ponto de exclamação"
    if "..." in frase or "…" in frase:
        yield AVISO, "R8.7", "reticências"

    frase = PADRAO_CITACAO.sub("CITACAO", frase)

    for padrao, sugestao, regra, severidade in TERMOS_COMPILADOS:
        encontrado = padrao.search(frase)
        if encontrado:
            yield severidade, regra, f"'{encontrado.group(0).strip()}': {sugestao}"

    for encontrado in PADRAO_PASSIVA.finditer(frase):
        severidade = ERRO if procedimento else AVISO
        yield severidade, "R3.1", f"possível voz passiva '{encontrado.group(0)}': use a voz ativa"
    for encontrado in PADRAO_PASSIVA_SE.finditer(frase):
        if encontrado.group(0).lower() not in EXCECOES_SE:
            yield AVISO, "R3.1", f"possível voz passiva com 'se' '{encontrado.group(0)}': use a voz ativa"

    for encontrado in PADRAO_GERUNDIO.finditer(frase):
        if encontrado.group(0).lower() not in EXCECOES_GERUNDIO:
            yield AVISO, "R3.3", f"gerúndio '{encontrado.group(0)}': divida em frases ou use outro tempo"

    encontrado = PADRAO_NOMINALIZACAO.search(frase)
    if encontrado:
        yield AVISO, "R2.3", f"nominalização '{encontrado.group(0)}': use o verbo da ação"

    encontrado = PADRAO_CADEIA_DE.search(frase)
    if encontrado:
        yield AVISO, "R2.1", f"mais de três substantivos encadeados: '{encontrado.group(0)}'"

    if procedimento and re.search(r"\betc\b", frase, re.IGNORECASE):
        yield AVISO, "R9.4", "'etc.' em procedimento: escreva a lista completa"


def verificar_texto(texto: str, nome: str, args: argparse.Namespace) -> List[Achado]:
    achados: List[Achado] = []
    for bloco in extrair_blocos(texto, args.tipo):
        frases = list(dividir_frases(bloco.texto))
        for deslocamento, frase in frases:
            linha = bloco.linha + bloco.texto[:deslocamento].count("\n")
            for severidade, regra, mensagem in verificar_frase(frase, bloco.procedimento, args):
                achados.append(Achado(nome, linha, severidade, regra, mensagem, resumir(frase)))
        if bloco.paragrafo and len(frases) > args.max_frases_paragrafo:
            achados.append(Achado(
                nome, bloco.linha, AVISO, "R6.2",
                f"parágrafo com {len(frases)} frases (máximo {args.max_frases_paragrafo})",
                resumir(bloco.texto),
            ))
    if args.sem_avisos:
        achados = [a for a in achados if a.severidade == ERRO]
    return achados


def listar_arquivos(caminhos: Iterable[str]) -> Iterator[Path]:
    for caminho in caminhos:
        alvo = Path(caminho)
        if alvo.is_dir():
            for arquivo in sorted(alvo.rglob("*")):
                if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES:
                    yield arquivo
        else:
            yield alvo


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verifica a redação técnica STE em português brasileiro.",
    )
    parser.add_argument("caminhos", nargs="+", help="arquivos, pastas ou '-' para ler da entrada padrão")
    parser.add_argument("--tipo", choices=["auto", "procedimento", "descricao"], default="auto",
                        help="tipo do texto. 'auto' trata listas numeradas e avisos como procedimento")
    parser.add_argument("--max-procedimento", type=int, default=20, help="máximo de palavras por frase de procedimento")
    parser.add_argument("--max-descricao", type=int, default=25, help="máximo de palavras por frase de descrição")
    parser.add_argument("--max-frases-paragrafo", type=int, default=6, help="máximo de frases por parágrafo")
    parser.add_argument("--estrito", action="store_true", help="retorna código 1 também quando há AVISO")
    parser.add_argument("--sem-avisos", action="store_true", help="mostra só os itens ERRO")
    parser.add_argument("--json", action="store_true", help="mostra o resultado em JSON")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = criar_parser().parse_args(argv)
    achados: List[Achado] = []
    for caminho in args.caminhos:
        if caminho == "-":
            achados.extend(verificar_texto(sys.stdin.read(), "<stdin>", args))
            continue
        for arquivo in listar_arquivos([caminho]):
            try:
                texto = arquivo.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as erro:
                print(f"Não foi possível ler {arquivo}: {erro}", file=sys.stderr)
                return 2
            achados.extend(verificar_texto(texto, str(arquivo), args))

    erros = sum(1 for a in achados if a.severidade == ERRO)
    avisos = len(achados) - erros

    if args.json:
        print(json.dumps({"erros": erros, "avisos": avisos, "achados": [asdict(a) for a in achados]},
                         ensure_ascii=False, indent=2))
    else:
        for a in achados:
            print(f"{a.arquivo}:{a.linha}: {a.severidade} {a.regra}: {a.mensagem}\n    \"{a.trecho}\"")
        print(f"\nTotal: {erros} ERRO, {avisos} AVISO.")

    if erros or (args.estrito and avisos):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
