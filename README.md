# Yhdyssanageneraattori
A small tool that creates combined compound words.   
As an example, the words "tunneäly" and "älykääpiö" can be combined to "tunneälykääpiö"

### Results
Pre-generated results can be found in the output and output_loose folder.
The results are grouped to different files based on the length of the combining middle word.  
i.e. "tunne*äly*kääpiö" is found in the file output03.txt

The output_loose folder contains words where the other words aren't strictly compound words,
but they do match like in "paloautomaatti".

### Why?
The motivation for this script came from this old [vauva.fi post](https://www.vauva.fi/keskustelu/4211554/ketju/keksitaan_hauskoja_yhdyssanoja_tyyliin_lapsivesipuisto)

### Word list
The word list that was used is based on a wordlist from the [Institute for the Languages of Finland](http://kaino.kotus.fi/sanat/nykysuomi/) (Kotimaisten kielten keskus in Finnish, or KOTUS). I got it from this [Github repo](https://github.com/hugovk/everyfinnishword/) by [hugovk](https://github.com/hugovk)
