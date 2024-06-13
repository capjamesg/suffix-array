def suffix_array(text):
    return sorted([(text[i:], i) for i in range(0, len(text))])


with open("process.py", "r") as f:
    text = f.read()
    text = text.replace("\n", " ")

seq = suffix_array(text)

# implemented using https://en.wikipedia.org/wiki/Suffix_array#Example
def search(string_to_find, indexed_suffix_array):
    """Search the suffix array for all instances of a string."""
    start = 0
    end = len(indexed_suffix_array)

    while start < end:
        mid_point = (start + end) // 2

        if string_to_find > indexed_suffix_array[mid_point][0]:
            start = mid_point + 1
        else:
            end = mid_point

    end = len(indexed_suffix_array)
    init_start = start

    while start < end:
        mid_point = (start + end) // 2

        if indexed_suffix_array[mid_point][0].startswith(string_to_find):
            start = mid_point + 1
        else:
            end = mid_point

    return [indexed_suffix_array[i] for i in range(init_start, start)]


def get_n_concordance(string_to_find, indexed_suffix_array, n):
    """Retrieve the n letters after a string in the suffix array."""
    return [
        i[0][: n + len(string_to_find) + 1]
        for i in search(string_to_find, indexed_suffix_array)
    ]


def search_to_nearest_word(string_to_find, indexed_suffix_array, space_count=5):
    """Retrieve the next n words after the given subsequence, where n = space_count."""
    words = search(string_to_find, indexed_suffix_array)
    results = []

    for w in words:
        idx = 0
        chr = None
        has_found_space = 0
        while idx < len(w[0]) and has_found_space < space_count:
            chr = w[0][idx]
            idx += 1
            if chr == " ":
                has_found_space += 1

        # remove trailing space
        context = w[0][:idx][:-1]
        results.append(context)

    return results


def highlight_search_terms(text, results):
    """Highlight instances of the search term."""
    highlighted_results = []

    for r in results:
        chr = 0
        found = False

        while chr < len(r) and not found:
            if r[chr:].startswith(text):
                highlighted_results.append(
                    r[:chr] + f"[bold red]{text}[/bold red]" + r[chr + len(text) :]
                )
                found = True
            chr += 1

    return highlighted_results


query = "csv"
results = search_to_nearest_word(query, seq)

from rich import print

highlighted = highlight_search_terms(query, results)
for h in highlighted:
    print(h)
