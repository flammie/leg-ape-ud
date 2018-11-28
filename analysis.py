#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A container for analysis.

Contains single hypothesis of single aspect of things.
"""


class Analysis:
    """Contains a single analysis of a token.

    Analysis is a hypothesis of what token's some features may be:
    morphological analysis contains morphosyntactic readings and segmentation
    contains segment markers.
    """

    def __init__(self):
        """Create an empty analysis."""
        self.upos = None
        self.ufeats = dict()
        self.udepname = None
        self.udeppos = None
        self.misc = dict()
        self.weight = float("inf")
        self.analsurf = None
        self.lemmas = list()

    def get_upos(self):
        '''Finds UPOS from analyses.

        Returns:
            upos in a string
        '''
        return self.upos

    def get_lemmas(self):
        '''Finds lemmas from analyses.

        Returns:
            list of strings.
        '''
        return self.lemmas

    def get_ufeats(self):
        '''Finds UD Feats from analyses.

        Returns:
            dict of key value pairs of UD Feat column.
        '''
        return self.ufeats

    @staticmethod
    def fromape(ape: str):
        '''Constructs analysis from an apertium stream format string.

        Args:
            ape     An apertium analysis, i.e. `lemma<tags>`

        Returns:
            an analysis parsed into structured information
        '''
        a = Analysis()
        fields = [tag.strip('>') for tag in ape.split("<")]
        a.lemmas = fields[0].split('+')
        for f in fields:
            if f == 'n':
                a.upos = 'NOUN'
            elif f == 'adj':
                a.upos = 'ADJ'
            elif f == 'vblex':
                a.upos = 'VERB'
            elif f in ['vaux', 'vbser', 'vbmod', 'vbdo']:
                a.upos = 'AUX'
            elif f == 'cnjcoo':
                a.upos = 'CCONJ'
            elif f in ['cnjadv', 'cnjsub']:
                a.upos = 'SCONJ'
            elif f == 'ij':
                a.upos = 'INTJ'
            elif f == 'adv':
                a.upos = 'ADV'
            elif f in ['post', 'pp']:
                a.upos = 'ADP'
            elif f == 'pcle':
                a.upos = 'PART'
        return a

    def get_ud_misc(self):
        '''Get random collection of analyses for token.

        Primarily used for UD MISC field but can be used for any extra data.
        '''
        miscs = []
        if self.analsurf:
            miscs += ['AnalysisForm=' + self.analsurf]
        return miscs

    def printable_ud_misc(self):
        '''Formats UD misc like in UD data.'''
        miscs = self.get_ud_misc()
        if not miscs:
            return '_'
        return '|'.join(miscs)

    def printable_udepname(self):
        '''Format udep as string for CONLL-U.

        Returns:
            string of udep nam
        '''
        if self.udepname:
            return self.udepname
        else:
            return '_'

    def printable_udephead(self):
        '''Format udep head position for CONLL-U.

        Returns:
            string of non-ngative integer or _'''
        if self.udepname and self.udepname == 'root' and self.udeppos == 0:
            return '0'
        if self.udeppos:
            return str(self.udeppos)
        else:
            return '_'

    def printable_ud_feats(self):
        '''Formats UD feats from token data exactly as in UD.

        When the correct analysis is in question the result should be equal
        to the UFEAT field of the connl-u data downloadable from UD web site,
        in string format.

        Returns:
            string of |-separated key=value pairs in correct order or _
        '''
        rvs = self.ufeats
        if not rvs:
            return '_'
        rv = ''
        for k in sorted(rvs, key=str.lower):
            rv += k + '=' + rvs[k] + '|'
        return rv.rstrip('|')

    def is_oov(self):
        '''Figures out if this analysis was guessed for an OOV.'''
        return False
