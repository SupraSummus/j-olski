"""The typography pack: rules that need nothing but a tokenizer.

Every threshold here is provisional, which is what ``calibration`` records
and what the milestone 1 harness settles.
See docs/roadmap.md and docs/rules.md.
"""

from olski.rules import UNCALIBRATED, Pack

pack = Pack(
    name="typography",
    tier="A",
    severity="warning",
    calibration=UNCALIBRATED,
    # Typographic convention does not shift with register: a Polish quotation
    # mark is a Polish quotation mark in a manual and in a novel. Rules whose
    # threshold does depend on register override this per rule.
    registers=("technical", "general"),
)

pack.rule(
    id="em-dash-density",
    check="pattern-density",
    # Fiction wants dashes and uses them deliberately,
    # so this one is scoped to the declared target register.
    registers=("technical",),
    params=dict(
        pattern=r"[—–]",
        unit="document",
        # Roughly one dash per hundred words. Chosen to be lenient on purpose,
        # since an uncalibrated threshold should err towards saying nothing.
        max_per_1000_words=10,
        min_count=3,
        min_words=150,
    ),
    message="{count} dashes in {words} words, {rate} per 1000, "
    "above the {limit} this pack allows; "
    "Polish technical prose usually takes a comma, a colon or parentheses instead.",
    justification="""
    The pauza is at home in Polish dialogue and in a deliberate aside,
    but where English reaches for an em dash
    Polish technical prose generally reaches for a comma, a colon or parentheses.
    A high rate in expository Polish is usually English punctuation habits carried across,
    which is also why it is one of the more visible signatures of generated text.
    """,
    sources=(
        "docs/rule-inventory.md#typography-tier-a",
        "https://en.wikipedia.org/wiki/Wikipedia_talk:Signs_of_AI_writing",
    ),
)

pack.rule(
    id="quote-straight",
    check="pattern",
    params=dict(pattern=r'"'),
    message="Straight quotation mark; Polish takes „ opening and ” closing.",
    justification="""
    Polish typography uses „ for the opening quotation mark and ” for the closing one.
    A straight ASCII quote is a keyboard artifact rather than a Polish mark,
    and it carries no information about which end of the quotation it is.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="quote-english",
    check="pattern",
    # Only the opening mark differs. The closing mark ” is shared,
    # so flagging it would accuse correctly typeset Polish.
    params=dict(pattern=r"“"),
    message="English opening quotation mark; Polish opens a quotation with „ on the baseline.",
    justification="""
    The English pair “ ” and the Polish pair „ ” differ in the opening mark only:
    it sits on the baseline in Polish and at cap height in English,
    and the closing ” is the same character in both.
    An opening “ in Polish text is half-applied English typesetting.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="orphan-single-letter-word",
    check="line-end-word",
    params=dict(words=["a", "i", "o", "u", "w", "z"]),
    message="Single-letter word {word} left at the end of a line; "
    "Polish typography moves it to the next line with a non-breaking space.",
    justification="""
    Polish has one-letter conjunctions and prepositions,
    and typographic practice does not leave them at the end of a line,
    because the reader meets a word with nothing yet to attach it to.
    The usual fix is a non-breaking space
    between the letter and the word it governs.
    This rule can only apply where a line break in the source
    is a line break in the output,
    so it abstains on a document whose own lines say otherwise
    as well as on a format olski does not read.
    The list is lower case, which leaves out the sentence
    that opens on one of these words at a line end:
    the capitals belong to a Roman numeral, a section label and a unit
    more often than to a conjunction,
    and one list cannot hold `Tom I` out and let `I` in.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="double-space",
    check="pattern",
    params=dict(pattern=r"(?<=\S)[ ]{2,}(?=\S)"),
    message="Two or more spaces between words.",
    justification="""
    Polish typesetting sets a single space between words, including after a full stop.
    Runs of spaces inside a line are an editing artifact,
    and they survive into rendered output as visible gaps.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="trailing-space",
    check="pattern",
    severity="note",
    params=dict(pattern=r"[ \t]+$", flags=["multiline"]),
    message="Trailing whitespace at the end of a line.",
    justification="""
    Trailing whitespace is invisible to the author,
    changes nothing about the rendered text,
    and shows up in every later diff of the line that carries it.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="space-before-punctuation",
    check="pattern",
    params=dict(
        # The mark itself is the match, not the space before it, so that the
        # message can name what is wrong and point at it.
        pattern=r"(?<=[ \t])[,.;:!?…]",
        # A mark that runs straight into a word is not punctuation closing a
        # clause: it is a file name such as .config, a version, or an ellipsis
        # opening a fragment.
        unless_followed_by=r"\w",
    ),
    message="Space before {match}, which sets tight against the word before it.",
    justification="""
    In Polish, as in English,
    a comma, full stop, semicolon, colon, question mark and exclamation mark
    set tight against the preceding word.
    A space before one is a French convention or a typing slip, not a Polish one.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="missing-space-after-punctuation",
    check="pattern",
    # Digits on either side are excluded:
    # 1,5 is a Polish decimal and 10:30 is a time, and neither wants a space.
    params=dict(pattern=r"(?<!\d)[,;:](?=[^\s\d)\]/”])"),
    message="No space after {match}.",
    justification="""
    A comma, semicolon or colon is followed by a space in running Polish text.
    The missing space is nearly always a concatenation artifact rather than a choice,
    which is why this rule is safe to state without a threshold.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)

pack.rule(
    id="missing-space-after-full-stop",
    check="pattern",
    params=dict(
        # A lower-case letter or a closing quotation mark is required before the
        # stop, and a capital after it, so that decimal points, dates and
        # internal abbreviation periods such as the one in m.in. are left alone.
        pattern=r"""(?<=[a-ząćęłńóśźż”"])[.!?](?=[A-ZĄĆĘŁŃÓŚŹŻ])""",
    ),
    message="No space after {match}.",
    justification="""
    Polish sets a space after a full stop,
    and that holds whether the stop ends a sentence or an abbreviation:
    np. Zapisz takes a space exactly as Zapisz plik. Potem does.
    So the rule does not have to decide which of the two it is looking at.
    Both readings of np.Zapisz are malformed,
    and the ambiguity is about why it is wrong rather than whether it is.
    The one real false positive left is a dotted identifier
    quoted bare in running prose, such as System.Console,
    which is code rather than Polish
    and belongs in a code span the linter is not being shown.
    """,
    sources=("docs/rule-inventory.md#typography-tier-a",),
)
