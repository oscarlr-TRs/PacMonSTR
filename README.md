# PacMonSTR
## Intro
This is refactored code from ```https://github.com/alibashir/pacmonstr``` containing only code corresponding to the dynamic programming (modified Smith–Waterman) algorithm used to count tandem repeat motifs in long reads from:
```
A. Ummat, A. Bashir, Resolving complex tandem repeats with long reads. 
Bioinformatics. 30, 3491–3498 (2014).
```

## Quick start
```
git clone https://github.com/oscarlr/PacMonSTR.git
python setup.py install

pacmonstr test/test.bam test/test.bed test/test_ref.fasta test/out.bed
```

## Manual
```
usage: pacmonstr [-h] [--padding PADDING] bam bed ref outbed

Genotype TRs

positional arguments:
  bam                Alignments with read groups for haps
  bed                BED file with TRs
  ref                Fasta file with reference
  outbed

optional arguments:
  -h, --help         show this help message and exit
  --padding PADDING  Padding added to input BED
  ```
## Inputs
### BAM file
The reads in the BAM file must contain read group tags "0","1" or "2". "1" and "2" correspond to haplotype 1 and haplotype 2. "0" are unphased reads.
### BED file
The bed file must contain 6 columns:
1. chrom
2. start
3. end
4. motif size
5. motif sequence
6. copies of motif in the reference

## Output
