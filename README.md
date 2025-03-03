# Fastqc Reporter Technical Documentation

## By Oluwasusi David  

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Program Design](#program-design)
   - [Overview of Functionality](#overview-of-functionality)
   - [Folder Structure](#folder-structure)
   - [Dependencies Used](#dependencies-used)
4. [Example Usage](#example-usage)
   - [Options and Results](#options-and-results)
5. [Error Handling](#error-handling)
6. [References](#references)

---

## Introduction
Fastqc reporter is a **Command Line Interface (CLI) tool** built to parse fastqc files into sections and generate reports. It also generates graphical representations and a flag file indicating the QC test result (`pass`, `fail`, or `warn`).

---

## Installation
To run this program, the following are required:

- Python 3.9 or higher
- Conda or venv (Conda is used in this documentation)

To create a new virtual environment and install dependencies:

```sh
conda create -c conda-forge -n name_of_my_env seaborn pandas matplotlib
```

Activate the virtual environment:

```sh
source activate name_of_my_env
```

Run the program with its parameters (refer to the [Example Usage](#example-usage) section).

---

## Program Design
Fastqc reporter follows an **object-oriented approach** with two main classes:

- **FastQCParser**
- **Section**

The `FastQCParser` class parses fastqc files into sections and manages optional parameters. The `Section` class writes reports and flag files for each section.

Each section inherits from the base `Section` class and defines its own implementation of the `plot_section()` method to generate the necessary plots.

### Overview of Functionality
Fastqc reporter uses Python's `argparse` module to handle command-line arguments. Required parameters:

- Path to the fastqc file
- Output folder for plots, reports, and flag files

Optional parameters are handled via `add_argument` with `store_true`, making them optional.

#### Workflow:
1. Instantiate `FastQCParser` with required parameters.
2. Parse the fastqc file into a dictionary.
3. Handle optional parameters and call appropriate methods.
4. Generate reports, plots, and flag files.

---

### Folder Structure
The script is structured as follows:

```
fastqc_reporter/
│── fastqc_reporter.py  # Entry point, defines parser options
│── constants.py  # Defines section titles
│── model/  # Contains all classes used in the script
│   ├── __init__.py
│   ├── section.py
│   ├── fastqc_parser.py
│── data/  # Contains test fastqc files
```

---

### Dependencies Used

- **Matplotlib** & **Seaborn** - For plotting graphs
- **Pandas** - To extract and manage section data using `pandas.read_csv()`

---

## Example Usage

To run the program in its default form:

```sh
python3 fastqc_reporter.py ./data/fastqc_data1.txt ./solution1/
```

### Output Example:
```
Basic Statistics pass
#Measure Value
Filename 4_age21_S12_L001_R2_001_concat.fastq.gz
File type Conventional base calls
Encoding Sanger / Illumina 1.9
Total Sequences 37287903
Sequences flagged as poor quality 0
Sequence length 75
%GC 55
```

---

## Options and Results
Users can specify sections to run using options:

| Option | Description |
|--------|-------------|
| `-t` / `--per_tile_seq_qual` | Per Tile Sequence Quality |
| `-s` / `--per_seq_qual_scores` | Per Sequence Quality Scores |
| `-c` / `--per_base_seq_content` | Per Base Sequence Content |
| `-g` / `--per_seq_GC_cont` | Per Sequence GC Content |
| `-n` / `--per_base_N_cont` | Per Base N Content |
| `-l` / `--seq_len_dist` | Sequence Length Distribution |
| `-d` / `--seq_dup` | Sequence Duplication Levels |
| `-o` / `--over_seq` | Overrepresented Sequences |
| `-p` / `--adap_cont` | Adapter Content |
| `-k` / `--kmer_count` | K-mer Content |
| `-a` / `--all` | Run all sections |

---

## Error Handling
The script implements error handling using Python's `try-except` block to manage:

- Invalid user input
- Malformed fastqc files
- File permission errors
- Parsing errors

If an error occurs, the program exits with a **non-zero exit code** and prints an error message.

---

## References

- Akalin, A. (2020). *Computational genomics with R* (Chapter 7: Quality check on sequencing reads). [Bookdown](https://compgenomr.github.io/book/quality-check-on-sequencing-reads.html)
- Babraham Institute. (n.d.). *FastQC per tile sequence quality analysis.* [FastQC Help](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modules/12%20Per%20Tile%20Sequence%20Quality.html)
- Kong, Y. (2011). *Btrim: A fast, lightweight adapter and quality trimming program for next-generation sequencing technologies.* [Genomics](https://doi.org/10.1016/j.ygeno.2011.05.009)
- Illumina. (2018). *Ask a scientist - What is GC-Bias?* [YouTube](https://www.youtube.com/watch?v=wdEb3chYFOw)
- O'Rawe, J. F., Ferson, S., & Lyon, G. (2015). *Accounting for uncertainty in DNA sequencing data.* [Trends in Genetics](https://doi.org/10.1016/j.tig.2014.12.002)
- Pandas Documentation. [pandas.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- Seaborn Documentation. [Seaborn functions](https://seaborn.pydata.org/tutorial/function_overview.html)

---


