"""Models to manage the per base n section of the fastqc files"""
# David Oluwasusi 6th November 2024

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class PerBaseNContentSection(Section):
    """
    Represents the per base N content  section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create
    a line plot representing the base N content

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a line plot representing the base N content
    """
    def plot_section(self):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        data = pd.read_csv(file_path, sep='\t')
        # Create the plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data, x='#Base', y='N-Count', marker='o')
        # Add titles and labels
        plt.title('Per Base N Content')
        plt.xlabel('Base Position')
        plt.ylabel('N-Content')
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'per_base_n_content_plot.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")
