---
layout: post
title: "Personal Notes on Natural Language Processing, week 1"
date: 2016-05-22 10:03:00 +0300
excerpt: "My notes on the Natural Language Processing Coursera course for the first week. Just some compressed notes."
categories: [NLP]
tags: [NLP, Coursera]
comments: true
---

<!--excerpt-->

<h2><strong>Contents</strong></h2>

* TOC
{:toc}

### Regular Expressions

<strong>Regular Expressions in Practical NLP:</strong>
An example is given on how regexps are used in practice in real world case related to NLP.
A link to the open source code with many such examples can be found [here][tokenizer-github-url].

### Word Tokenization
The problem of extracting words from a text body.

<strong>Word Tokenization Bash Tools:</strong>
Using bash tools to analyse text. Useful programs:

* tr: Translates text, can perform substitutions
* sort: Sorts alphanumerically
* uniq: Groups and counts same words

<strong>Issues with Tokenization:</strong>

* How to handle punctuation (periods, dashes, apostrophes).<br>
* How to handle language specific punctuation e.g. French Le, L', l',<br>
German/Chinese no space between words etc.

<strong>Maximum Matching Word Segmentation Algorithm:</strong>
Given a string with no spaces, start at the beginning of the string,
find the longest word in the dictionary based on the beginning of said string,
segment out the first word and continue similarly. Doesn't work well on english.

### Word Normalization
The problem of transforming similar words to one with the "base" meaning.

<strong>Normalization:</strong>
Implicitly defining equivalence classes of terms. E.g. U.S.A. matching USA.
There is also asymmetric expansion, which is when searching for the term "window"
we might also want to search "windows", "Windows". However when searching for
"Windows" we might refer to the OS and only be interested in "Windows".

<strong>Case folding:</strong>
In information retrieval applications we usually reduce all letters to lowercase
for better matching. There are exceptions when we have mid-sentence upper case ones,
which might refer to special words.
In sentiment analysis case can be important.

<strong>Lemmatization:</strong>
Finding the correct dictionary headword form.
We are usually reducing inflections or variants to the base form.
E.g. am, are, is -> be
car, cars, car's, cars' -> car

<strong>Morphology:</strong>
Stems: The core meaning-bearing units.
Affixes: Bits and pieces that adhere to stems.
Stemming: Removing affexes, reducing terms to Stems.

<strong>Porter's stemming algorithm:</strong>
Step 1a: Remove plural-related affixes (sses -> ss, ies -> i, ss -> ss, s -> null)
Step 1b: Remove verb related affixes ( (*vowel*)ing -> null, (*vowel*)ed -> null)
Step 2: For long stems special rules (ational -> ate, izer -> ize, ator, ate)
Step 3: For longer stems more rules (al -> null, able -> null, ate -> null)

### Sentence Segmentation
The problem of defining sentences.

<strong>Classifier:</strong>
"!", "?" can be unambiguous sentence endings.
"."" is not, can be used in abbreviations and numbers.
Easier implementation with decision trees (series of if-then-else rules).
Case of the word ending with ".", case of the word after ".", length of the word with "." etc
We can use machine learning to give us a threshold of probabilities that a word
with a "." is an end of sentence.

### Minimum Edit Distance
The problem of defining word similarity

<strong>Definition:</strong>
The minimum number of editing operations (insertions, deletions, substitutions)
needed to transform one string to the other.
Usually all operations have a cost of 1. In Levenshtein Distance substitutions cost 2.
Can be used similarly on evaluating machine translation/speech recognition based
on operations of words between the machine generated text and a human equivalent.
We difine table D(i,j) that contains the cost between X(1,i) and Y(1,j) where
X(1,i) is the i first letters of string X and Y(1,j) the j first letters in string Y.

<strong>How to calculate:</strong>
Dynamic programming to the rescue. We are combining solutions to subproblems to
generate the solution to the whole problem. Levenshtein implementation:

![Levenshtein Distance](/img/levenshtein-distance.png)

<strong>Backtrace for Computing Alignments:</strong>
We can keep pointers in each cell to where we came from so we can retrace the steps
taken. Thus we know which action was taken in each step to compute the minimum
distance and we can get a "mapping" of the operations required.
Time complexity: O(nm), Space complecity: O(nm), Backtrace: O(n+m)

There is also Weighted Minimum Edit Distance, for cases where insertions and deletions
are not exactly equal but some operations have a higher or lower chance of occurring
(such as in spelling correction where the word was mistyped etc).
We keep del[x(i)], ins[y(j)] and sub[x(i),y(j)] tables with the extra costs per letter.

<strong>Minimum Edit Distance in Computational Biology:</strong>
The [Needleman-Wunsch Algorithm][needleman-url] is an implementation used in CB where we have a common
cost "-d" for insertions and deletions and "s" for substitutions.
This can be used to find the minimum edit distance of a string within a possibly larger string.

<strong>Local Alignment Problem:</strong>
Given two strings X, Y, find two substrings x', y' whose similarity is maximum.
Implementation using the Smith-Waterman algorithm.
![Smith-Waterman algorithm](/img/smith-waterman.png)


[tokenizer-github-url]:https://github.com/stanfordnlp/CoreNLP/blob/master/src/edu/stanford/nlp/process/PTBLexer.flex
[nlp-url]:https://www.coursera.org/course/nlp
[needleman-url]:https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
