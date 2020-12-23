#!/bin/env python
import sys

from PacMonSTR.alg import run_pacmonstr_alg
from PacMonSTR.extract_sequence import flank_seq

class Seq():
    def __init__(self,hap,seq):
        self.hap = hap
        self.seq = seq

        self.copies = None
        self.prefix_score = None
        self.suffix_score = None
        self.seq_score = None

    def test_code(self):
        prefix = "ACG"
        suffix = "AGA"
        motif = "TCC"
        print run_pacmonstr_alg(prefix,suffix,motif,self.seq)
        
    def genotype(self,prefix,suffix,motif):
        self.copies, scores = run_pacmonstr_alg(prefix,suffix,motif,self.seq)        
        self.prefix_score,self.suffix_score,self.seq_score = scores

    def __str__(self):
        out = [self.hap,self.copies,self.prefix_score,self.suffix_score,self.seq_score]
        return "\t".join(map(str,out))
        
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

    def __str__(self):
        out = [self.chrom,self.start,self.end,self.motif_seq,self.copies_in_ref]
        for seq in self.seqs:
            out.append(seq.__str__())
        return "\t".join(map(str,out))

def test():
    s = Seq("1","ACGTCCTCCAGA")
    s.test_code()
    sys.exit()
    
#test()
