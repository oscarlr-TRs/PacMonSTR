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

        self.genotyped = False
        
    def test_code(self):
        prefix = "ACG"
        suffix = "AGA"
        motif = "TCC"
        print run_pacmonstr_alg(prefix,suffix,motif,self.seq)
        
    def genotype(self,prefix,suffix,motif):
        self.copies, scores = run_pacmonstr_alg(prefix,suffix,motif,self.seq)        
        self.prefix_score,self.suffix_score,self.seq_score = scores
        if self.copies != None:
            self.copies = round(self.copies,2)
        if self.prefix_score != None:
            self.prefix_score = round(self.prefix_score,2)
        if self.suffix_score != None:
            self.suffix_score = round(self.suffix_score,2)
        if self.seq_score != None:
            self.seq_score = round(self.seq_score,2)
        if self.copies != None:
            self.genotyped = True
            
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
        
        self.seqs = {
            "0": [],
            "1": [],
            "2": []
        }

    def add_flanks(self,reffn,padding):
        prefix, suffix = flank_seq(reffn,self.chrom,self.start,self.end,padding)
        self.prefix = prefix
        self.suffix = suffix
        
    def add_overlapping_seq(self,hap,seq):
        self.seqs[hap].append(Seq(hap,seq))

    def genotype_seqs(self):
        for hap in self.seqs:
            for seq in self.seqs[hap]:
                seq.genotype(self.prefix,self.suffix,self.motif_seq)

    def get_copies(self,hap):
        copies = []
        for seq in self.seqs[hap]:
            if seq.genotyped:
                copies.append(seq.copies)
        if len(copies) == 0:
            copies = [None]
        return copies
        
    def average_copies(self,hap):
        copies = self.get_copies(hap)
        if copies[0] == None:
            return None
        sum_ = 0.0
        for copy in copies:
            sum_ += copy
        return sum_/len(copies)

    def max_copies(self,hap):
        copies = self.get_copies(hap)
        if copies[0] == None:
            return None
        return max(copies)

    def get_scores(self,hap):
        prefix_scores = []
        suffix_scores = []
        seq_scores = []
        for seq in self.seqs[hap]:
            if seq.genotyped:
                prefix_scores.append(seq.prefix_score)
                suffix_scores.append(seq.suffix_score)
                seq_scores.append(seq.seq_score)
        return (prefix_scores,suffix_scores,seq_scores)
                
    def get_prefix_scores(self,hap):
        prefix_scores = self.get_scores(hap)[0]
        if len(prefix_scores) == 0:
            return [None]
        return prefix_scores
        
    def get_suffix_scores(self,hap):
        suffix_scores = self.get_scores(hap)[1]
        if len(suffix_scores) == 0:
            return [None]
        return suffix_scores

    def get_seq_scores(self,hap):
        seq_scores = self.get_scores(hap)[2]
        if len(seq_scores) == 0:
            return [None]
        return seq_scores

    def __str__(self):
        out = [
            self.chrom,
            self.start,
            self.end,
            self.motif_seq,
            self.copies_in_ref
        ]

        for hap in ["0","1","2"]:
            avg = self.average_copies(hap)
            max_ = self.max_copies(hap)
            copies = ",".join(map(str,self.get_copies(hap)))
            prefix_scores = ",".join(map(str,self.get_prefix_scores(hap)))
            suffix_scores = ",".join(map(str,self.get_suffix_scores(hap)))
            seq_scores = ",".join(map(str,self.get_seq_scores(hap)))
            entries = [avg,max_,copies,prefix_scores,suffix_scores,seq_scores]
            for entry in entries:
                out.append(entry)

        return "\t".join(map(str,out))

def test():
    s = Seq("1","ACGTCCTCCAGA")
    s.test_code()
    sys.exit()
    
#test()
