#/usr/bin/env bash
for bed_file in ./bed_files/*.bed; do
    output_file="./output/bed_sh/$(basename "$bed_file" .bed).fa"
    bedtools getfasta -fi ./reference/hg38.fa -bed "$bed_file" -fo "$output_file"
done
