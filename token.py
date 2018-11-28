#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Support functions for handling tokens.
"""

from analysis import Analysis


class Token:
    """Token is a surface form, list of analyses and many other things."""

    def __init__(self, surf=None):
        """Create token with surface string optionally."""
        self.analyses = []
        self.surf = surf
        self.pos = 0
        self.spacebefore = False
        self.spaceafter = False

    @staticmethod
    def fromape(ape):
        '''Create a token by converting apertium stream format.

        A token in apertium stream format is a string starting with a
        circumflex accent and ending in a dollar sign.
        '''
        if not ape.startswith('^') or not ape.endswith('$'):
            print("Not a token in ape stream:", ape)
            return None
        fields = ape.split('/')
        token = Token(fields[0].lstrip('^'))
        for field in fields[1:]:
            analysis = Analysis.fromape(field)
            token.analyses.append(analysis)
        return token

    def printable_conllu(self):
        '''Create CONLL-U output based on token and selected analysis.'''
        lemma = self.surf
        upos = 'X'
        third = '_'
        ud_feats = '_'
        ud_misc = '_'
        anal = self.analyses[0]
        if anal:
            upos = anal.get_upos()
            third = upos
            lemmas = anal.get_lemmas()
            if lemmas:
                lemma = '#'.join(lemmas)
            ud_feats = anal.printable_ud_feats()
            ud_misc = anal.printable_ud_misc()
            depname = anal.printable_udepname()
            dephead = anal.printable_udephead()
        return "\t".join([str(self.pos), self.surf, lemma, upos, third,
                          ud_feats, dephead, depname, "_", ud_misc])
