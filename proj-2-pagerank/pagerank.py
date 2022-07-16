import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    result = dict()
    pages = corpus.keys()
    links = corpus[page]

    # When no links, make it even probability
    if len(links) <= 0:
        for key in pages:
            result[key] = 1 / len(pages)

        return result

    # Create weighted dictionary
    for key in pages:

        # Assign the random propability factor
        result[key] = (1 - damping_factor) / len(pages)

        # When key is also in links add the propability for the link
        if key in links:
            result[key] += (damping_factor / len(links))

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Copy keys and zero values into samples variable
    samples = corpus.copy()
    for key in samples:
        samples[key] = 0

    sample_key = None
    for _ in range(n):

        # When key is not assigned get a random key and continue loop
        if sample_key is None:
            sample_key = random.choice(list(corpus.keys()))
            samples[sample_key] += 1
            continue

        # When key assigned transition model, and create lists for keys and weights
        distr = transition_model(corpus, sample_key, damping_factor)
        distr_sites = list(distr.keys())  # [key for key in distr.keys()]
        distr_weights = list(distr.values())  # [distr[key] for key in distr]

        # Get weighted random list item
        # random.choice does not take a weights list input, so using random.choices this time
        sample_key = random.choices(distr_sites, distr_weights, k=1)[0]
        samples[sample_key] += 1

    # Divide all samples so sum will be 1
    for key in samples:
        samples[key] /= n

    return samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Assign equal probability
    d_current = dict()
    for key in corpus:
        d_current[key] = 1 / len(corpus)

    while True:

        # For each page get a new rank value based on the current
        d_new = dict()
        for key in corpus:
            d_new[key] = calc_rank(corpus, key, damping_factor, d_current)

        # When convergence return
        if max([abs(d_new[key] - d_current[key]) for key in d_current]) < 0.001:
            return d_current

        # Make the new dictionary as the current, and repeat the loop with it
        d_current = d_new.copy()


def calc_rank(corpus, page, damping_factor, dictionary):
    """
    Helper Function - calculate new rank value based on the current
    """

    result = 0

    for key in corpus:

        # When page has no links - link to each page equally
        if len(corpus[key]) == 0:
            result += (dictionary[key] / len(corpus))

        # When page is in page links - add the link probability
        if page in corpus[key]:
            result += (dictionary[key] / len(corpus[key]))

    # Multiply by damping factor and add the random factor
    result *= damping_factor
    result += (1 - damping_factor) / len(corpus)

    return result


if __name__ == "__main__":
    main()
