#!/bin/env python
import sys
import argparse

from PacMonSTR.trs import Tr
from PacMonSTR.extract_sequence import hap_seq

def create_tr(line):
    line = line.rstrip().split('\t')
    chrom = line[0]
    start = int(line[1])
    end = int(line[2])
    motif_seq = line[4]
    if "/" in motif_seq:
        motif_seq = motif_seq.split("/")[0]
    copies_in_ref = line[5]
    tr = Tr(chrom,start,end,motif_seq,copies_in_ref)
    return tr

def genotype_tr(line,ref,padding,bam):
    tr = create_tr(line)
    tr.add_flanks(ref,padding)
    hap_seqs = hap_seq(bam,tr.chrom,tr.start,tr.end,padding)
    for hap in hap_seqs:
        for seq in hap_seqs[hap]:
            tr.add_overlapping_seq(hap,seq)
            tr.genotype_seqs()
            
def main():
    parser = argparse.ArgumentParser(description='Genotype TRs')
    parser.add_argument('bam',
                        help='Alignments with read groups for haps')
    parser.add_argument('bed',
                        help='BED file with TRs')
    parser.add_argument('ref',
                        help='Fasta file with reference')
    parser.add_argument('--padding',default=1000,
                        help='Padding added to input BED')
    parser.add_argument('outdir')
    args = parser.parse_args()

    with open(args.bed,'r') as fh:
        for line in fh:
            genotype_tr(line,args.ref,args.padding,args.bam)
