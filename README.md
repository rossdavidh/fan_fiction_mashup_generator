# fan_fiction_mashup_generator
generates ideas for fan fiction mashups, e.g. 
"When The Jeffersons and Star Wars played a hard-fought game of Calvinball, with a Greek chorus"
"Star Trek and Swamp Thing face a zombie apocalypse, as a Choose Your Own Adventure paperback"
"Paul Bunyan and Steven Universe Travel Through Time, a dadaist retelling"
etc.

To use, at the command line in the same directory as this repo, type:
python fan_fiction_idea_generator.py

Your idea will pop up on the terminal.  Feel free to create as many as you like, but at some
point you will get the message back:

"the file mashup_used_today.csv looks pretty full, especially for...[something]"
When this happens, just do:

rm mashup_used_today.csv

...and continue.  This csv file is how we prevent it getting in a rut where it keeps suggesting
'Charles Darwin' for one of the characters, or 'Marooned on an Island' for the scenario, etc.
This does mean that the program will need write permission for the directory it lives in, btw.
