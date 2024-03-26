# line-align

# line-align ![CI](https://github.com/rafelafrance/line-align/workflows/CI/badge.svg)

1. [Description](#Description)
2. [Alignment example](#Example)
3. [Install](#Install)
4. [Test](#Test)

## Description

I had several version of the "same" string coming from different sources, All of the strings were slightly different, and with no indication of which one, if any, is correct. So I decided to take a page from the bioinformatics and use a multiple sequence alignment algorithm on the text lines to find a single "best" representation of the true string.

The Multiple Sequence Alignment (MSA) algorithm that is directly analogous to the ones used for biological sequences but instead of using a PAM or BLOSUM substitution matrix we use a visual similarity matrix. Visual similarity depends on the font so an exact distance is not always feasible. Instead, we use a rough similarity score that ranges from +2 for characters that are identical, to -2 where the characters are wildly different like a period "." and a "W". The default gap penalty is -3 and the default gap extension penalty is -0.5.

For example, if given these strings:

```
MOJAVE DESERT, PROVIDENCE MTS.: canyon above
E. MOJAVE DESERT , PROVIDENCE MTS . : canyon above
E MOJAVE DESERT PROVTDENCE MTS. # canyon above
Be ‘MOJAVE DESERT, PROVIDENCE canyon “above
```

The alignment may look like the following, depending on the MSA parameters. "⋄" is the gap character.

```
⋄⋄⋄⋄MOJAVE DESERT⋄, PROVIDENCE MTS⋄.⋄: canyon ⋄above
E⋄. MOJAVE DESERT , PROVIDENCE MTS . : canyon ⋄above
E⋄⋄ MOJAVE DESERT ⋄⋄PROVTDENCE MTS⋄. # canyon ⋄above
Be ‘MOJAVE DESERT⋄, PROVIDENCE ⋄⋄⋄⋄⋄⋄⋄⋄canyon “above
```

## Install

## Test
