#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=06:00:00
#SBATCH --job-name=gpu_run_emsb1
#SBATCH --mem=32GB
#SBATCH --ntasks=1
#SBATCH --output=myjob.%j.out
#SBATCH --error=myjob.%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=courtney.c@northeastern.edu

module load miniconda3/23.5.2
module load cuda/12.1
source activate
conda activate CUDA_baby


# Variables
PATH_TO_CLASS=/courses/BINF6310.202410                    # Base of all the other variables we make
PATH_TO_ME=${PATH_TO_CLASS}/students/${USER}                      # Where you will store the output
PATH_TO_ACTIVITY=${PATH_TO_CLASS}/data/alignment         # This is where the activity data is stored

# code
python3 /courses/BINF6310.202410/students/courtney.c/esm-variants/esm_score_missense_mutations_mod.py --input-fasta-file ${PATH_TO_ME}/esm-variants/uniprot-filtered-reviewed_yes_Human_isoforms.fasta --output-csv-file scratch/${USER}/test.csv
