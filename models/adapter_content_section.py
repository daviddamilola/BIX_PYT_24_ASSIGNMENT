"""model to manage the adapter content section of the fastqc files"""
# David Oluwasusi 6th November 2024

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class AdapterContentSection(Section):
    """
    Represents the adapter content section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method 
    to create a line plot to show the adapter content across positions

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a line plot to show the adapter content across positions
    """
    def plot_section(self):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        data = pd.read_csv(file_path, sep='\t')
        # Melt the data for easier plotting with seaborn
        data_melted = data.melt(id_vars=['#Position'], var_name='Adapter Type', value_name='Content')
        # Create the plot
        plt.figure(figsize=(14, 8))
        # Plot each adapter type's content across positions
        sns.lineplot(data=data_melted, x='#Position', y='Content', hue='Adapter Type', marker='o')
        # Add titles and labels
        plt.title('Adapter Content Across Positions')
        plt.xlabel('Position')
        plt.ylabel('Adapter Content')
        # Enable grid lines for better readability
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'adapter_content_plot.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")
