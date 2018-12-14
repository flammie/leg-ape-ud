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
        if self.upos:
            return self.upos
        else:
            return 'X'

    def get_lemmas(self):
        '''Finds lemmas from analyses.

        Returns:
            list of strings.
        '''
        if self.lemmas:
            return self.lemmas
        else:
            return ['_']

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
        if ape.startswith('*'):
            a.lemmas = [ape[1:]]
            a.upos = 'X'
            return a
        if '#' in ape:
            if ape.find('<') < ape.rfind('#'):
                # remove tags before compound boundaries for now
                ape = ape[0:ape.find('<')] + ape[ape.rfind('#'):]
        if '+' in ape:
            ape = ape.replace('+', '<')
        fields = [tag.strip('>') for tag in ape.split("<")]
        a.lemmas = fields[0].split('#')
        a.weight = len(a.lemmas) - 1.0
        for f in fields[1:]:
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
            elif f == 'np':
                a.upos = 'PROPN'
            elif f == 'prn':
                a.upos = 'PRON'
            elif f == 'num':
                a.upos = 'NUM'
            elif f == 'adv':
                a.upos = 'ADV'
            elif f in ['post', 'pp']:
                a.upos = 'ADP'
            elif f == 'pcle':
                a.upos = 'PART'
            elif f == 'punct':
                a.upos = 'PUNCT'
            elif f == 'sym':
                a.upos = 'SYM'
            elif f == 'sg':
                a.ufeats['Number'] = 'Sing'
            elif f == 'pl':
                a.ufeats['Number'] = 'Plur'
            elif f == 'nom':
                a.ufeats['Case'] = 'Nom'
            elif f == 'par':
                a.ufeats['Case'] = 'Par'
            elif f == 'gen':
                a.ufeats['Case'] = 'Gen'
            elif f == 'ill':
                a.ufeats['Case'] = 'Ill'
            elif f == 'ela':
                a.ufeats['Case'] = 'Ela'
            elif f == 'ade':
                a.ufeats['Case'] = 'Ade'
            elif f == 'abe':
                a.ufeats['Case'] = 'Abe'
            elif f == 'abl':
                a.ufeats['Case'] = 'Abl'
            elif f == 'ine':
                a.ufeats['Case'] = 'Ine'
            elif f == 'all':
                a.ufeats['Case'] = 'All'
            elif f == 'ess':
                a.ufeats['Case'] = 'Ess'
            elif f == 'tra':
                a.ufeats['Case'] = 'Tra'
            elif f == 'act':
                a.ufeats['Voice'] = 'Act'
            elif f == 'actv':
                a.ufeats['Voice'] = 'Act'
            elif f == 'pasv':
                a.ufeats['Voice'] = 'Pass'
            elif f == 'pri':
                a.ufeats['Tense'] = 'Present'
                a.ufeats['Mood'] = 'Ind'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'past':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['Mood'] = 'Ind'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'impv':
                a.ufeats['Mood'] = 'Imp'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'p1':
                a.ufeats['Person'] = '1'
            elif f == 'p2':
                a.ufeats['Person'] = '2'
            elif f == 'p3':
                a.ufeats['Person'] = '3'
            elif f == 'inf':
                a.ufeats['VerbForm'] = 'Inf'
            elif f == 'ger':
                a.ufeats['VerbForm'] = 'Ger'
            elif f == 'conneg':
                a.ufeats['Conneg'] = 'Yes'
            elif f == 'neg':
                a.ufeats['Polarity'] = 'Neg'
            elif f == 'pers':
                a.ufeats['PronType'] = 'Pers'
            elif f == 'dem':
                a.ufeats['PronType'] = 'Dem'
            elif f == 'rel':
                a.ufeats['PronType'] = 'Rel'
            elif f == 'indef':
                a.ufeats['PronType'] = 'Ind'
            elif f == 'ki':
                a.ufeats['Clitic'] = 'Ki'
            elif f == 'enc':
                pass
            elif f == 'ja':
                pass
            elif f in ['acr', 'abbr']:
                a.ufeats['Abbr'] = 'Yes'
            elif f == 'refl':
                a.ufeats['Reflex'] = 'Yes'
            elif f == 'pxsg1':
                a.ufeats['Person[psor]'] = '1'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'pxsg2':
                a.ufeats['Person[psor]'] = '2'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'pxsp3':
                a.ufeats['Person[psor]'] = '3'
            elif f == 'comp':
                a.ufeats['Cmp'] = 'Cmp'
            elif f == 'sup':
                a.ufeats['Cmp'] = 'Sup'
            elif f == 'cog':
                a.misc['PropnType'] = 'Cog'
            elif f == 'top':
                a.misc['PropnType'] = 'Top'
            elif f in ['interr', 'itg']:
                a.misc['PronType'] = 'Interr'
            elif f == 'al':
                a.misc['PropnType'] = 'Al'
            elif f == 'ant':
                a.misc['PropnType'] = 'Ant'
            elif f == 'f':
                a.misc['Gender'] = 'Female'
            elif f == 'm':
                a.misc['Gender'] = 'Male'
            else:
                print("unknown ape", f)
                exit(2)
        return a

    def get_ud_misc(self):
        '''Get random collection of analyses for token.

        Primarily used for UD MISC field but can be used for any extra data.
        '''
        miscs = []
        if self.analsurf:
            miscs += ['AnalysisForm=' + self.analsurf]
        if self.misc:
            miscs += [k + '=' + v for k, v in self.misc.items()]
        if self.weight != float('inf'):
            miscs += ['Weight=' + str(self.weight)]
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
