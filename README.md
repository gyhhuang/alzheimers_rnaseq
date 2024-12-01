### Table of Contents

# run_metadata.csv
    Description: the metadata for each run (sample) that was taken. 
    Important Columns: 
            Run: The ID for the run. This is the identifier for the expression folders
            isolate: The corresponding subject (person) of the run. For an isolate, one run per tissue (region).  Corresponds to the isolate column in the subject_metadata table.
            tissue: The tissue being analyzed (Either EC or V2)


# subject_metadata.csv
    Description: the metadata for each subject
    Important Columns:
            Isolate: The ID of the subject. Corresponds to the isolate column in run_metadata.csv
            Pathology Stage: This is the Alzheimer's partitioning we want to use. It is the most comprehensive. There are four stages, 1-4, with 4 being the most extreme. I got 2 samples of each.
            Sex: Sex of the subject
            Age: Age of the subject


# expression/
    Description: the directory containing the expression levels for all runs

    /SRR22924XXX: the directory containing the expression levels for that particular run (Run column in metadata)

        /run_info.json: metadata for the run
            Important Columns:
                n_pseudoaligned: The number of reads that were matched to the reference genome
        /abundance.tsv: expression levels
            Important Columns:
                target_id: gene name (it's an id, you're going to have to map it back to the original gene)
                est_counts: raw number of genes found
                tpm: the transcripts per million, to account for different lengths
