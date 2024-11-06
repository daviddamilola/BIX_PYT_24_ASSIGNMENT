"""Model to manage per tile sequence section of the fastqc file, inherits from Section model"""
# David Oluwasusi 6th November 2024


import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from  models.base_section import Section


class PerTileSeqSection(Section):
    """
    Represents the per-tile sequence quality section in the fastqc file.
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
        plot_section(): Generates a heatmap representing the quality score across base
                        positions for each tile, then saves it as a PNG file.
    """
    def plot_section(self):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        data = pd.read_csv(file_path, sep='\t')
        # Pivot the data to format it for the heatmap
        heatmap_data = data.pivot(index='#Tile', columns='Base', values='Mean')
        # Create the heatmap
        plt.figure(figsize=(14, 10))
        sns.heatmap(
            heatmap_data,
            cmap='coolwarm',
            annot=False,
            cbar_kws={'label': 'Mean Quality Score'},
            xticklabels=5,  # Show every 5th base on x-axis for readability
            yticklabels=5   # Show every 5th tile on y-axis for readability
        )
        # Add titles and labels
        plt.title('Per Tile Sequence Quality Across Base Positions', fontsize=16, pad=20)
        plt.xlabel('Base Position', fontsize=14)
        plt.ylabel('Tile ID', fontsize=14)
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'per_tile_sequence_quality_heatmap.png')
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        print(f"Plot saved to {output_path}")
