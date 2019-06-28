# Saffron Irish

Code related to adapting Saffron to Irish. These scripts support the experiments
described in 

> "Adapting Term Recognition to an Under-Resourced Language: the Case of Irish" - J.P. McCrae and A. Doyle. Published at the Celtic Language Technology Workshop 2019

## Gold Standard

The gold standard is available in the file `gold.txt`. It is in the IOB format
using `_` to separate the tag and the word. This text is derived from Wikipedia
and is licensed with a [CC-BY-SA](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_4.0_International_License) license:

Example

    An_B tSomáilis_I Is_O í_O an_B tSomáilis_I an_O teanga_B a_O labhraíonn_O formhor_O muintir_O na_B Somáile_I agus_O na_O Somálaigh_B sna_O tíortha_O in_O aice_O láimhe_O ._O Is_O teanga_B Cúiseach_I í_O agus_O í_O an_O dara_O teanga_B Cúiseach_I is_O mó_O a_O labhraítear_O ar_O domhan_O í_O

## Scripts

* `align-pos.py`: Used to align the two part-of-speech tagged corpora
* `analyzze-corpus.py`: Produces some basic facts about the corpus reported in the paper
* `build-lemmatizer.py`: Builds the lemmatizer list for Saffron. Requires `morphology.xml` from [Pota Focal](http://www.potafocal.com).
* `eval.py`: Calculates precision, recall and F-Measure from two corpora (provided as command line arguments)
* `filter_term_freqs.py`: Filters out terms with excessive frequency. Requires `morphology.xml` and the `term_freqs.tsv` from `term_freq.py`
* `make-stopwords.py`: Build a stopword list (Top 300 terms)
* `make_tagged_corpus.py`: Builds the corpus from the Tearma database, requires `morphology.xml`, the sorted list of term frequences constructed with `term_freqs-sort.tsv` and the Wikipedia corpus `gawiki-filt.gz` (see below)
* `pos-to-terms.py`: Convert a POS-tagged corpus to an IOB-tagged corpus
* `process-elaines-data.py`: Used to extract the data from Elaine Ní Dhonnchadha's corpus. Please contact her for data.

### Wikipedia corpus

The Wikipedia corpus should be formatted with one article per line and the article title preceeding the article content separted by a `:`. Tokenization should alreayd hve been applied.
