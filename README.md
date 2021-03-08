# PacMonSTR
## Intro
This is refactored code from ```https://github.com/alibashir/pacmonstr``` containing only code corresponding to the dynamic programming (modified Smith–Waterman) algorithm used to count tandem repeat motifs in long reads from:
```
A. Ummat, A. Bashir, Resolving complex tandem repeats with long reads. 
Bioinformatics. 30, 3491–3498 (2014).
```

## Quick start
```
conda create -n str python=2.7
conda activate str

git clone https://github.com/oscarlr/PacMonSTR.git
cd PacMonSTR

conda install cython
conda install numpy
conda install biopython
conda install pysam

python setup.py install

## test/test.bam is phased. The read groups have an "1" and "2" annotation specifying the haplotypes
pacmonstr test/test.bam test/test.bed test/ref.fa test/out.bed

## test/test_unphased.bam does not have read group annotations.
python PacMonSTR/add_read_group.py test/test_unphased.bam test/test_unphased_with_rg.bam
samtools index test/test_unphased_with_rg.bam
pacmonstr test/test_unphased_with_rg.bam test/test.bed test/ref.fa test/out.bed
```

## Required packages
```
python/2.7
cython
numpy
biopython
pysam
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

If the alignment BAM file does have a read group tag, then the tag "0" can be added to the bam file using the script `PacMonSTR/add_read_group.py`, for example:
```
python PacMonSTR/add_read_group.py \
  alignment_sorted.bam \
  alignment_sorted_with_rg.bam
```
### BED file
The bed file must contain 6 columns:
```
1. chrom
2. start
3. end
4. motif size
5. motif sequence
6. copies of motif in the reference
```

## Output
The output is a 23 columned BED file:
```
1. chrom
2. start
3. end
4. motif
5. copies_in_ref
6. hap0_avg
7. hap0_max
8. hap0_copies
9. hap0_prefix_scores
10. hap0_suffix_scores
11. hap0_motif_scores
12. hap1_avg
13. hap1_max
14. hap1_copies
15. hap1_prefix_scores
16. hap1_suffix_scores
17. hap1_motif_scores
18. hap2_avg
19. hap2_max
20. hap2_copies
21. hap2_prefix_scores
22. hap2_suffix_scores
23. hap2_motif_scores
```
Since there could be multiple reads overlapping the tandem repeat, PacMonSTR reports the average and max copies as well as all the copies found across all the reads. The alignment score for each part of the alignment is also reported.
