#!/bin/env python

from PacMonSTR.alg import alignRegions
from PacMonSTR.extract_sequence import flank_seq

class Seq():
    def __init__(self,hap,seq):
        self.hap = hap
        self.seq = seq

        self.copies = None
        self.prefix_score = None
        self.suffix_score = None
        self.seq_score = None

    def genotype(self,prefix,suffix,motif):
        pass    
        # self.copies, scores = alignRegions(prefix,suffix,motif,self.seq)        
        # self.prefix_score,self.suffix_score,self.seq_score = scores
        
class Tr():
    def __init__(self,chrom,start,end,motif_seq,copies_in_ref):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.motif_seq = motif_seq
        self.copies_in_ref = copies_in_ref

        self.prefix = None
        self.suffix = None

        self.seqs = []

    def add_flanks(self,reffn,padding):
        prefix, suffix = flank_seq(reffn,self.chrom,self.start,self.end,padding)
        self.prefix = prefix
        self.suffix = suffix
        
    def add_overlapping_seq(self,hap,seq):
        self.seqs.append(Seq(hap,seq))

    def genotype_seqs(self):
        for seq in self.seqs:
            seq.genotype(self.prefix,self.suffix,self.motif_seq)
