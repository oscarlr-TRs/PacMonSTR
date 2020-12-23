#!/bin/env python
import sys
import pysam

def skip_read(read):
    skip = False
    if read.is_secondary:
        skip = True
    if read.is_supplementary:
        skip = True
    if read.is_unmapped:
        skip = True
    return skip

def query_coords(read,start,end):
    query_start = None
    query_end = None        
    ap = read.get_aligned_pairs()
    for q_pos, r_pos in ap:
        if q_pos == None:
            continue
        if r_pos == None:
            continue
        if r_pos <= start:
            query_start = q_pos
        query_end = q_pos
        if r_pos > end:
            break
    return (query_start,query_end)
        
def hap_seq(bam,chrom,start,end,flank):
    hap_sequences = {}
    read_sequence = None
    samfile = pysam.AlignmentFile(bam)
    for read in samfile.fetch(chrom,max(1,start),end + flank):
        if skip_read(read):
            continue
        hap = read.get_tag("RG",with_value_type=True)
        if hap not in hap_sequences:
            hap_sequences[hap] = []
        query_start,query_end = query_coords(read,start,end)
        read_sequence = read.query_sequence[query_start:query_end]        
        hap_sequences[hap].append(read_sequence)
    return hap_sequences

def flank_seq(reffn,chrom,start,end,flank):
    ref = pysam.FastaFile(reffn)
    prefix_seq = ref.fetch(chrom,max(1,start-flank),start)
    suffix_seq = ref.fetch(chrom,end,end+flank)
    return (prefix_seq,suffix_seq)
