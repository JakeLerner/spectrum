#The Political Spectrum Project

## Idea - Politics in N-Dimensional Space

This project is largely influenced by the "ideology analysis" of senators and congressmen available at govtrack.us. A full description of that analysis is available [here](https://www.govtrack.us/about/analysis#ideology), but the essential feature of the visualization is to find similarities between candidates based on co-sponsorship records across all bills, and use some smart linear algebra (specifically, a singular value decomposition) to turn those similarities into a one dimensional spectrum which shows quantitatively how 'left' or 'right' a given legislator might be.


Govtrack's tool is great for visualizing the political spectrum and where individual polticians fall upon it, but politics is more complex than just a simple left-right spectrum.

Another, slightly more nuanced map of political space is [Political Compass](http://www.politicalcompass.org/).This site places politicians in two dimensional space, with the x axis representing degree of government involvement in economic affairs, and the y axis representing degree of government involvement in social affairs.

Political Compass provides a much more nuanced map of political space, by adding an extra dimension, but political stances are more complex than a point in two dimensional space.

For example, two American Democrats might share viewpoints on government involvement in social and economic life, but have vastly different takes on American foreign policy - one, 'hawkish' might support, say, intervention in Syria, while another, 'dovish' might always support diplomatic rather than military policy. Similarly, one Neoliberal might favor a cap-and-trade scheme to save the environment through market mechanisms, while another might favor striking environmental regulations across the board, Whooping Cranes be damned. 

Foreign interventionism and environmentalism are just a few examples, but they should give the flavor of the idea that politics is not one-dimensional or two-dimensional, but N-Dimensional. There are a huge number of 'spectrums' upon which we could group or delineate politicians. 

This project hopes to provide a tool to generate visualizations of politician stance across arbitrary spectrums, using the same quantitative cosponsor analysis as Govtrack's ideology analysis.

Specifically, given a keyword or set of keywords, the code fetches all bills from the current Congress containing a given keyword in their title from the Govtrack API. It then generates a cosponsor matrix from those bills, and renders this matrix in two dimensions using a Singular Value Decomposition. After re-scaling, this spectrum is plotted as the Y axis against overall cosponsorship values. Issues which track well to partisan beliefs would be expected to result in a strong correlation between issue specific and overall cosponsorship similarity. Outliers represent legislators who vote differently on the issue than the rest of their ideology might suggest.

## TODO:

- Fix Bug which marks peters, sullivan, gardner etc as Sanders-Left Independents
- Make list of bill titles visible
- Add command line options for house/senate and issue area
- Improve this Readme
- Clean up code
- Import bulk data into local SQL for wayyyy faster queries


## Design Problems
- Misses lots of important bills (from previous terms, with different wording)
- Includes some irrelevant bills (have word for different reason, not very important)
- Doesn't account for lots of nuances (committee politics, differing importance of bills)
- Small sample sizes for some issue areas

## How to play with it

To generate an image, just enter your desired search terms into the second to last line of govchart.py (command line support for this is on the to-do list), and run "python govchart.py" from the correct directory. As this queries the govtrack API, you need internet access. A spectrum of candidates along the issue area of your choice is about a coffee break away!