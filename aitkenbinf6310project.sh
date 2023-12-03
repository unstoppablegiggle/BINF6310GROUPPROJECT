#!/bin/bash

#SBATCH --job-name=binf6310_project	  # Name of the job
#SBATCH -p courses                # Who to bill for the job
#SBATCH -N 50                              # How many nodes do you need
#SBATCH -c 8                              # How many$
#SBATCH --mem 64G                         # How much memory
#SBATCH -t 24:00:00                        # How long
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=<aitken.n>@northeastern.edu
#SBATCH --out=/courses/BINF6310.202410/students/%u/logs/%x_%j.log
#SBATCH --error=/courses/BINF6310.202410/students/%u/logs/%x_%j.err


module load miniconda3/23.5.2
source activate binf6310
#conda activate


# Variables
PATH_TO_CLASS=/courses/BINF6310.202410                    # Base of all the other variables we make
PATH_TO_ME=${PATH_TO_CLASS}/students/${USER}                      # Where you will store the output
PATH_TO_ACTIVITY=${PATH_TO_CLASS}/data/alignment         # This is where the activity data is stored

# code
python3 esm-variants/esm_score_missense_mutations_mod.py --input-fasta-file esm-variants/uniprot-filtere$

