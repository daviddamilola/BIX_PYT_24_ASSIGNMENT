"""Base model to manage each section of the fastqc files"""
# David Oluwasusi 6th November 2024

import os

class Section:
    """
    Represents a section in the fastqc file.
    it has associated data, flag, and output folder for report generation and plotting.

    Attributes:
        title (str): The title of the section, used for naming folders and files.
        data (List): The main data content of the section, which will be saved in a report.
        flag (str): A flag associated with the section, saved separately.
        output_folder (str): The root folder where reports and plots are saved.
    """
    def __init__(self, title, data, flag, output_folder):
        self.title = title
        self.data = data
        self.flag = flag
        self.output_folder = output_folder

    def write_report(self):
        """
            Writes the section data to a text file in the specified output folder.
        """

        # Define the report directory and file path
        report_dir = os.path.join(self.output_folder, self.title)
        report_path = os.path.join(report_dir, 'report.txt')

        try:
            # Check if the directory exists; if not, create it
            os.makedirs(report_dir, exist_ok=True)
            # Write data content to the report file
            data_content = "".join(self.data)
            with open(report_path, 'w', encoding="utf-8") as f:
                f.write(data_content)
            print("Report successfully written to", report_path)

        except IOError as e:
            print(f"Error with file I/O: {e}")

        except OSError as e:
            print(f"Error creating directory or writing file: {e}")
       
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def write_flag(self):
        """Write the flag of the test on the section to a flag.txt file
        """
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
        """To be implemented by each section on its own
        """
        pass
