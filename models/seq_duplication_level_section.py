"""
Model to process the sequence duplication level section of the fastqc file.
It inherits from Section model
"""
# David Oluwasusi 6th November 2024


import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section

class SeqDuplicationLevelSection(Section):
    """
    Represents the sequence duplication level section in the fastqc file.
    It inherits from the `Section` class and provides
    a specific implementation of the `plot_section` method to create a barplot showing
    the relationship between the percentage of duplicated sequences and the total sequence

    Attributes:
        title (str): The title of the section.
        data (List): The primary data content for the section, to be saved in a report file.
        flag (str): A status or quality flag associated with this section.
        output_folder (str): The path to the root folder for 
            storing report file, flag file and generated plots.

    Methods:
        plot_section(): Generates a barplot showing
    the relationship between the percentage of deduplicated sequences and the total sequence
    """
    def plot_section(self):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        data = pd.read_csv(file_path, sep='\t', skiprows=1)
        # Convert the 'Duplication Level' column to a categorical type to preserve order
        data['#Duplication Level'] = pd.Categorical(
            data['#Duplication Level'],
            categories=data['#Duplication Level'].unique(),
            ordered=True
        )
        # Create the plot
        plt.figure(figsize=(14, 8))
        # Plot both "Percentage of deduplicated" and "Percentage of total" as bars
        sns.barplot(data=data, x='#Duplication Level', y='Percentage of deduplicated', color='skyblue', label='Percentage of Deduplicated')
        sns.barplot(data=data, x='#Duplication Level', y='Percentage of total', color='salmon', label='Percentage of Total', alpha=0.7)
        # Add titles and labels
        plt.title('Sequence Duplication Level Distribution')
        plt.xlabel('Duplication Level')
        plt.ylabel('Percentage')
        # Add a legend
        plt.legend(title="Legend")
        # Enable grid lines for better readability
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'sequence_duplication_level_plot.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")