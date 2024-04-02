# line-align

# line-align ![CI](https://github.com/rafelafrance/line-align/workflows/CI/badge.svg)

1. [Description](#Description)
2. [Install](#Install)
3. [Test](#Test)

## Description

The problem: I had several version of the "same" string coming from different sources, Although they were all supposed to be identical they were actually all slightly different, and with no indication of which one, if any, was correct. To find the "correct" string, I decided to use an algorithm bioinformatics and use a multiple sequence alignment (MSA) algorithm on the text lines to find a single representation of the "true" string.

The Multiple Sequence Alignment algorithm I am using is directly analogous to the ones used for biological sequences, but instead of using a PAM or BLOSUM substitution matrix I use a visual similarity matrix. Visual similarity of characters depends on the font so an exact distance is not always feasible. Instead, I use a rough similarity score that ranges from +2 for characters that are identical, to -2 where the characters are wildly different like a period "." and a "W". I also use a gap open penalty and a gap extend penalty just like the bioinformatics algorithm.

These are naive implementations of string algorithms based on Gusfield, 1997. I.e. There's _plenty_ of room for improvement.

**NOTE**: The functions are geared towards OCR errors and not human errors. OCR engines will often mistake one letter for another or drop/add a character (particularly from the ends) but will seldom transpose characters, which humans do often. Therefore: I do not consider transpositions in the Levenshtein or Needleman Wunsch distances, and substitutions are based on visual similarity, etc.

For example, if given these 4 similar strings:

```
MOJAVE DESERT, PROVIDENCE MTS.: canyon above
E. MOJAVE DESERT , PROVIDENCE MTS . : canyon above
E MOJAVE DESERT PROVTDENCE MTS. # canyon above
Be ‘MOJAVE DESERT, PROVIDENCE canyon “above
```

The alignment may look like the following, depending on the MSA parameters. "⋄" is the gap character.

```
⋄⋄⋄⋄MOJAVE DESERT⋄, PROVIDENCE MTS⋄.⋄: canyon ⋄above
E.⋄ MOJAVE DESERT , PROVIDENCE MTS . : canyon ⋄above
E⋄⋄ MOJAVE DESERT ⋄⋄PROVTDENCE MTS⋄. # canyon ⋄above
Be ‘MOJAVE DESERT⋄, PROVIDENCE ⋄⋄⋄⋄⋄⋄⋄⋄canyon “above
```

I can use a character (or word) selection algorithm to build a single "correct" string from this alignment. The result may look like:

```
E. MOJAVE DESERT, PROVIDENCE MTS.: canyon above
```

## API

## Install

## Test
