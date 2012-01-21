"""billboard.py - Fit fixed-width text on a billboard (Round 1)
"""
# Copyright 2012 Erich Blume <blume.erich@gmail.com>
# ===========================
#
# This file is part of fbhc
#
# fbhc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# fbhc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with fbhc, in a file called COPYING.  If not, see
# <http://www.gnu.org/licenses/>.

class Billboard:
    """Create a ``Billboard`` object to fit text in a limited space.

    `height` and `width` must be integers between 1 and 1000 (inclusive).

    >>> Billboard(20,6).set("hacker cup")
    3
    >>> Billboard(100,20).set("hacker cup 2013")
    10
    >>> Billboard(10,20).set("MUST BE ABLE TO HACK")
    2
    >>> Billboard(55,25).set("Can you hack")
    8
    >>> Billboard(100,20).set("Hack your way to the cup")
    7
    >>> Billboard(350,100).set("Facebook Hacker Cup 2013")
    33
    >>> Billboard(1,1).set("Too Much Text")
    0
    """
    
    def __init__(self,width,height):
        self.height = height
        self.width = width

    def set(self,text):
        """Fit (set) `text` (a string) to the billboard.

        Returns an integer, being the maximum size in inches for the font.

        Returns 0 if the text cannot be properly set.
        """
        # We will brute-force the solution (as this is simple and
        # time-effective) by checking every font size from the lesser of the
        # height or the width, down.
        #
        # Off the top of my head, there may be a faster algorithm that uses
        # genetic programming, but this solution is still linear and the
        # boundaries are small.
        
        for i in range(self.height if self.height < self.width else self.width,
                       1, -1):
            if self.check_size(i,text):
                return i

        return 0
        

    def check_size(self,size,text):
        """Return True if the text can be set without breaking a word."""
        # Note that the FB contraints specify that text will not start or end
        # with a space. If that constraint was broken, this algorithm would
        # strip off that space before setting it. This might produce an
        # unexpected result, but frankly I would think it is the preferable one.
        words = text.split()
        for row in range(int(self.height / size)):
            # 'consume' text for this row
            self.set_row(size,words)
            if not words:
                # If we consumed the last of text, then this fit.
                return True
        return False

    def set_row(self,size,words):
        """Consume words to fill a row without breaking any words.
        
        `words` must be a list (it must support ``pop(0)``).
        
        >>> b = Billboard(10,10) # height doesn't matter for this test
        >>> words = ['12345','67890']
        >>> b.set_row(1,words)
        >>> words
        ['67890']
        >>> words = ['1','2','3','4','5','6','7','8','9','0']
        >>> b.set_row(1,words)
        >>> words
        ['6', '7', '8', '9', '0']
        >>> words = ['1234567890']
        >>> b.set_row(1,words)
        >>> words
        []
        >>> words = ['12345','6']
        >>> b.set_row(2,words)
        >>> words
        ['6']
        
        """
        row = []
        while words:
            row.append(words[0])
            if len(" ".join(row)) > self.width / size:
                break
            words.pop(0)


