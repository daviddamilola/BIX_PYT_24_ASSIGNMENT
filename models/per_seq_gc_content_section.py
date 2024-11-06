"""Models to manage each section of the fastqc files"""
# David Oluwasusi 6th November 2024

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class PerSeqGCContentSection(Section):
    """
    Represents the per GC content  section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create a lineplot of gc content
    and read counts

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a bar plot representing the gc content and the read count
    """
    def plot_section(self):
        # Construct the path to the data file
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        # Load the data from the text file, assuming it's tab-separated
        data = pd.read_csv(file_path, sep='\t')
        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=data, x='#GC Content', y='Count', marker='o')
        # Add titles and labels
        plt.title('Per Sequence GC Content Distribution')
        plt.xlabel('GC Content (%)')
        plt.ylabel('Read Count')
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'per_sequence_gc_content_plot.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")
