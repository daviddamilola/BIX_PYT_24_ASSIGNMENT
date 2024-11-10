"""Models to manage the per sequence quality section of the fastqc file"""
# David Oluwasusi 6th November 2024

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class PerSeqQualSection(Section):
    """
    Represents the per sequence quality scores section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create a heatmap of quality
    scores by tile and base position.

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a bar plot representing the quality score and the read count
    """
    def plot_section(self):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        try:
            data = pd.read_csv(file_path, sep='\t')
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            sys.exit(1)
        except pd.errors.EmptyDataError:
            print(f"Error: The file '{file_path}' is empty.")
            sys.exit(1)
        except pd.errors.ParserError:
            print(f"Error: The file '{file_path}' could not be parsed. Please check the file format.")
            sys.exit(1)

        # Create the plot
        plt.figure(figsize=(10, 6))

        try:
            sns.barplot(data=data, x='#Quality', y='Count', color='blue')
        except ValueError as ve:
            print(f"ValueError while creating plot: {ve}. Please check the data values.")
            sys.exit(1)
        except TypeError as te:
            print(f"TypeError while creating plot: {te}. Verify data types in the 'report.txt' file.")
            sys.exit(1)
        # Add titles and labels
        plt.title('Per Sequence Quality Distribution')
        plt.xlabel('Quality Score')
        plt.ylabel('Read Count')
        plt.grid(True, linestyle='--', linewidth=0.5)
        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        # Define the path to save the plot
        
        try:
            output_path = os.path.join(self.output_folder + '/'  + self.title, 'per_sequence_quality_plot.png')
            plt.savefig(output_path)
        except PermissionError:
            print(f"PermissionError: Insufficient permissions to save the plot to '{output_path}'.")
            sys.exit(1)
        except FileNotFoundError:
            print(f"FileNotFoundError: The path '{output_path}' is invalid. Please verify the output folder structure.")
            sys.exit(1)
        except IOError as ioe:
            print(f"IOError: Could not save the plot to '{output_path}': {ioe}")
            sys.exit(1)
        finally:
            # Save the plot
            plt.close()  # Close the plot to free memory
            print(f"Plot saved to {output_path}")
