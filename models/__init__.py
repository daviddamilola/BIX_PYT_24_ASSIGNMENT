"""models to manage each section of the fastqc files"""
# David Oluwasusi 6th November 2024

from .base_section import Section
from .base_stats_section import BaseStatsSection
from .per_tile_seq_section import PerTileSeqSection
from .per_seq_qual_section import PerSeqQualSection
from .per_base_seq_content_section import PerBaseSeqContentSection
from .per_seq_gc_content_section import PerSeqGCContentSection
from .per_base_n_content_section import PerBaseNContentSection
from .seq_duplication_level_section import SeqDuplicationLevelSection
from .adapter_content_section import AdapterContentSection
from .kmer_content_section import KmerContentSection
