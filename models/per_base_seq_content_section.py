""" 
Model to process the per base  sequence content section of the fastqc file.
inherits from Section model
"""
# David Oluwasusi 6th November 2024

import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section


class PerBaseSeqContentSection(Section):
    """
    Represents the per base sequence content section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create a lineplot showing
    the relationship between the percentage of duplicated sequences and the total sequence

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a barplot showing
    the percentage base nucleotide 
    """
    def plot_section(self):
        # Construct the path to the data file
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        # Load the data from the text file, assuming it's tab-separated
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
        # Melt the DataFrame to make it easier to plot with seaborn
        data_melted = data.melt(id_vars='#Base', var_name='Nucleotide', value_name='Percentage')
        # Create the plot
        plt.figure(figsize=(10, 6))
        try:
            sns.lineplot(data=data_melted, x='#Base', y='Percentage', hue='Nucleotide', marker='o')
            plt.grid(True, linestyle='--', linewidth=0.5)
        except ValueError as ve:
            print(f"ValueError while creating plot: {ve}. Please check the data values.")
            sys.exit(1)
        except TypeError as te:
            print(f"TypeError while creating plot: {te}. Verify data types in the 'report.txt' file.")
            sys.exit(1)
        # Add titles and labels
        plt.title('Per Base Sequence Composition')
        plt.xlabel('Base Position')
        plt.ylabel('Percentage of Each Nucleotide')
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        try:
            output_path = os.path.join(plot_folder, 'per_base_sequence_plot.png')
            plt.savefig(output_path)
        except PermissionError:
            print(f"PermissionError: Insufficient permissions to save the plot to '{output_path}'.")
            sys.exit(1)
        except FileNotFoundError:
            print(f"FileNotFoundError: The path '{output_path}' is invalid. Please verify the output folder structure.")
            sys.exit(1)
        except IOError as ioe:
            print(f"IOError: Could not save the plot to '{output_path}': {ioe}")
        # Save the plot
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")