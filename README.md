# PacMonSTR
## Intro
This is refactored code from ```https://github.com/alibashir/pacmonstr``` containing only code corresponding to the dynamic programming (modified Smith–Waterman) algorithm used to count tandem repeat motifs from:
```
A. Ummat, A. Bashir, Resolving complex tandem repeats with long reads. Bioinformatics. 30, 3491–3498 (2014).
```

## Quick start
```
git clone https://github.com/oscarlr/PacMonSTR.git
python setup.py install

pacmonstr test/test.bam test/test.bed test/test_ref.fasta test/out.bed
```

