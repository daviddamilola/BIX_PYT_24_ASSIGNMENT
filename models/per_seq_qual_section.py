"""Models to manage the per sequence quality section of the fastqc file"""
# David Oluwasusi 6th November 2024

import os
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
        data = pd.read_csv(self.output_folder + self.title + '/report.txt', sep='\t')
        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.barplot(data=data, x='#Quality', y='Count', color='blue')
        # Add titles and labels
        plt.title('Per Sequence Quality Distribution')
        plt.xlabel('Quality Score')
        plt.ylabel('Read Count')
        # Ensure the output folder exists
        os.makedirs(self.output_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(self.output_folder + self.title, 'per_sequence_quality_plot.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")
