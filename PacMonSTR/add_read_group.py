#!/bin/env python
import sys
import pysam

inbamfile = sys.argv[1]
outbamfile = sys.argv[2]

insamfile = pysam.AlignmentFile(inbamfile,'rb')
outsamfile = pysam.AlignmentFile(outbamfile,'wb',template=insamfile)

def add_read_group(read):
    read_tags = read.get_tags()
    tags_to_add = []
    for tag in read_tags:
        if tag[0] != "RG":
            tags_to_add.append(tag)
    haptag = ("RG", str(0), "Z")
    tags_to_add.append(haptag)
    read.set_tags(tags_to_add)
    return read
    
for read in insamfile.fetch():
    if read.is_secondary:
        continue
    if read.is_unmapped:
        continue
    if read.is_supplementary:
        continue
    out_read = add_read_group(read)
    outsamfile.write(out_read)

insamfile.close()
outsamfile.close()
