# search_domain

A simple application for finding free .de domains. It generates a list of
candidates out of a simple pattern or tests a provided wordlist.

It first checks DNS to determine if a domain is occupied. If there is no
DNS entry, it asks the DENIC whois database that is rate-limited (~60 req/s).

It appends free and occupied domains to the specified files (from time to
time and not only at the end). In addition, you can specify multiple files
with domains that should be skipped which can be the same like the output
files. In this way, you can easily stop and resume your search.

There is also a chunk feature to run this script on multiple machines to
speedup the process. Notice that the chunking is done on the actual domains
that should be tested (without the ones from the skip files). So you might
miss some domains if you run the script on some machines and have to restart
one of them because then it takes the already found domains into account
for chunking.

## Requirements

Just Python 3.X installed (tested with Python 3.7).

## Usage

### Sample call

`./search_domain.py -v -p "A.de" --skip data/occu.txt data/free.txt`

Tests `a.de`, `b.de`, ..., `0.de`, ..., `9.de` and stores the results in
`data/occu.txt` and `data/free.txt`. In addition, it skips already checked
domains from these files.

### Help

```
usage: search_domain.py [-h] (--wordlist WORDLIST | --pattern PATTERN)
                         [--free FREE] [--occu OCCU] [--skip [SKIP [SKIP ...]]]
                         [--chunk CHUNK] [--chunks CHUNKS] [--verbose]
                         [--version]
 
 Find free .de domains. Requires either a wordlist or a pattern.
 
 optional arguments:
   -h, --help            show this help message and exit
   --wordlist WORDLIST, -w WORDLIST
                         a file with a list of .de domains to test
   --pattern PATTERN, -p PATTERN
                         a pattern for the domain generation. Allowed elements:
                         lowercase letters, numbers, dash, L for an arbitrary
                         letter, D for an arbitrary digit, and A for an
                         arbitrary allowed char.
   --free FREE           a file for storing free domains (default:
                         data/free.txt)
   --occu OCCU           a file for storing occupied domains (default:
                         data/occu.txt)
   --skip [SKIP [SKIP ...]]
                         one or multiple files containing domains that should
                         be skipped
   --chunk CHUNK         if you want to chunk the list of test domains, this
                         specifies which chunk should be processed
   --chunks CHUNKS       the number of chunks
   --verbose, -v         enable logging
   --version             show program's version number and exit
```

### Patterns

For the `--pattern` option, you can use a simple pattern language consisting of:
- lowercase letters (a-z),
- digits (0-9),
- dash (-), not as the first or last char,
- `L` for an arbitrary letter of a-z,
- `D` for an arbitrary digit 0-9, and
- `A` for an arbitary char out of a-z, 0-9 and dash.

The pattern is validated. You might provide the domain TLD `.de` but it is
also appended if it is not present.
