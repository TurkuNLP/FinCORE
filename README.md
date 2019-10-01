# Finnish Corpus of Online REgisters (FinCORE)

This repository contains the Finnish Corpus of Online REgisters (FinCORE)
data introduced in the paper
[Toward Multilingual Identification of Online Registers](https://www.aclweb.org/anthology/W19-6130/) ([pdf](https://www.aclweb.org/anthology/W19-6130)).

FinCORE annotations are licensed under
[CC BY](http://creativecommons.org/licenses/by-sa/4.0/).

The software introduced in the paper is available from
<https://github.com/spyysalo/multiling-cnn>.

## Format

The annotated texts are found in the files `train.tsv`, `dev.tsv` and
`test.tsv` in the `data/` subdirectory in a simple TSV format where each
line has the format `LABEL<TAB>TEXT`.

## Quickstart

To format the data for fastText, run

```
mkdir fasttext
for f in data/{train,dev,test}.tsv; do
    perl -pe 's/^(.*?)\t/__label__$1 /' $f > fasttext/$(basename $f .tsv).ft
done
```

Download Finnish MUSE word vectors

```
wget https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi.fi.vec
```

Train fastText, predict label probabilities for test data

```
fasttext supervised -epoch 10 -pretrainedVectors wiki.multi.fi.vec -dim 300 \
    -input fasttext/train.ft -output fasttext.model
fasttext predict-prob fasttext.model.bin fasttext/test.ft 6 > probs.txt
```

Evaluate

```
python scripts/auc.py fasttext/test.ft probs.txt
```
