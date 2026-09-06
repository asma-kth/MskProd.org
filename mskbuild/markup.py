"""A very small markup dialect used to author topic content.

Block syntax
------------
    ### Heading                     -> h4 sub heading
    - item                          -> unordered list
    1. item                         -> ordered list
    | a | b |                       -> table, first row is the header
    ```python  ... ```              -> highlighted code block
    ```pseudo  ... ```              -> OCR reference language / pseudocode
    ```text    ... ```              -> plain preformatted block
    !key Title :: body              -> key idea callout
    !grade Title :: body            -> grade 9 / A star callout
    !warn Title :: body             -> common mistake callout
    !exam Title :: body             -> exam technique callout
    !fact Title :: body             -> Pixel fun fact callout
    !diagram <name>                 -> an inline SVG diagram from mskbuild.diagrams
    !tool <name>                    -> mount point for an interactive tool
    everything else                 -> paragraph

Inline syntax
-------------
    **bold**   *italic*   `code`   [text](url)
"""
import html
import re

def _slot(i: int) -> str:
    """Placeholder built from control characters.

    Using control characters rather than digits matters: the highlighter stashes
    comments and strings first, and a digit-based placeholder would then be
    re-matched by the number rule and destroyed.
    """
    return "\x01" + "".join(chr(3 + int(d)) for d in str(i)) + "\x02"


# --------------------------------------------------------------- inline

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITAL = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_SUB = re.compile(r"~([0-9a-z]+)~")
_SUP = re.compile(r"\^([0-9a-z+-]+)\^")


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    slots = []

    def stash(m):
        slots.append("<code>" + m.group(1) + "</code>")
        return _slot(len(slots) - 1)

    out = _INLINE_CODE.sub(stash, out)
    out = _LINK.sub(lambda m: '<a href="%s"%s>%s</a>' % (
        m.group(2),
        ' target="_blank" rel="noopener"' if m.group(2).startswith("http") else "",
        m.group(1)), out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITAL.sub(r"<em>\1</em>", out)
    out = _SUB.sub(r"<sub>\1</sub>", out)
    out = _SUP.sub(r"<sup>\1</sup>", out)
    for i, s in enumerate(slots):
        out = out.replace(_slot(i), s)
    return out


# ------------------------------------------------------ syntax colouring

PY_KW = ("False None True and as assert async await break class continue def del elif else "
         "except finally for from global if import in is lambda nonlocal not or pass raise "
         "return try while with yield self").split()
PY_BUILTIN = ("print input int str float bool list dict tuple set len range open abs round min max "
              "sum sorted enumerate zip type isinstance super append pop insert remove index "
              "split join strip upper lower replace format random randint choice sqrt append "
              "keys values items get read write close readlines").split()
PSEUDO_KW = ("if then else elseif endif for to next while endwhile do until switch case default "
             "endswitch function endfunction procedure endprocedure return global array "
             "print input and or not div mod byRef byVal new class inherits public private "
             "true false").split()


def _highlight(code: str, lang: str) -> str:
    kws = PSEUDO_KW if lang == "pseudo" else PY_KW
    bis = [] if lang == "pseudo" else PY_BUILTIN
    esc = html.escape(code, quote=False)
    tokens = []

    def stash(cls, text):
        tokens.append('<span class="tok-%s">%s</span>' % (cls, text))
        return _slot(len(tokens) - 1)

    # comments first so keywords inside them are left alone
    esc = re.sub(r"(#[^\n]*)", lambda m: stash("com", m.group(1)), esc)
    esc = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')',
                 lambda m: stash("com", m.group(1)), esc, flags=re.S)
    esc = re.sub(r'("[^"\n]*"|\'[^\'\n]*\')', lambda m: stash("str", m.group(1)), esc)
    esc = re.sub(r"\b(\d+\.?\d*)\b", lambda m: stash("num", m.group(1)), esc)
    if kws:
        esc = re.sub(r"\b(" + "|".join(sorted(kws, key=len, reverse=True)) + r")\b",
                     lambda m: stash("kw", m.group(1)), esc,
                     flags=0 if lang != "pseudo" else re.I)
    if bis:
        esc = re.sub(r"\b(" + "|".join(sorted(bis, key=len, reverse=True)) + r")(?=\s*\()",
                     lambda m: stash("bi", m.group(1)), esc)
    esc = re.sub(r"\b([a-zA-Z_]\w*)(?=\s*\()", lambda m: stash("fn", m.group(1)), esc)
    for i, t in enumerate(tokens):
        esc = esc.replace(_slot(i), t)
    return esc


LANG_LABEL = {"python": "Python", "pseudo": "OCR reference language", "text": "",
              "sql": "SQL", "html": "HTML", "css": "CSS", "js": "JavaScript",
              "assembly": "Assembly", "trace": "Trace table"}


def code_block(code: str, lang: str = "python") -> str:
    body = _highlight(code, lang) if lang in ("python", "pseudo") else html.escape(code, quote=False)
    label = LANG_LABEL.get(lang, lang.upper() if lang else "")
    lab = '<span class="code-label">%s</span>' % label if label else ""
    return ('<div class="code-block">%s<button class="code-copy" type="button">Copy</button>'
            '<pre><code>%s</code></pre></div>' % (lab, body))


# ----------------------------------------------------------------- blocks

CALLOUTS = {
    "key":   ("note-key", "i-key", "Key idea"),
    "grade": ("note-grade", "i-trophy", "Reach the top grade"),
    "warn":  ("note-warn", "i-warn", "Common mistake"),
    "exam":  ("note-exam", "i-paper", "In the exam"),
    "fact":  ("note-fact", "i-sparkle", "Fun fact"),
    "info":  ("note-key", "i-info", "Note"),
}


def render(src: str) -> str:
    lines = (src or "").strip("\n").split("\n")
    out, i, n = [], 0, len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip() or "python"
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            # strip the common leading indent so authoring stays readable
            body = "\n".join(buf)
            indents = [len(l) - len(l.lstrip()) for l in buf if l.strip()]
            if indents:
                cut = min(indents)
                body = "\n".join(l[cut:] if len(l) >= cut else l for l in buf)
            out.append(code_block(body.rstrip(), lang))
            continue

        # heading
        if stripped.startswith("### "):
            out.append("<h4>%s</h4>" % inline(stripped[4:]))
            i += 1
            continue

        # diagram: !diagram <name>
        m = re.match(r"^!diagram\s+([a-z0-9-]+)\s*$", stripped)
        if m:
            from .diagrams import REGISTRY as _DG
            name = m.group(1)
            if name not in _DG:
                raise KeyError("unknown diagram %r (have: %s)"
                               % (name, ", ".join(sorted(_DG))))
            out.append(_DG[name]())
            i += 1
            continue

        # interactive tool: !tool <name>
        m = re.match(r"^!tool\s+([a-z0-9-]+)\s*(?:::\s*(.*))?$", stripped)
        if m:
            from .tools import TOOLS
            name = m.group(1)
            if name not in TOOLS:
                raise KeyError("unknown tool %r (have: %s)"
                               % (name, ", ".join(sorted(TOOLS))))
            meta = TOOLS[name]
            head = (m.group(2) or "").strip() or meta["title"]
            out.append(
                '<div class="tool" data-tool="%s">'
                '<div class="tool-head"><svg class="icon" aria-hidden="true">'
                '<use href="#%s"></use></svg><h4>%s</h4></div>'
                '<div class="tool-body"><p class="tool-fallback">%s '
                'This tool needs JavaScript, so turn it on to use it. '
                'Everything you need to answer the exam question is explained '
                'in the text above.</p></div></div>'
                % (name, meta["icon"], inline(head), inline(meta["blurb"])))
            i += 1
            continue

        # callout
        m = re.match(r"^!(\w+)\s+(.*)$", stripped)
        if m and m.group(1) in CALLOUTS:
            kind = m.group(1)
            rest = m.group(2)
            title, _, body = rest.partition("::")
            buf = [body.strip()]
            i += 1
            while i < n and lines[i].strip() and not re.match(r"^!(\w+)\s", lines[i].strip()) \
                    and not lines[i].strip().startswith(("```", "### ", "- ", "|")):
                buf.append(lines[i].strip())
                i += 1
            cls, icon, default = CALLOUTS[kind]
            head = title.strip() or default
            text = " ".join(x for x in buf if x)
            out.append(
                '<div class="note %s"><div class="note-title">'
                '<svg class="icon" aria-hidden="true"><use href="#%s"></use></svg>%s</div><p>%s</p></div>'
                % (cls, icon, inline(head), inline(text)))
            continue

        # table
        if stripped.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                head = rows[0]
                body = rows[1:]
                t = ['<div class="table-scroll"><table><thead><tr>']
                t += ["<th>%s</th>" % inline(c) for c in head]
                t.append("</tr></thead><tbody>")
                for r in body:
                    t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
                t.append("</tbody></table></div>")
                out.append("".join(t))
            continue

        # unordered list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ul>")
            continue

        # ordered list
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s", "", lines[i].strip()))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % inline(x) for x in items) + "</ol>")
            continue

        # checklist
        if stripped.startswith("+ "):
            items = []
            while i < n and lines[i].strip().startswith("+ "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append('<ul class="checklist">' + "".join(
                '<li><svg class="icon" aria-hidden="true"><use href="#i-check"></use></svg>'
                "<span>%s</span></li>" % inline(x) for x in items) + "</ul>")
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r"^(```|### |!(\w+)\s|\||- |\+ |\d+\.\s)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))

    return "\n".join(out)


def plain(src: str, limit: int = 220) -> str:
    """Strip markup down to plain text, for meta descriptions and the index."""
    t = re.sub(r"```.*?```", " ", src or "", flags=re.S)
    t = re.sub(r"^!(diagram|tool)\s+.*$", " ", t, flags=re.M)
    t = re.sub(r"^[!#\-+|>\d.]+\s*", " ", t, flags=re.M)
    t = re.sub(r"[*`\[\]()~^]", "", t)
    t = re.sub(r"::", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0] + "..."
    return t
