"""Module providing a class for processing fastqc files."""

import re
import sys
import constants as sections
import section_model as se

class FastQCParser:
    """
    Reads fastqc files and provides functions to get individual sections in the file.

    ...

    Attributes
    ----------
    fastqc_dict : dict
        first name of the person
    output_folder : str
        family name of the person
    file_path : int
        age of the person

    """

    def __init__(self, file_path, output_folder):
        """
        Constructs all the necessary attributes for the parser object.

        Parameters
        ----------
            file_path : str
                the file path to read the fastqc file
            output_folder : str
                the folder to write the results to
        """
        self.fastqc_dict = {}
        self.output_folder = output_folder
        self.file_path = file_path

    @staticmethod
    def print_summary(summary):
        """
        Prints a provided summary.

        Args:
            summary (str): A summary string to print.
        """
        print("".join(summary))

    def parse_fastqc_to_dictionary(self):
        """converts fastqc file to a dictionary where the key is the title of the section.
        The value is a dictionary containing section_content, status

        Returns:
            Dictionary: {
                "section_content": list of each line in the section
                "status": string(pass | fail | warn) which represents the result of the section
            }
        """
        try:
            # comment:
            with open(self.file_path, 'r',  encoding="utf-8") as f:
                parsed_dict = {}
                end_pattern = r'.*>>END_MODULE$'
                section_title = r'>>\s*(.*?)\s+(pass|fail|warn)$'
                current_section = None
                current_status = None
                section_content = []
                for line in f:
                    if line.startswith(">>") and not re.match(end_pattern, line) :
                        # Save the previous section if any
                        if current_section:
                            parsed_dict[current_section] = {
                                "section_content": section_content, 
                                "status": current_status
                                }
                            section_content = []

                        #extract section title
                        match = re.search(section_title, line)
                        if match:
                            current_section = match.group(1).strip()
                            current_status = match.group(2).strip()
                    elif re.match(end_pattern, line) and current_section:
                        # Reached end of a section, save it and reset the pointers to None
                        parsed_dict[current_section] = {
                            "section_content": section_content, 
                            "status": current_status
                            }
                        current_section = None
                        current_status = None
                        section_content = []

                    elif current_section:
                        section_content.append(line)

                if current_section:
                    parsed_dict[current_section] = {
                        "section_content": section_content, 
                        "status": current_status
                        }

            self.fastqc_dict = parsed_dict
            return self.fastqc_dict

        except FileNotFoundError:
            print("passed path", self.file_path, "does not exist")
            sys.exit(1)

    def get_base(self):
        """parses the base section
        """
        title = sections.BASIC_STATS
        data = self.fastqc_dict[sections.BASIC_STATS]["section_content"]
        flag = self.fastqc_dict[sections.BASIC_STATS]["status"]
        output = self.output_folder
        section = se.BaseSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_report()
        section.write_flag()

    def get_tile_seq(self):
        """parses the per tile sequence section
        """
        title = sections.PER_TILE_SEQ
        data = self.fastqc_dict[sections.PER_TILE_SEQ]["section_content"]
        flag = self.fastqc_dict[sections.PER_TILE_SEQ]["status"]
        output = self.output_folder
        section = se.PerTileSeqSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_qual_scores(self):
        """parses the per quality scores section
        """
        title = sections.PER_SEQ_QUALITY_SCORES
        data = self.fastqc_dict[sections.PER_SEQ_QUALITY_SCORES]["section_content"]
        flag = self.fastqc_dict[sections.PER_SEQ_QUALITY_SCORES]["status"]
        output = self.output_folder
        section = se.PerSeqQualSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_base_seq_content(self):
        """ parses the per base sequence content section
        """
        title = sections.PER_BASE_SEQ_CONTENT
        data = self.fastqc_dict[sections.PER_BASE_SEQ_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_BASE_SEQ_CONTENT]["status"]
        output = self.output_folder
        section = se.PerBaseSeqContentSection(
            title=title,
            data=data,
            flag=flag,
            output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_gc_content(self):
        """parses the per sequence gc content section
        """
        title = sections.PER_SEQ_GC_CONTENT
        data = self.fastqc_dict[sections.PER_SEQ_GC_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_SEQ_GC_CONTENT]["status"]
        output = self.output_folder
        section = se.PerSeqGCContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_base_n_content(self):
        """parses the per base N content sections
        """
        title = sections.PER_BASE_N_CONTENT
        data = self.fastqc_dict[sections.PER_BASE_N_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_BASE_N_CONTENT]["status"]
        output = self.output_folder
        section = se.PerBaseNContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_len_dist(self):
        """parses the sequence length list section"""
        title = sections.SEQ_LEN_DIST
        data = self.fastqc_dict[sections.SEQ_LEN_DIST]["section_content"]
        flag = self.fastqc_dict[sections.SEQ_LEN_DIST]["status"]
        output = self.output_folder
        section = se.SeqLenDistSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_dup(self):
        """parses the sequence duplication level section
        """
        title = sections.SEQ_DUPLICATION_LEVEL
        data = self.fastqc_dict[sections.SEQ_DUPLICATION_LEVEL]["section_content"]
        flag = self.fastqc_dict[sections.SEQ_DUPLICATION_LEVEL]["status"]
        output = self.output_folder
        section = se.SeqDuplicationLevelSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_overep_seq(self):
        """parses the overrepresented sequence section
        """
        title = sections.OVERREPRESENTED_SEQ
        data = self.fastqc_dict[sections.OVERREPRESENTED_SEQ]["section_content"]
        flag = self.fastqc_dict[sections.OVERREPRESENTED_SEQ]["status"]
        output = self.output_folder
        section = se.OverRepresentedSeqSection(title, data, flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_adap_cont(self):
        """parses the adapter content section
        """
        title = sections.ADAPTER_CONTENT
        data = self.fastqc_dict[sections.ADAPTER_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.ADAPTER_CONTENT]["status"]
        output = self.output_folder
        section = se.AdapterContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_kmer_cont(self):
        """parses the kmer content section
        """
        title = sections.KMER_CONTENT
        data = self.fastqc_dict[sections.KMER_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.KMER_CONTENT]["status"]
        output = self.output_folder
        section = se.KmerContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_all(self):
        """parses all sections
        """
        self.get_base()
        self.get_tile_seq()
        self.get_seq_qual_scores()
        self.get_base_seq_content()
        self.get_seq_gc_content()
        self.get_base_n_content()
        self.get_seq_len_dist()
        self.get_seq_dup()
        self.get_overep_seq()
        self.get_adap_cont()
        self.get_kmer_cont()
