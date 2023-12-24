#!/usr/bin/env bash 

#SBATCH --job-name=tied_73
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:rtx_2080:1
#SBATCH --partition gpu_short
#SBATCH --time=05:00:00
#SBATCH --mem=4G

## system error message output file
## leave %j as it's being replaced by JOB ID number
#SBATCH -e err_%j.txt

## system message output file
#SBATCH -o out_%j.txt

# load relevant modules
# module load lang/cuda
module load lang/python/anaconda/pytorch

# change to working directory, where the job was submitted from.
cd "${SLURM_SUBMIT_DIR}"

# record details about the job: 
echo "Running on host $(hostname)"
echo "Started on $(date)"
echo "Directory is $(pwd)"
echo "Slurm job ID is ${SLURM_JOBID}"
echo "This jobs runs on the following machines:"
echo "${SLURM_JOB_NODELIST}" 
printf "\n\n"

time python "main.py" --data "data/" --save "models/mtied73.pt" --log "models/mtied73.txt" --emsize 650 --nhid 650 --epochs 50 --seed 73 --batch_size 128 --tied --cuda 
# print ending time:
printf "\n\n"
echo "Ended on: $(date)"


