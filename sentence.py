#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Support functions for handling sentences.
"""
from token import Token


class Sentence:
    """A sentence is a list of tokens, an id and a text."""

    def __init__(self):
        """Create an empty sentence."""
        self.tokens = []
        self.id = ""
        self.text = ""

    @staticmethod
    def fromapeline(s: str):
        """Creates sentence from apertium stream format string.

        One sentence per line."""
        sentence = Sentence()
        apes = s.split("$")
        pos = 1
        text = ''
        for ape in apes:
            if ape.startswith(' ') and '^' in ape:
                text += ape[:ape.find('^')]
            ape = ape.lstrip()
            if ape.startswith('^'):
                token = Token.fromape(ape + '$')
                token.pos = pos
                sentence.tokens.append(token)
                pos += 1
                text += token.surf
            elif ape.strip() == '':
                pass
            else:
                print("Unrecognised ape", ape)
        sentence.text = text
        return sentence

    def printable_conllu(self):
        '''Create CONLL-U from sentence.'''
        conllu = ""
        if self.id:
            conllu += "# sent-id: " + self.id + "\n"
        if self.text:
            conllu += "# text: " + self.text + "\n"
        for token in self.tokens:
            conllu += token.printable_conllu() + '\n'
        return conllu
