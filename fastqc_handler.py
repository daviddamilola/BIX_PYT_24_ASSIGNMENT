import constants as sections
import re
import sys
import os

class FastQCParser:

    def __init__(self, file_path, output_folder):
        self.fastqc_dict = {}
        self.output_folder = output_folder
        self.file_path = file_path

    def parse_fastqc_to_dictionary(self):
        try:
            # comment:
            with open(self.file_path, 'r') as f:
                parsed_dict = {}
                end_pattern = r'.*>>END_MODULE$'
                section_title = r'>>\s*(.*?)\s+(pass|fail|warn)$'
                current_section = None
                current_status = None
                section_content = []
                for line in f:
                    if line.startswith(">>") and not(re.match(end_pattern, line)):
                        # Save the previous section if any
                        if current_section:
                            parsed_dict[current_section] = {"section_content": section_content, "status": current_status}
                            section_content = []

                        #extract section title
                        match = re.search(section_title, line)
                        if match:
                            current_section = match.group(1).strip()
                            current_status = match.group(2).strip()
                    
                    elif re.match(end_pattern, line) and current_section:
                        # Reached end of a section, save it and reset the pointers to None
                        parsed_dict[current_section] = {"section_content": section_content, "status": current_status}
                        current_section = None
                        current_status = None
                        section_content = []

                    elif current_section:
                        section_content.append(line)

                if current_section:
                    parsed_dict[current_section] = {"section_content": section_content, "status": current_status}

            self.fastqc_dict = parsed_dict
            return self.fastqc_dict

        except FileNotFoundError:
            print("passed path", self.file_path, "does not exist")
            sys.exit(1)
 
    def get_base(self):
        title = sections.BASIC_STATS
        data = self.fastqc_dict[sections.BASIC_STATS]["section_content"]
        flag = self.fastqc_dict[sections.BASIC_STATS]["status"]
        output = self.output_folder
        section = BaseSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_tile_seq(self):
        title = sections.PER_TILE_SEQ
        data = self.fastqc_dict[sections.PER_TILE_SEQ]["section_content"]
        flag = self.fastqc_dict[sections.PER_TILE_SEQ]["status"]
        output = self.output_folder
        section = PerTileSeqSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_qual_scores(self):
        title = sections.PER_SEQ_QUALITY_SCORES
        data = self.fastqc_dict[sections.PER_SEQ_QUALITY_SCORES]["section_content"]
        flag = self.fastqc_dict[sections.PER_SEQ_QUALITY_SCORES]["status"]
        output = self.output_folder
        section = PerSeqQualSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_base_seq_content(self):
        title = sections.PER_BASE_SEQ_CONTENT
        data = self.fastqc_dict[sections.PER_BASE_SEQ_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_BASE_SEQ_CONTENT]["status"]
        output = self.output_folder
        section = PerBaseSeqContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_gc_content(self):
        title = sections.PER_SEQ_GC_CONTENT
        data = self.fastqc_dict[sections.PER_SEQ_GC_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_SEQ_GC_CONTENT]["status"]
        output = self.output_folder
        section = PerSeqGCContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_base_n_content(self):
        title = sections.PER_BASE_N_CONTENT
        data = self.fastqc_dict[sections.PER_BASE_N_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.PER_BASE_N_CONTENT]["status"]
        output = self.output_folder
        section = PerBaseNContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_len_dist(self):
        title = sections.SEQ_LEN_DIST
        data = self.fastqc_dict[sections.SEQ_LEN_DIST]["section_content"]
        flag = self.fastqc_dict[sections.SEQ_LEN_DIST]["status"]
        output = self.output_folder
        section = SeqLenDistSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_seq_dup(self):
        title = sections.SEQ_LEN_DIST
        data = self.fastqc_dict[sections.SEQ_LEN_DIST]["section_content"]
        flag = self.fastqc_dict[sections.SEQ_LEN_DIST]["status"]
        output = self.output_folder
        section = SeqLenDistSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_overep_seq(self):
        title = sections.OVERREPRESENTED_SEQ
        data = self.fastqc_dict[sections.OVERREPRESENTED_SEQ]["section_content"]
        flag = self.fastqc_dict[sections.OVERREPRESENTED_SEQ]["status"]
        output = self.output_folder
        section = OverRepresentedSeqSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_adap_cont(self):
        title = sections.ADAPTER_CONTENT
        data = self.fastqc_dict[sections.ADAPTER_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.ADAPTER_CONTENT]["status"]
        output = self.output_folder
        section = AdapterContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_kmer_cont(self):
        title = sections.KMER_CONTENT
        data = self.fastqc_dict[sections.KMER_CONTENT]["section_content"]
        flag = self.fastqc_dict[sections.KMER_CONTENT]["status"]
        output = self.output_folder
        section = KmerContentSection(title=title, data=data, flag=flag, output_folder=output)
        section.print_summary(self.fastqc_dict[sections.BASIC_STATS]["section_content"])
        section.write_flag()
        section.write_report()
        section.plot_section()

    def get_all(self):
        for key, val in self.fastqc_dict.items():
            print(key)
            print("".join(val["section_content"]))

class Section:
    def __init__(self, title, data, flag, output_folder):
        self.title = title
        self.data = data
        self.flag = flag
        self.output_folder = output_folder

    def print_summary(self, summary):
        print("".join(summary))

    def write_report(self):
        # Define the report directory and file path
        report_dir = os.path.join(self.output_folder, self.title)
        report_path = os.path.join(report_dir, 'report.txt')

        try:
            # Check if the directory exists; if not, create it
            os.makedirs(report_dir, exist_ok=True)
            
            # Write data content to the report file
            data_content = "".join(self.data)
            with open(report_path, 'w') as f:
                f.write(data_content)
            
            print("Report successfully written to", report_path)

        except OSError as e:
            print(f"Error creating directory or writing file: {e}")
        except IOError as e:
            print(f"Error with file I/O: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def write_flag(self):
        # Define the flag directory and file path
        flag_dir = os.path.join(self.output_folder, self.title)
        flag_path = os.path.join(flag_dir, 'flag.txt')

        try:
            # Check if the directory exists; if not, create it
            os.makedirs(flag_dir, exist_ok=True)
            
            # Write flag content to the flag file
            flag_content = self.flag
            with open(flag_path, 'w') as f:
                f.write(flag_content)
            
            print("Flag successfully written to", flag_path)

        except OSError as e:
            print(f"Error creating directory or writing file: {e}")
        except IOError as e:
            print(f"Error with file I/O: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def plot_section(self):
        pass

class BaseSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)

class PerTileSeqSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class PerSeqQualSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class PerBaseSeqContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class PerSeqGCContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class PerBaseNContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class SeqLenDistSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class SeqDuplicationLevelSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class OverRepresentedSeqSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()
    
class AdapterContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()

class KmerContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        return super().plot_section()


