#!/ust/bin/env python3

# Evaluate AUC for fastText outputs.

import sys
import os
import json

from sklearn.metrics import roc_auc_score


LABEL_STR = '__label__'


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('gold')
    ap.add_argument('pred')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])
    true_labels = []
    with open(args.gold) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            label, rest = l.split(' ', 1)
            if label.startswith(LABEL_STR):
                label = label[len(LABEL_STR):]
            true_labels.append(label)
    labels = set(true_labels)
    label_probs = []
    with open(args.pred) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            fields = l.split(' ')
            if len(fields) != 2 * len(labels):
                raise ValueError('expected {} fields on line {}: {}'.\
                                 format(2*len(fields), ln, l))
            label_prob = {}
            for i in range(len(labels)):
                label, prob = fields[2*i], fields[2*i+1]
                if label.startswith(LABEL_STR):
                    label = label[len(LABEL_STR):]
                prob = float(prob)
                label_prob[label] = prob
            label_probs.append(label_prob)
    aucs = []
    for label in labels:
        y_true = [l == label for l in true_labels]
        y_score = [label_prob[label] for label_prob in label_probs]
        auc = roc_auc_score(y_true, y_score)
        print('{} AUC:\t{:.4f}'.format(label, auc))
        aucs.append(auc)
    print('average AUC:\t{:.4f}'.format(sum(aucs)/len(labels)))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
