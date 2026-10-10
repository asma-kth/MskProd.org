"""Three dimensional scenes for topics where depth is part of the explanation.

These are plain HTML and CSS 3D transforms. There is no WebGL and no library:
a scene costs a few hundred bytes of markup and reuses the stylesheet the page
already loads, which matters on a revision site that students open on phones.

A scene is used where the thing being taught genuinely has layers, stacking or
position in space. A protocol stack, a memory hierarchy and a polygon mesh are
all easier to hold in your head when you can see them separated and turn them
around. A list of laws is not, and gets a flat diagram instead.

Every scene renders complete and readable with no JavaScript at all: the
stages are all in the markup and only hidden once the controller loads, and
the whole thing is described in full in the text alternative underneath, so a
reader using a screen reader is told what the picture shows rather than that a
picture exists.
"""
from .svg import esc

REGISTRY = {}


def scene(name):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap


def plane(z, title, sub="", tone="teal", extra="", width=None):
    """One horizontal sheet in the stack, lifted off the floor by z pixels."""
    w = ' style="--sc-z:%dpx;--sc-w:%dpx"' % (z, width) if width else ' style="--sc-z:%dpx"' % z
    return ('<div class="sc-plane sc-%s"%s>'
            '<span class="sc-plane-label"><b>%s</b>%s</span>%s</div>'
            % (tone, w, esc(title), '<i>%s</i>' % esc(sub) if sub else "", extra))


def stage(n, body, label):
    """One step of the walkthrough."""
    return ('<div class="sc-step" data-step="%d" data-sc-label="%s">%s</div>'
            % (n, esc(label), body))


def figure_scene(name, *, world, steps, title, desc, caption=None,
                 height=340, depth=0, labels=None, hint=None):
    """Wrap a scene in its figure, controls and text alternative.

    `world` is drawn on every stage, `steps` are the stages. `desc` is the full
    description, which is the picture's content for anyone who cannot see it.
    """
    n = len(steps)
    first = esc(labels[0]) if labels else ""
    controls = ""
    if n > 1:
        controls = (
            '<div class="sc-controls" hidden data-sc-controls>'
            '<button type="button" class="sc-btn" data-sc-prev aria-label="Previous step">Back</button>'
            '<button type="button" class="sc-btn sc-btn-play" data-sc-play '
            'aria-label="Play the animation">Play</button>'
            '<button type="button" class="sc-btn" data-sc-next aria-label="Next step">Next</button>'
            '<p class="sc-status" role="status" aria-live="polite">'
            '<b data-sc-count>Step 1 of %d</b> <span data-sc-text>%s</span></p>'
            '</div>' % (n, first))
    tip = ('<p class="sc-hint" data-sc-hint hidden>%s</p>'
           % esc(hint or "Drag the picture to turn it round. "
                         "With it focused, the arrow keys turn it too.")) if hint is not False else ""
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ""
    return (
        '<figure class="scene" data-scene="%s" style="--sc-h:%dpx;--sc-depth:%dpx">'
        '<div class="sc-frame"><div class="sc-stage" data-sc-stage>'
        '<div class="sc-world" data-sc-world>%s%s</div>'
        '</div></div>'
        '<p class="sc-alt">%s</p>%s%s%s</figure>'
        % (esc(name), height, depth, world, "".join(steps), esc(desc), tip, controls, cap))


# ============================================================ the TCP/IP stack

@scene("tcp-ip-stack-3d")
def _tcpip():
    """Four layers, seen as four sheets, with a packet falling through them.

    The whole point of a layered model is that each layer wraps what the one
    above it handed down and knows nothing about the contents. Drawn flat that
    reads as four boxes in a column; drawn as sheets you can see the message
    pass down through them and come back out the other side.
    """
    L = ["Your message starts at the top, in the application.",
         "Transport splits it into segments and adds a port number.",
         "Internet wraps each segment in a packet and adds IP addresses.",
         "Link turns the packet into a frame with MAC addresses, and it goes out.",
         "At the other end the same four layers run in reverse, unwrapping it."]

    LAYERS = [
        (255, "APPLICATION", "HTTP · HTTPS · SMTP", "lilac"),
        (170, "TRANSPORT", "TCP · UDP · ports", "teal"),
        (85, "INTERNET", "IP · routing", "lilac"),
        (0, "LINK", "cables, wifi · MAC", "teal"),
    ]
    world = "".join(plane(z, t, s, tone) for z, t, s, tone in LAYERS)

    # The travelling unit of data. It gains a wrapper at each layer going down.
    WRAPS = [
        (255, "DATA", ["Your message"], "lilac"),
        (170, "SEGMENT", ["TCP", "DATA"], "teal"),
        (85, "PACKET", ["IP", "TCP", "DATA"], "lilac"),
        (0, "FRAME", ["MAC", "IP", "TCP", "DATA"], "teal"),
    ]

    def unit(z, name, parts, tone):
        chips = "".join('<span class="sc-chip sc-chip-%s">%s</span>'
                        % ("head" if i < len(parts) - 1 else "body", esc(p))
                        for i, p in enumerate(parts))
        return ('<div class="sc-unit sc-%s" style="--sc-z:%dpx">'
                '<span class="sc-unit-name">%s</span>'
                '<span class="sc-unit-parts">%s</span></div>' % (tone, z, esc(name), chips))

    steps = []
    for i, (z, nm, parts, tone) in enumerate(WRAPS):
        body = unit(z, nm, parts, tone) + ('<div class="sc-glow" style="--sc-z:%dpx"></div>' % z)
        steps.append(stage(i + 1, body, L[i]))

    # The receiving stack: the same frame climbing back up, shedding wrappers.
    back = (unit(0, "FRAME ARRIVES", ["MAC", "IP", "TCP", "DATA"], "teal")
            + '<div class="sc-arrow sc-arrow-up"></div>'
            + '<div class="sc-note">each layer strips its own wrapper'
              ' and hands the rest up</div>')
    steps.append(stage(5, back, L[4]))

    desc = ("The four layer TCP/IP model drawn as four stacked sheets, with the "
            "application layer on top and the link layer at the bottom. A message "
            "starts at the application layer, where protocols such as HTTP, HTTPS, "
            "SMTP, IMAP and FTP live. It passes down to the transport layer, which "
            "splits it into segments and adds a TCP or UDP header carrying the port "
            "number. Each segment passes down to the internet layer, which wraps it "
            "in a packet and adds the source and destination IP addresses used for "
            "routing. Each packet passes down to the link layer, which wraps it in a "
            "frame carrying MAC addresses and puts it onto the physical network. At "
            "the receiving computer the same four layers run in reverse: each layer "
            "strips off the wrapper it recognises and hands the rest up, so the "
            "application at the top receives exactly the message that was sent. No "
            "layer needs to know how any other layer does its job, which is the "
            "whole reason the model is split up this way.")
    return figure_scene(
        "tcp-ip-stack-3d", world=world, steps=steps,
        title="The TCP/IP stack", desc=desc, height=425, depth=255, labels=L,
        caption="Each layer wraps what the layer above handed it, and knows nothing "
                "about what is inside. That is why you can change the wifi for a "
                "cable without rewriting the web browser.")
