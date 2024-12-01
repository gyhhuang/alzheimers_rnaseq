prefetch SRR22924489
fasterq-dump --threads 8 SRR22924489
kallisto quant -i kallisto_index -o kallisto_output4 --single -l 91 -s 15 -t 12 SRR22924489.fastq
del SRR22924489.fastq
rd /s /q "SRR22924489"

prefetch SRR22924500
fasterq-dump --threads 8 SRR22924500
kallisto quant -i kallisto_index -o kallisto_output5 --single -l 91 -s 15 -t 12 SRR22924500.fastq
del SRR22924500.fastq
rd /s /q "SRR22924500"