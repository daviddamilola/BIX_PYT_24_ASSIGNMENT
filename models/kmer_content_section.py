"""Model to manage the kmer content section of the fastqc file, inherits from Section model"""
# David Oluwasusi 6th November 2024

import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class KmerContentSection(Section):
    """
    Represents the kmer content  section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create a barplot of the top 20 kmer count
    and read counts

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a barplot of the top 20 kmer count
    """

    def plot_section(self, metric='Count', top_n=20):
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
        # Remove any leading '#' from column names
        data.columns = data.columns.str.replace('#', '')
        # Sort by the specified metric and select the top N K-mers
        data_top = data.nlargest(top_n, metric)
        # Create the plot
        plt.figure(figsize=(14, 8))
        try:
            sns.barplot(data=data_top, x=metric, y='Sequence', color='skyblue')
        except ValueError as ve:
            print(f"ValueError while creating plot: {ve}. Please check the data values.")
            sys.exit(1)
        except TypeError as te:
            print(f"TypeError while creating plot: {te}. Verify data types in the 'report.txt' file.")
            sys.exit(1)
        # Add titles and labels
        plt.title(f'Top {top_n} K-mer Sequences by {metric}')
        plt.xlabel(metric)
        plt.ylabel('K-mer Sequence')
        # Enable grid lines for better readability
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, f'kmer_content_by_{metric.lower()}.png')
        # Save the plot
        try:
            plt.savefig(output_path, bbox_inches="tight")
            plt.close()  # Close the plot to free memory
        except PermissionError:
            print(f"PermissionError: Insufficient permissions to save the plot to '{output_path}'.")
            sys.exit(1)
        except FileNotFoundError:
            print(f"FileNotFoundError: The path '{output_path}' is invalid. Please verify the output folder structure.")
            sys.exit(1)
        except IOError as ioe:
            print(f"IOError: Could not save the plot to '{output_path}': {ioe}")
            sys.exit(1)
        
        print(f"Plot saved to {output_path}")

