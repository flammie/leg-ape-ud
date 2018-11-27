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

    def printable_conllu(self, which="1random"):
        '''Create CONLL-U output based on token and its analyses.'''

    def printable_conllu(self, hacks=None, which="1best"):
        '''Create CONLL-U output based on token and selected analysis.'''
        if self.nontoken:
            if self.nontoken == 'error':
                return "# ERROR:" + self.error
            elif self.nontoken == 'comment':
                if self.comment.startswith('#'):
                    return self.comment
                else:
                    return '# ' + self.comment
            elif self.nontoken == 'separator':
                # not returning \n since the it's already printed on a line
                return ''
            else:
                # ignore other nontokens??
                return ''
        lemma = self.surf
        upos = 'X'
        third = '_'
        ud_feats = '_'
        ud_misc = '_'
        anal = self._select_anal(which)
        if anal:
            upos = anal.get_upos()
            if hacks and hacks == 'ftb':
                third = anal.get_xpos_ftb()
            else:
                third = anal.get_xpos_tdt()
            lemmas = anal.get_lemmas()
            if lemmas:
                lemma = '#'.join(lemmas)
            ud_feats = anal.printable_ud_feats()
            ud_misc = anal.printable_ud_misc()
            depname = anal.printable_udepname()
            dephead = anal.printable_udephead()
        return "\t".join([str(self.pos), self.surf, lemma, upos, third,
                          ud_feats, dephead, depname, "_", ud_misc])

    def printable_ftb3(self, which="1best"):
        '''Create FTB-3 output based on token and selected analysis.'''
        if self.nontoken:
            if self.nontoken == 'error':
                return "# ERROR:" + self.error
            elif self.nontoken == 'comment':
                if self.comment.startswith('#'):
                    return self.comment
                else:
                    return '# ' + self.comment
            elif self.nontoken == 'separator':
                # not returning \n since the it's already printed on a line
                return ''
            else:
                # ignore other nontokens??
                return ''
        lemma = self.surf
        pos = '_'
        feats = '_'
        anal = self._select_anal(which)
        if anal:
            pos = anal.get_xpos_ftb()
            lemmas = anal.get_lemmas()
            if lemmas:
                lemma = '#'.join(lemmas)
            feats = anal.printable_ftb_feats()
        return '\t'.join([str(self.pos), self.surf, lemma, pos, pos, feats,
                          '_', '_', '_', '_'])

    def _get_nbest(self, n: int, anals: list):
        nbest = []
        worst = -1.0
        if n == 0:
            n = 65535
        for anal in anals:
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

    def get_nbest(self, n: int):
        """Get n most likely analyses.

        Args:
            n: number of analyses, use 0 to get all

        Returns:
            At most n analyses of given type or empty list if there aren't any.
        """
        return self._get_nbest(n, self.analyses)

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

    def get_best_segments(self):
        """Get most likely segmentation.

        Returns:
            list of strings each one being a morph or other sub-word segment.
        """
        nbest1 = self._get_nbest(1, self.segmentations)
        if nbest1:
            return nbest1[0]
        else:
            return None
