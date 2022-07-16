[<- Back to course](https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/dict/course/CS50-HarvardX/CS50AI/README.md)

<p align="center"><a href="https://cs50.harvard.edu/ai/2020">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/course/harvard100.png" /><br>
</a></p>
<h1 align="center">CS50’s Introduction to Artificial Intelligence with Python<br><br>PageRank</h1>

<p align="center"><a href="#">
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/python.png" />
  <img src="https://github.com/GrandEchoWhiskey/grandechowhiskey/blob/main/icons/programming/html.png" />
</a></p>

### Background:
When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. But how does the search engine know which pages are more important than other pages?

One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage. We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.

But this definition isn’t perfect: if someone wants to make their page seem more important, then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.

For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. 

### Getting Started:
Clone this repository.
```
git clone https://github.com/GrandEchoWhiskey/harvard-cs50-ai-pagerank
```
Now run the program.
```
python pagerank.py corpus
```
For example:
```
python pagerank.py corpus0
```
