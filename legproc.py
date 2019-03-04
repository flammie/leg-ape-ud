#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A command-line interface for LEG processor."""

# string munging
from argparse import ArgumentParser, FileType
# CLI stuff
from sys import stdin, stdout
# statistics
from time import perf_counter, process_time

from disamparsulator import Disamparsulator
from sentence import Sentence


def main():
    """Invoke a simple CLI analyser."""
    a = ArgumentParser()
    a.add_argument('-i', '--input', metavar="INFILE", type=open,
                   dest="infile", help="source of analysis data")
    a.add_argument('-v', '--verbose', action='store_true',
                   help="print verbosely while processing")
    a.add_argument('-o', '--output', metavar="OUTFILE", dest="outfile",
                   help="print output into OUTFILE", type=FileType('w'))
    a.add_argument('-x', '--statistics', metavar="STATFILE", dest="statfile",
                   help="print statistics to STATFILE", type=FileType('w'))
    a.add_argument('--not-rules', metavar="RULEFILE", type=open, required=True,
                   help="read non-rules from RULEFILE")
    a.add_argument('--giella', default=False, action='store_true',
                   help="use giella instead of ape parsing")
    a.add_argument('--debug', action='store_true',
                   help="print lots of debug info while processing")
    options = a.parse_args()
    if options.verbose:
        print("Printing verbosely")
    disamparsulator = Disamparsulator()
    if options.not_rules:
        if options.verbose:
            print("Loading", options.not_rules)
        disamparsulator.frobblesnizz(options.not_rules)
    else:
        print("Disamparsulate must frobblesnizz")
        exit(4)
    if not options.infile:
        print("reading from <stdin>")
        options.infile = stdin
    if options.verbose:
        print("analysing", options.infile.name)
    if not options.outfile:
        options.outfile = stdout
    if options.verbose:
        print("writing to", options.outfile.name)
    if not options.statfile:
        options.statfile = stdout

    # statistics
    realstart = perf_counter()
    cpustart = process_time()
    tokens = 0
    unknowns = 0
    sentences = 0
    for line in options.infile:
        sent = {'text': None}
        if options.giella:
            sent = Sentence.fromapeline(line.strip(), reformat="giella")
        else:
            sent = Sentence.fromapeline(line.strip())
        if sent.text:
            sentences += 1
            sent.id = options.infile.name + "." + str(sentences)
            disamparsulator.linguisticate(sent)
            if not options.debug:
                print(sent.printable_conllu(), file=options.outfile)
            else:
                print("DEBG")
                print(sent.printable_ambigonllu(), file=options.outfile)
    cpuend = process_time()
    realend = perf_counter()
    print("Tokens:", tokens, "Sentences:", sentences,
          file=options.statfile)
    print("Unknowns / OOV:", unknowns, "=",
          unknowns / tokens * 100 if tokens != 0 else 0,
          "%", file=options.statfile)
    print("CPU time:", cpuend - cpustart, "Real time:", realend - realstart,
          file=options.statfile)
    print("Tokens per timeunit:", tokens / (realend - realstart),
          file=options.statfile)
    print("Sentences per timeunit:", sentences / (realend - realstart),
          file=options.statfile)
    exit(0)


if __name__ == "__main__":
    main()
