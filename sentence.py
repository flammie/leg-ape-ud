#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Support functions for handling sentences.
"""
from token import Token
from analysis import Analysis


class Sentence:
    """A sentence is a list of tokens, an id and a text."""

    def __init__(self):
        """Create an empty sentence."""
        self.tokens = []
        self.id = ""
        self.text = ""

    @staticmethod
    def fromapestream(s: str):
        """Creates sentence from apertium stream format string."""
        sentence = Sentence()
        apes = s.split("$")
        pos = 1
        for ape in apes:
            ape = ape.strip('^')
            fields = ape.split('/̈́')
            token = Token(fields[0])
            token.pos = pos
            for field in fields[1:]:
                if field.startswith('*'):
                    pass
                else:
                    analysis = Analysis.fromape(field)
                    token.analyses.append(analysis)
            sentence.tokens.append(token)
        return sentence

    def printable_conllu(self):
        '''Create CONLL-U from sentence.'''
        conllu = ""
        if self.id:
            conllu += "# sent-id: " + self.id + "\n"
        if self.text:
            conllu += "# text: " + self.text + "\n"
