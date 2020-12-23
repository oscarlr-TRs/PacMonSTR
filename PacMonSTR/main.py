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
    start = max(1,tr.start - padding)
    end = tr.end + padding
    hap_seqs = hap_seq(bam,tr.chrom,start,end)
    for hap in hap_seqs:
        for seq in hap_seqs[hap]:
            tr.add_overlapping_seq(hap,seq)
            tr.genotype_seqs()
    return tr
            
def main():
    parser = argparse.ArgumentParser(description='Genotype TRs')
    parser.add_argument('bam',
                        help='Alignments with read groups for haps')
    parser.add_argument('bed',
                        help='BED file with TRs')
    parser.add_argument('ref',
                        help='Fasta file with reference')
    parser.add_argument('outbed')
    parser.add_argument('--padding',default=1000,
                        help='Padding added to input BED')
    args = parser.parse_args()

    header = [
        "chrom",
        "start",
        "end",
        "motif",
        "copies_in_ref",
        "hap0_avg",
        "hap0_max",
        "hap0_copies",
        "hap0_prefix_scores",
        "hap0_suffix_scores",
        "hap0_motif_scores",
        "hap1_avg",
        "hap1_max",
        "hap1_copies",
        "hap1_prefix_scores",
        "hap1_suffix_scores",
        "hap1_motif_scores",
        "hap2_avg",
        "hap2_max",
        "hap2_copies",
        "hap2_prefix_scores",
        "hap2_suffix_scores",
        "hap2_motif_scores"
        ]

    with open(args.outbed,'w') as outfh:
        outfh.write("%s\n" % "\t".join(header))
        with open(args.bed,'r') as infh:
            for line in infh:
                tr = genotype_tr(line,args.ref,args.padding,args.bam)
                outfh.write("%s\n" % tr)
