#/usr/bin/env bash
#
all_beds=(
  "https://www.encodeproject.org/files/ENCFF089TRW/@@download/ENCFF089TRW.bed.gz"
  "https://www.encodeproject.org/files/ENCFF265ZRC/@@download/ENCFF265ZRC.bed.gz"
  "https://www.encodeproject.org/files/ENCFF839QLN/@@download/ENCFF839QLN.bed.gz"
  "https://www.encodeproject.org/files/ENCFF870FOG/@@download/ENCFF870FOG.bed.gz"
  "https://www.encodeproject.org/files/ENCFF561HFN/@@download/ENCFF561HFN.bed.gz"
  "https://www.encodeproject.org/files/ENCFF863XOL/@@download/ENCFF863XOL.bed.gz"
  "https://www.encodeproject.org/files/ENCFF402BMP/@@download/ENCFF402BMP.bed.gz"
  "https://www.encodeproject.org/files/ENCFF188HUC/@@download/ENCFF188HUC.bed.gz"
  "https://www.encodeproject.org/files/ENCFF436SLI/@@download/ENCFF436SLI.bed.gz"
  "https://www.encodeproject.org/files/ENCFF828FGS/@@download/ENCFF828FGS.bed.gz"
)

for b in "${all_beds[@]}"
do
  wget $b --directory-prefix=./downloaded_bed
done

gunzip -f ./downloaded_bed/*.bed.gz
