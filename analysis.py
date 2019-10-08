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
    def fromgiella(giella: str):
        '''Constructs analysis from an apertium stream format string. The
        analyses in ape stream format are in giella form however (e.g.
        someone's used hfst-proc on giella-langs).

        Args:
            giella     A giellatekno analysis, i.e. `lemma+tag+tag`

        Returns:
            an analysis parsed into structured information
        '''
        a = Analysis()
        if giella.startswith('*'):
            a.lemmas = [giella[1:]]
            a.upos = 'X'
            return a
        if '#' in giella:
            if giella.find('+') < giella.rfind('#'):
                # remove tags before compound boundaries for now
                giella = giella[0:giella.find('+')] +\
                        giella[giella.rfind('#'):]
        fields = giella.split("+")
        a.lemmas = fields[0].split('#')
        a.weight = len(a.lemmas) - 1.0
        for f in fields[1:]:
            if f == 'N':
                a.upos = 'NOUN'
            elif f == 'A':
                a.upos = 'ADJ'
            elif f == 'V-Aux':
                a.upos = 'AUX'
            elif f == 'V':
                a.upos = 'VERB'
            elif f == 'Conj':
                pass
            elif f == 'CC':
                a.upos = 'CCONJ'
            elif f == 'CS':
                a.upos = 'SCONJ'
            elif f == 'Interj':
                a.upos = 'INTJ'
            elif f == 'Prop':
                a.upos = 'PROPN'
            elif f == 'Pron':
                a.upos = 'PRON'
            elif f == 'Num':
                a.upos = 'NUM'
            elif f == 'Adv':
                a.upos = 'ADV'
            elif f == 'Det':
                a.upos = 'DET'
            elif f == 'Adp':
                a.upos = 'ADP'
            elif f == 'Pr':
                a.upos = 'ADP'
                a.ufeats['AdpType'] = 'Pre'
            elif f == 'Part':
                a.upos = 'PART'
            elif f in ['PUNCT', 'CLB']:
                a.upos = 'PUNCT'
            elif f == 'Sym':
                a.upos = 'SYM'
            elif f == 'Sg':
                a.ufeats['Number'] = 'Sing'
            elif f == 'Pl':
                a.ufeats['Number'] = 'Plur'
            elif f == 'Acc':
                a.ufeats['Case'] = 'Acc'
            elif f == 'Nom':
                a.ufeats['Case'] = 'Nom'
            elif f == 'Par':
                a.ufeats['Case'] = 'Par'
            elif f == 'Gen':
                a.ufeats['Case'] = 'Gen'
            elif f == 'Ill':
                a.ufeats['Case'] = 'Ill'
            elif f == 'Ela':
                a.ufeats['Case'] = 'Ela'
            elif f == 'Ade':
                a.ufeats['Case'] = 'Ade'
            elif f == 'Abe':
                a.ufeats['Case'] = 'Abe'
            elif f == 'Abl':
                a.ufeats['Case'] = 'Abl'
            elif f == 'Com':
                a.ufeats['Case'] = 'Com'
            elif f == 'Ine':
                a.ufeats['Case'] = 'Ine'
            elif f == 'Ins':
                a.ufeats['Case'] = 'Ins'
            elif f == 'All':
                a.ufeats['Case'] = 'All'
            elif f == 'Ess':
                a.ufeats['Case'] = 'Ess'
            elif f == 'Ter':
                a.ufeats['Case'] = 'Ter'
            elif f == 'Tra':
                a.ufeats['Case'] = 'Tra'
            elif f == 'Act':
                a.ufeats['Voice'] = 'Act'
            elif f == 'Pss':
                a.ufeats['Voice'] = 'Pass'
            elif f == 'Ind':
                a.ufeats['Mood'] = 'Ind'
            elif f == 'PrtPrc':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'Ger':
                a.ufeats['VerbForm'] = 'Ger'
            elif f == 'PrsPrc':
                a.ufeats['Tense'] = 'Pres'
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'Prs':
                a.ufeats['Tense'] = 'Pres'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'Prt':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'Imprt':
                a.ufeats['Mood'] = 'Imp'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'Cond':
                a.ufeats['Mood'] = 'Cnd'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'pprs':
                a.ufeats['Tense'] = 'Pres'
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'PrfPrc':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'Sg1':
                a.ufeats['Number'] = 'Sing'
                a.ufeats['Person'] = '1'
            elif f == 'Sg2':
                a.ufeats['Number'] = 'Sing'
                a.ufeats['Person'] = '2'
            elif f == 'Sg3':
                a.ufeats['Number'] = 'Sing'
                a.ufeats['Person'] = '3'
            elif f == 'Pl1':
                a.ufeats['Number'] = 'Plur'
                a.ufeats['Person'] = '1'
            elif f == 'Pl2':
                a.ufeats['Number'] = 'Plur'
                a.ufeats['Person'] = '2'
            elif f == 'Pl3':
                a.ufeats['Number'] = 'Plur'
                a.ufeats['Person'] = '3'
            elif f == 'Inf':
                a.ufeats['VerbForm'] = 'Inf'
            elif f == 'ger':
                a.ufeats['VerbForm'] = 'Ger'
            elif f in ['pp', 'pprs']:
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'ConNeg':
                a.ufeats['Connegative'] = 'Yes'
            elif f == 'Neg':
                a.ufeats['Polarity'] = 'Neg'
            elif f == 'Pers':
                a.ufeats['PronType'] = 'Prs'
            elif f == 'Dem':
                a.ufeats['PronType'] = 'Dem'
            elif f == 'rel':
                a.ufeats['PronType'] = 'Rel'
            elif f == 'indef':
                a.ufeats['PronType'] = 'Ind'
            elif f == 'PrsPrc':
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'Ger':
                a.ufeats['VerbForm'] = 'Ger'
            elif f == 'Pss':
                a.ufeats['Voice'] = 'Pass'
            elif f == 'Qst':
                a.ufeats['Clitic'] = 'Ko'
            elif f == 'ki':
                a.ufeats['Clitic'] = 'Ki'
            elif f == 'Err':
                a.ufeats['Typo'] = 'Yes'
            elif f in ['Apr', 'Rc', 'RcSg']:
                # XXX?
                pass
            elif f == 'Sem':
                pass
            elif f == 'Manner':
                pass
            elif f == 'Rel':
                a.ufeats['PronType'] = 'Rel'
            elif f in ['TYÄ', 'Err_Orth']:
                a.ufeats['Guess'] = 'Yes'
            elif f in ['Apr', 'Rc', 'RcSg', 'VR']:
                # XXX?
                pass
            elif f in ['LEFT', 'RIGHT']:
                # meh
                pass
            elif f == 'Der_mine':
                a.misc['Deriv'] = 'Mine'
            elif f in ['Sem_Plc', 'Der_Rc', 'Clt']:
                pass
            elif f in ['Manner', 'Spat']:
                pass
            elif f in ['acr', 'abbr']:
                a.ufeats['Abbr'] = 'Yes'
            elif f == 'Refl':
                a.ufeats['Reflex'] = 'Yes'
            elif f == 'Px1Sg':
                a.ufeats['Person[psor]'] = '1'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'Px2Sg':
                a.ufeats['Person[psor]'] = '2'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'Px3Sg':
                a.ufeats['Person[psor]'] = '3'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'PxSP3':
                a.ufeats['Person[psor]'] = '3'
            elif f == 'Px1Pl':
                a.ufeats['Person[psor]'] = '1'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'Px2Pl':
                a.ufeats['Person[psor]'] = '2'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'Px3Pl':
                a.ufeats['Person[psor]'] = '3'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'Comp':
                a.ufeats['Degree'] = 'Cmp'
            elif f == 'Sup':
                a.ufeats['Degree'] = 'Sup'
            elif f == 'Ord':
                a.ufeats['NumType'] = 'Ord'
            elif f == 'Card':
                a.ufeats['NumType'] = 'Card'
            elif f == 'cog':
                a.misc['PropnType'] = 'Cog'
            elif f == 'top':
                a.misc['PropnType'] = 'Top'
            elif f == 'Interr':
                a.misc['PronType'] = 'Interr'
            elif f == 'al':
                a.misc['PropnType'] = 'Al'
            elif f == 'ant':
                a.misc['PropnType'] = 'Ant'
            elif f == 'f':
                a.misc['Gender'] = 'Female'
            elif f == 'm':
                a.misc['Gender'] = 'Male'
            elif f == 'Temp':
                a.misc['PronType'] = 'Temp'
            elif f == 'x':
                a.upos = 'X'
            elif f in ['LEFT', 'RIGHT', 'VR']:
                pass
            else:
                print("unknown giella", f)
                exit(2)
        return a

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
            ape = ape.replace('+', '<+')
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
            elif f in ['post', 'pr']:
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
            elif f == 'com':
                a.ufeats['Case'] = 'Com'
            elif f == 'ine':
                a.ufeats['Case'] = 'Ine'
            elif f == 'ins':
                a.ufeats['Case'] = 'Ins'
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
                a.ufeats['Tense'] = 'Pres'
                a.ufeats['Mood'] = 'Ind'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'past':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['Mood'] = 'Ind'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'imp':
                a.ufeats['Mood'] = 'Imp'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'cni':
                a.ufeats['Mood'] = 'Cnd'
                a.ufeats['VerbForm'] = 'Fin'
            elif f == 'pprs':
                a.ufeats['Tense'] = 'Pres'
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'pp':
                a.ufeats['Tense'] = 'Past'
                a.ufeats['VerbForm'] = 'Part'
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
            elif f in ['pp', 'pprs']:
                a.ufeats['VerbForm'] = 'Part'
            elif f == 'conneg':
                a.ufeats['Connegative'] = 'Yes'
            elif f == 'neg':
                a.ufeats['Polarity'] = 'Neg'
            elif f == 'pers':
                a.ufeats['PronType'] = 'Prs'
            elif f == 'dem':
                a.ufeats['PronType'] = 'Dem'
            elif f == 'rel':
                a.ufeats['PronType'] = 'Rel'
            elif f == 'ind':
                a.ufeats['PronType'] = 'Ind'
            elif f == 'qst':
                a.ufeats['Clitic'] = 'Ko'
            elif f == '+ki':
                a.ufeats['Clitic'] = 'Ki'
            elif f == 'enc':
                pass
            elif f in ['+ja', '+mini']:
                #
                pass
            elif f in ['acr', 'abbr']:
                a.ufeats['Abbr'] = 'Yes'
            elif f == 'pos':
                a.ufeats['Possessive'] = 'Yes'
            elif f == 'refl':
                a.ufeats['Reflex'] = 'Yes'
            elif f == 'px1sg':
                a.ufeats['Person[psor]'] = '1'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'px2sg':
                a.ufeats['Person[psor]'] = '2'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'px3sg':
                a.ufeats['Person[psor]'] = '3'
                a.ufeats['Number[psor]'] = 'Sing'
            elif f == 'px3sp':
                a.ufeats['Person[psor]'] = '3'
            elif f == 'px1pl':
                a.ufeats['Person[psor]'] = '1'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'px2pl':
                a.ufeats['Person[psor]'] = '2'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'px3pl':
                a.ufeats['Person[psor]'] = '3'
                a.ufeats['Number[psor]'] = 'Plur'
            elif f == 'comp':
                a.ufeats['Degree'] = 'Cmp'
            elif f == 'sup':
                a.ufeats['Degree'] = 'Sup'
            elif f == 'ord':
                a.ufeats['NumType'] = 'Ord'
            elif f == 'card':
                a.ufeats['NumType'] = 'Card'
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
            elif f == 'x':
                a.upos = 'X'
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
