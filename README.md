#The Political Spectrum Project

## Idea - Politics in N-Dimensional Space

This project is largely influenced by the "ideology analysis" of senators and congressmen available at govtrack.us. A full description of that analysis is available [here](https://www.govtrack.us/about/analysis#ideology), but the essential feature of the visualization is to find similarities between candidates based on co-sponsorhip records across all bills, and use some smart linear algebra to turn those similarities into a one dimensional spectrum to show quantitatively how 'left' or 'right' a given legislator might be.


Govtrack's tool is great for visualizing the political spectrum and where individual polticans fall upon it. But politics is more complex than just a simple left-right spectrum.

Another, slightly more nuanced map of political space is [Political Compass](http://www.politicalcompass.org/).This site places politicians in two dimensional space, with the x axis representing degree of government involvement in economic affairs, and the y axis representing degree of government involvement in social affairs.

But political stances are more complex than a point in two dimensional space.

For example two house democrats could have the exact same viewpoints on the government's involvement in social and economic life, but vastly different viewpoints on the government's involvement in international relations - one could be a hawk, and the other a dove. Similarly, two politicians could be very free-market, and believe in little control over the economy, but one could care deeply about the state of the environment, and create a cap-and-trade market through which the environment can be protected via market mechanisms, while another might favor removing all environmental regulations currently faced by corporations. 

Foreign interventionism and environmentalism are just a few examples, but they should give the flavor of the idea that politics is not one-dimensional or two-dimensional, but N-Dimensional. There are a huge number of 'spectrums' upon which we could group or delineate politicians. 

The political spectrum project hopes to provide a tool to generate visualizations of politician stance across arbitrary spectrums, using the same quantitative cosponsor analysis as Govtrack's ideology analysis.


## Method

This project (indeed, this readme) is very much a work in progress. This is a rough description of methodology as it stands right now:

- Finds all bills from the most recent congress containing some keyword in their description.
- Runs cosponsorship analysis on those bills
- Visualizes in comparison to cached overall cosponsorship analysis from govtrack
- If tracks well to parties or is genrally partisan issue, expect general diagonal line. However, outliers from this diagonal represent legislators who vote differently on the issue than the rest of their ideology might suggest.

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

## Conclusion

This doohicky is still pretty rough. It has some methodological flaws, some UI flaws, and (as you know if you've gotten this far in this readme) some documentation flaws. But I believe that it's still A) pretty fun and B) a valuable tool for expressing how nt all issues fall neatly along partisan lines, and presenting the idea that political beliefs or records might be expressed as N-dimensional vectors or points in N-dimensional space.