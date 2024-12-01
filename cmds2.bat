prefetch SRR22924497
fasterq-dump --threads 12 SRR22924497
kallisto quant -i kallisto_index -o kallisto_output7 --single -l 91 -s 15 -t 12 SRR22924497.fastq
del SRR22924497.fastq
rd /s /q "SRR22924497"

prefetch SRR22924507
fasterq-dump --threads 12 SRR22924507
kallisto quant -i kallisto_index -o kallisto_output8 --single -l 91 -s 15 -t 12 SRR22924507.fastq
del SRR22924507.fastq
rd /s /q "SRR22924507"

prefetch SRR22924387
fasterq-dump --threads 12 SRR22924387
kallisto quant -i kallisto_index -o kallisto_output9 --single -l 91 -s 15 -t 12 SRR22924387.fastq
del SRR22924387.fastq
rd /s /q "SRR22924387"

prefetch SRR22924389
fasterq-dump --threads 12 SRR22924389
kallisto quant -i kallisto_index -o kallisto_output10 --single -l 91 -s 15 -t 12 SRR22924389.fastq
del SRR22924389.fastq
rd /s /q "SRR22924389"

prefetch SRR22924489
fasterq-dump --threads 12 SRR22924489
kallisto quant -i kallisto_index -o kallisto_output11 --single -l 91 -s 15 -t 12 SRR22924489.fastq
del SRR22924489.fastq
rd /s /q "SRR22924489"