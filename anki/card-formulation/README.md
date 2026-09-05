# Card formulation

Cards are cheap or expensive to review depending on how they're written, and the difference
compounds over thousands of reps. This is the policy I formulate against, adapted from
Piotr Woźniak's [Twenty Rules of Formulating Knowledge](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge).

| File | What it is |
|---|---|
| [`card-formulation.md`](card-formulation.md) | The policy: which rules an agent can automate, which need a human, and the per-card-type table |
| [`card-formulation.prompt.md`](card-formulation.prompt.md) | A prompt that applies it — drop into any agent session with AnkiConnect access |

## The two ideas worth stealing

**Sort the rules by owner.** Woźniak's twenty rules don't all belong to an automated
registrar. Some are hard gates a script can enforce (the i+1 gate, monolingual definition,
source stamp, duplicate check); some are LLM rewrites (wording); and some — personalisation,
emotional hooks — must stay with the learner, because an agent inventing them produces
generic filler.

**Japanese breaks the atomization rule.** The minimum information principle says split
everything down to the smallest retrievable unit. For sentence cards that destroys the thing
being learned: collocation, register and particle nuance live in the sentence. The fix isn't
shorter cards, it's the **i+1 gate** — exactly one unknown word per sentence. Leeches come
from multiple unknowns, not from length.

See the per-card-type table in the policy for where each stance applies.

## Related

- [`../reference/conventions.md`](../reference/conventions.md) — *how* to format a
  card once you know what to put on it
