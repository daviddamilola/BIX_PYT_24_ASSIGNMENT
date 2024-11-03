import argparse
from fastqc_handler import FastQCParser


def main():
    #Description
    parser = argparse.ArgumentParser(description=""" This
    script parses FastQC text files and makes reports and plots based on the options passed to it.""")

    #Compulsory parameters
    parser.add_argument("input_path", metavar="FastQC input_path", type=str, help="FastQC input file path.")
    parser.add_argument("output_folder_path", metavar="FastQC output folder path", type=str, help="FastQC output folder path.")

    #Optional arguments
    parser.add_argument("-b", "--per_base_seq_qual", action="store_true", help="Per base sequence quality")

    parser.add_argument("-t", "--per_tile_seq_qual", action="store_true", help="Per tile sequence quality")

    parser.add_argument("-s", "--per_seq_qual_scores", action="store_true", help="Per sequence quality scores")

    parser.add_argument("-c", "--per_base_seq_content", action="store_true", help="Per base sequence content")

    parser.add_argument("-g", "--per_seq_GC_cont", action="store_true", help="Per sequence GC content")

    parser.add_argument("-n", "--per_base_N_cont", action="store_true", help="Per base N content")

    parser.add_argument("-l", "--seq_len_dist", action="store_true", help="Sequence Length Distribution")

    parser.add_argument("-d", "--seq_dup", action="store_true", help="Sequence Duplication Levels")

    parser.add_argument("-o", "--over_seq", action="store_true", help="Overrepresented sequences")

    parser.add_argument("-p", "--adap_cont", action="store_true", help="Adapter Content")

    parser.add_argument("-k", "--kmer_count", action="store_true", help="K-mer Content")

    parser.add_argument("-a", "--all", action="store_true", help="All the above")
    args = parser.parse_args()

    fastqc_file_input = args.input_path
    output_folder = args.output_folder_path
    parser = FastQCParser(fastqc_file_input, output_folder)

    parser.parse_fastqc_to_dictionary()
 
    if args.per_base_seq_qual:
        parser.get_base()

    if args.per_tile_seq_qual:
        parser.get_tile_seq()

    if args.all:
        parser.get_all()
    

if(__name__ == "__main__"):
    main()