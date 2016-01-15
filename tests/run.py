#!/usr/bin/python

"""
Copyright (C) 2015  Luiz Oliveira

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import unittest
from subprocess import call


class TestBot(unittest.TestCase):

    def test_call_bot(self):
        self.assertEqual(call(['bot-test', 'telegram', 'bot']), 0)


def runtests():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
