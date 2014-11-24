#!/usr/bin/env python

import subprocess
import commands
import cgi
import os
import re
import random
import string
import cgitb; cgitb.enable()

'''
Authors: Kaya Thomas and Ridwan Hassen

This script creates a website that uses 
carmel to display random sentences and a 
random poem.
'''

print "Content-type: text/html"
print 
print "<html><head>"
print "<title>Poetry and Sentence Generator"
print "</title>"
print "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.cs.dartmouth.edu/~sravana/classes/classes.css\">"
print "<style>"
print ".ttlarge{font-family: Courier; font-size: 12pt;}"
print ".box{height: 550px; float: left; border: 1px solid #cdcdcd; padding: 10px;}"
print "</style>"
print "</head><body style=\"padding: 20px;\">"

print "<h1>Poetry and Sentence Generator</h1>"
print "This is a final project by Kaya Thomas and Ridwan Hassen. You can have random poetic sentence or a full poem generated by the program.<p>"

form = cgi.FieldStorage()

fsm = ""
o = open("/net/tahoe3/kthomas/cs73/alphaonly.fsa", 'r')
for line in o:
    fsm += line

o.close()

fname1 = "alphaonly.fsa"
fname2 = 'rhyming.fsa'

print "<h2>Random Sentence Generator</h2>"

carmeloutput = commands.getoutput('/net/people/sravana/programs/carmel '+fname1)

carmeloutput = commands.getoutput('/net/people/sravana/programs/carmel -IWE -G '+'5'+' '+fname1).split('\n')
for li, line in enumerate(carmeloutput[3:]):
    print '<span class=\"ttlarge\">', line.replace('"', '')+'</span><br>'

print "<h2>Random Poem Generator</h2>"

carmeloutput = commands.getoutput('/net/people/sravana/programs/carmel '+fname2)

carmeloutput = commands.getoutput('/net/people/sravana/programs/carmel -IWE -G '+'1'+' '+fname2).split('/n')

i = 10
for li, line in enumerate(carmeloutput[3:]):
    print '<span class=\"ttlarge\">', line.replace('"', '')+'</span><br>'
    i -= 1
    if i == 0:
    	break
    	
print "<div style=\"clear: both;\"></div>"
print "</body></html>"