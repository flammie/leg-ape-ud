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
        fields = ape.replace('///', '@SLASH@/@SLASH@').split('/')
        token = Token(fields[0].lstrip('^'))
        for field in fields[1:]:
            analysis = Analysis.fromape(field.rstrip('$'))
            token.analyses.append(analysis)
        return token

    def printable_conllu(self):
        '''Create CONLL-U output based on token's 1-best analysis.'''
        lemma = self.surf
        upos = 'X'
        third = '_'
        ud_feats = '_'
        ud_misc = '_'
        dephead = '_'
        depname = '_'
        anal = self.get_best()
        if anal:
            upos = anal.get_upos()
            third = upos
            lemmas = anal.get_lemmas()
            if lemmas:
                lemma = '#'.join(lemmas)
            else:
                lemma = self.surf
            ud_feats = anal.printable_ud_feats()
            ud_misc = anal.printable_ud_misc()
            depname = anal.printable_udepname()
            dephead = anal.printable_udephead()
        return "\t".join([str(self.pos), self.surf, lemma, upos, third,
                          ud_feats, dephead, depname, "_", ud_misc])

    def printable_ambigonllu(self):
        '''Create ambiguous CONLL-U-style output based on token.'''
        lines = []
        for anal in self.analyses:
            lemma = self.surf
            upos = 'X'
            third = '_'
            ud_feats = '_'
            ud_misc = '_'
            dephead = '_'
            depname = '_'
            if anal:
                upos = anal.get_upos()
                third = upos
                lemmas = anal.get_lemmas()
                if lemmas:
                    lemma = '#'.join(lemmas)
                else:
                    lemma = self.surf
                ud_feats = anal.printable_ud_feats()
                ud_misc = anal.printable_ud_misc()
                depname = anal.printable_udepname()
                dephead = anal.printable_udephead()
            lines += ["\t".join([str(self.pos), self.surf, lemma, upos, third,
                                 ud_feats, dephead, depname, "_", ud_misc])]
        return '\n'.join(lines)

    def get_nbest(self, n: int):
        """Get n most likely analyses.

        Args:
            n: number of analyses, use 0 to get all

        Returns:
            At most n analyses of given type or empty list if there aren't any.
        """
        nbest = []
        worst = -1.0
        if n == 0:
            n = 65535
        for anal in self.analyses:
            if len(nbest) < n:
                nbest.append(anal)
                # when filling the queue find biggest
                if anal.weight > worst:
                    worst = anal.weight
            elif anal.weight < worst:
                # replace worst
                for i, a in enumerate(nbest):
                    if a.weight == worst:
                        nbest[i] = anal
                worst = -1.0
                for a in nbest:
                    if a.weight > worst:
                        worst = a.weight
        return nbest

    def get_best(self):
        """Get most likely analysis.

        Returns:
            most probably analysis of given type, or None if analyses have not
            been made for the type.
        """
        nbest1 = self.get_nbest(1)
        if nbest1:
            return nbest1[0]
        else:
            return None
