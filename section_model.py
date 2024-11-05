import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Section:
    """
    Represents a section with associated data, flag, and output folder for report generation and plotting.

    Attributes:
        title (str): The title of the section, used for naming folders and files.
        data (str): The main data content of the section, which will be saved in a report.
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
            with open(report_path, 'w') as f:
                f.write(data_content)
            print("Report successfully written to", report_path)

        except OSError as e:
            print(f"Error creating directory or writing file: {e}")
        except IOError as e:
            print(f"Error with file I/O: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def write_flag(self):
        """_summary_
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
        pass

class BaseSection(Section):
    """_summary_

    Args:
        Section (_type_): _description_
    """
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)

class PerTileSeqSection(Section):
    """_summary_

    Args:
        Section (_type_): _description_
    """
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)

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

class PerSeqQualSection(Section):
    """_summary_

    Args:
        Section (_type_): _description_
    """
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)

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
    
class PerBaseSeqContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self):
        # Construct the path to the data file
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        
        # Load the data from the text file, assuming it's tab-separated
        data = pd.read_csv(file_path, sep='\t')
        
        # Melt the DataFrame to make it easier to plot with seaborn
        data_melted = data.melt(id_vars='#Base', var_name='Nucleotide', value_name='Percentage')
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=data_melted, x='#Base', y='Percentage', hue='Nucleotide', marker='o')
        
        # Add titles and labels
        plt.title('Per Base Sequence Composition')
        plt.xlabel('Base Position')
        plt.ylabel('Percentage of Each Nucleotide')
        
        # Ensure the output folder exists
        plot_folder = os.path.join(self.output_folder, self.title)
        os.makedirs(plot_folder, exist_ok=True)
        
        # Define the path to save the plot
        output_path = os.path.join(plot_folder, 'per_base_sequence_plot.png')
        
        # Save the plot
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory
        
        print(f"Plot saved to {output_path}")
    
class PerSeqGCContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
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
    
class PerBaseNContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
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
    
class SeqLenDistSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
class SeqDuplicationLevelSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
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
    
class OverRepresentedSeqSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
class AdapterContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
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

class KmerContentSection(Section):
    def __init__(self, title, data, flag, output_folder):
        super().__init__(title, data, flag, output_folder)
    
    def plot_section(self, metric='Count', top_n=20):
        # Load the data from a text file, assuming it's tab-separated
        file_path = os.path.join(self.output_folder, self.title, 'report.txt')
        data = pd.read_csv(file_path, sep='\t')
        
        # Remove any leading '#' from column names
        data.columns = data.columns.str.replace('#', '')
        
        # Sort by the specified metric and select the top N K-mers
        data_top = data.nlargest(top_n, metric)
        
        # Create the plot
        plt.figure(figsize=(14, 8))
        sns.barplot(data=data_top, x=metric, y='Sequence', color='skyblue')
        
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
        plt.savefig(output_path, bbox_inches="tight")
        plt.close()  # Close the plot to free memory
        
        print(f"Plot saved to {output_path}")


