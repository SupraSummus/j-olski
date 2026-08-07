"""A pack that counts characters instead of judging them.

A survey characterizes a corpus by how often a mark appears in it, and a rate
like that is only comparable across corpora if the same tokenizer produced the
denominator every time. The shipped rules produce most of them, since a
``pattern`` rule's row in ``olski --format report`` is its matches per thousand
words. What they do not produce is a rate for the marks no rule fires on — the
Polish quotation marks, and the dashes, which ``em-dash-density`` reports as the
share of documents over a threshold rather than as a rate.

So the counting versions live here, outside the linter, where a declaration that
asserts nothing about Polish cannot be read as a rule about it. What cites them
is docs/corpora.md and docs/generated-polish.md.

    python3 -m olski prose/ --format report --packs harness/counts.py
"""

from olski.rules import Pack

#: Counters are unscoped, because a count is not a norm and a norm is what a
#: register scopes.
pack = Pack(name="counts", severity="note")

COUNTING = """
Not a norm and not a defect: a count,
so that a rate a document cites is measured
over the same words the rules are measured over.
"""

for identifier, character in (
    ("em-dash", "—"),
    ("en-dash", "–"),
    ("quote-open", "„"),
    ("quote-close", "”"),
):
    pack.rule(
        id=identifier,
        check="pattern",
        params=dict(pattern=character),
        message=f"{identifier} {{match}}",
        justification=COUNTING,
    )
