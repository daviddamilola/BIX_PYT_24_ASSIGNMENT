import argparse
from fastqc_handler import FastQCParser
import constants as sections


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

    parser_instance = FastQCParser(fastqc_file_input, output_folder)

    parser_instance.parse_fastqc_to_dictionary()

    FastQCParser.print_summary(parser_instance.fastqc_dict[sections.BASIC_STATS]["section_content"])

    if args.per_base_seq_qual:
        parser_instance.get_base()

    if args.per_tile_seq_qual:
        parser_instance.get_tile_seq()

    if args.per_seq_qual_scores:
        parser_instance.get_seq_qual_scores()

    if args.per_base_seq_content:
        parser_instance.get_base_seq_content()

    if args.per_seq_GC_cont:
        parser_instance.get_seq_gc_content()

    if args.per_base_N_cont:
        parser_instance.get_base_n_content()

    if args.seq_len_dist:
        parser_instance.get_seq_len_dist()

    if args.seq_dup:
        parser_instance.get_seq_dup()

    if args.over_seq:
        parser_instance.get_overep_seq()

    if args.adap_cont:
        parser_instance.get_adap_cont()

    if args.kmer_count:
        parser_instance.get_kmer_cont()

    if args.all:
        parser_instance.get_all()

if __name__ == "__main__":
    main()
