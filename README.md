Poetry-Generator
================

A program that uses python scripts and Carmel, a finite state machine package to generate random sentences and poems.

# Running the program via UNIX

* grab a copy of the git repository
```
git clone https://github.com/kmt901/Poetry-Generator
```

Unzip neede_files.zip and save these files into one directory where the code is located.

You must have Python 2.7 on your machine and access to the Carmel toolkit to run the finite state acceptors.

# Random Sentence Generator

To create the random sentence finite state acceptor, cd into your directory where stateproducer.py, alphaonly.fsa, and textonly.bigrams.arpa are located.

On the command line, type:
```
python stateproducer.py
```
Once it is finished running the finite state acceptor will be finished in the alphaonly.fsa file. You need to edit the first line of the file. The first line should be 'end' which is the accept state for our finite state acceptor.

To test the finite state acceptor, ssh into the server that gives you access to the Carmel toolkit. Upload alphaonly.fsa to your server. On the command line type:
```
carmel -g 1 alphaonly.fsa
```

This will generate one random sentence.

# Random Poetry Generator

To create the random poem finite state acceptor, cd into your directory where rhyming.py, rhyming.fsa, cmudict.0.7a.txt and textonly.bigrams.arpa are located. Create a text file and name it dummy_start.txt, so you can store your dummy start state with uniform probabilities in this file. Save the file in the directory where all your files are located.

On the command line, type:
```
python rhyming.py
```

The program will run for a long time. It is up to you whether you want to let it run till the finish or stop it prematurely. Once it is finished or you stop it pressing down Control and C the finite state acceptor will be finished in the rhyming.fsa file. You need to edit the first line of the file. The first line should be 'end' which is the accept state for our finite state acceptor.

To test the finite state acceptor, ssh into the server that gives you access to the Carmel toolkit. Upload rhyming.fsa to your server. On the command line type:
```
carmel -g 1 rhyming.fsa
```

This will generate a poem, the sentences that are split by /n.

# CGI Website

In order to create a website that uses python scripts to run the Carmel toolkit you need server to host your site files. Upload the public_html folder to your server. Transfer the rhyming.fsa file to your cgi-bin folder. Test the webpage [here](www.cs.dartmouth.edu/cgi-bin/cgiwrap/kthomas/fsa.cgi) or on the webpage you uploaded your files. Give it time to load, the rhyming finite state acceptor is large.

