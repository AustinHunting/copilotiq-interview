# CopilotIQ-Interview

Repository containing interview problems and solutions for CopilotIQ.
We are solving [Links-Exercise-1.rtf](./Links-Exercise-1.rtf). It is a python script for building a linked graph of URLs from a single URL.

### Prerequisites

To build and use this project you will need Docker installed and either a local copy of this repository or git.

```
git clone git@github.com:AustinHunting/copilotiq-interview.git
cd copilotiq-interview
docker build -t hyperlinks .
```

What the docker build command is doing:
1. Creates a local alpine docker container
1. Installs python3 and pip3
1. Uses pip to install required python libraries
1. Copies the python executable into the docker container

## Usage

```
usage: hyperlinks.py [-h] --url URL --limit LIMIT [--out OUT]

traverse the Web as a linked graph from the starting --url finding all outgoing links (<a> tag): it
will store each outgoing link for the URL, and then repeat the process for each of them, until
--limit URLs will have been traversed.

optional arguments:
  -h, --help     show this help message and exit
  --url URL      Starting URL
  --limit LIMIT  Number of URLs to traverse
  --out OUT      File to store computed json data in, defaults to stdout

Example: hyperlinks.py --url https://docs.python.org/ --limit 10 --out links.json
```

The script can be called by running the docker image `hyperlink`

Example:

```
docker run --rm -it -v /tmp/:/home/ hyperlinks --url=https://example.com --limit=4 --out=out.json
```

`hyperlinks.py` is defined as the entrypoint to the docker container, this means any variables passed into the container will be consumed by `hyperlinks.py`

Example:

```
# will print json to stdout
docker run --rm -it -v /tmp/:/home/ hyperlinks --url=https://example.com --limit=4

# will print help text from the hyperlinks script
docker run --rm -it -v /tmp/hmmmm:/home/ hyperlinks -h
```

Please note the `-v` flag on on the `run` command. This mirrors the current host directory into the docker container so output can be saved to disk.

This has been tested on Linux and MacOS, when running on Windows you will have to replace `/` with `\` (**untested**)

## Running the tests

Testing `hyperlinks.py` is done by running `hyperlinks_test.py` from the main git directory. All imports are included in the standard libraries.

It is recommended that CI runs `hyperlinks_test.py` on commits to branches and merges to main.

## License

This project is licensed under the GNU General Public License v3.0, more information can be found [here](https://www.gnu.org/licenses/gpl-3.0.en.html)
