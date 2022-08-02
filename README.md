# [G-AI4Code](https://www.kaggle.com/competitions/AI4Code/overview)
---


## Brief:

The purpose of this repository is to provide a pipeline that can be applied to solve the AI4Code challenge hosted by Google on Kaggle. This is a Natural Language Processing Text Ranking Challenge. 

We're given a dataset of JSON files derived from python notebooks. A notebook can be interpreted as an ordered-set of text-blocks.

Where a text-block contains a string either of type "code" or "markdown".

Luckily, all "code" text-blocks contain only python code.

## Hypothesis:

Let X denote a notebook's JSON with k text-blocks.

Let C denote a set of "code" text-blocks and M denote a set of "markdown" text-blocks.

We can represent a given notebook as:

X = {C, M} | |X| = k

F: X -> X' | X' = (m1, c1, ..., m(k-|C|))

F = G o (H o C, J o M) | H: C -> C', J: M -> M', G: C' x M' -> X'


- [ ] Undesrtand Code Parrot
