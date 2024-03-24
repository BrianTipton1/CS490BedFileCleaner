import os
from pathlib import Path
from os.path import dirname, basename, join
from shutil import copytree, rmtree
from typing import List, Tuple

SCRIPT_DIR = dirname(__file__)
DOWNLOADED_BED = join(SCRIPT_DIR, "downloaded_bed")
OUT_DIR = join(SCRIPT_DIR, "output")
REF_DIR = join(SCRIPT_DIR, "reference")

POS_DIR = join(OUT_DIR, "positive")
NEG_DIR = join(OUT_DIR, "negative")

MAIN_REF = join(REF_DIR, "hg38.fa")


def get_evens(files: List[str]):
    even_enum = filter(lambda ix: ix[0] % 2 != 0, enumerate(files))
    return list(map(lambda x: x[1].strip(), even_enum))


def get_avg_len(file_path: Path):
    with open(file_path) as f:
        lines = get_evens(f.readlines())
        n_lines = len(lines)
        n_characters = sum(map(lambda x: len(x), lines))
        return n_characters // n_lines


def trim(file_path: Path, seq_path: Path, crop_path: Path, n: int):
    with open(file_path) as f:
        lines = get_evens(f.readlines())
        with open(seq_path, "w+") as s:
            s.writelines(list(map(lambda x: f"{x}\n", lines)))
            s.close()
        trimmed = list(map(lambda x: f"{x[:n]}", lines))
        after_discard = list(filter(lambda x: len(x) == n, trimmed))
        with open(crop_path, "w+") as c:
            c.writelines(list(map(lambda x: f"{x}\n", after_discard)))
            c.truncate()
            c.close()


def create_negative(bed_file: Path, out_file: Path):
    lines = open(bed_file).readlines()
    splits = list(map(lambda x: x.strip().split("\t"), lines))
    ranges = list(map(lambda x: (x[0], int(x[1]), int(x[2])), splits))
    
    new_ranges: List[Tuple[str, int, int]] = []
    
    for i in range(len(ranges) - 1):
        rg = ranges[i]
        next_rg = ranges[i + 1]
        
        if rg[0] == next_rg[0]: 
            start = rg[2] + 1
            end = next_rg[1] - 1
            if start < end:
                new_ranges.append((rg[0], start, end))
    
    new_lines = map(lambda x: f"{x[0]}\t{x[1]}\t{x[2]}\n", new_ranges)
    open(out_file, "w+").writelines(new_lines)


def run_beds(dir, out_dir):
    for file in os.scandir(dir):
        out_file = join(out_dir, basename(Path(file).stem))
        print(file.name)
        os.system(
            f'bedtools getfasta -fi {MAIN_REF} -bed "{file.path}" -fo "{out_file}.fa"'
        )


def init_dirs():
    dirs = [
        [
            join(OUT_DIR, x, "bed_output"),
            join(OUT_DIR, x, "cropped"),
            join(OUT_DIR, x, "seqs"),
            join(OUT_DIR, x, "bed_files"),
        ]
        for x in ["positive", "negative"]
    ]
    [
        Path(join(SCRIPT_DIR, y)).mkdir(exist_ok=True, parents=True)
        for x in dirs
        for y in x
    ]


def create_and_clean_pos():
    bed_out = join(POS_DIR, "bed_output")
    bed_file_dir = join(POS_DIR, "bed_files")

    copytree(DOWNLOADED_BED, bed_file_dir, dirs_exist_ok=True)

    run_beds(bed_file_dir, bed_out)

    files = list(map(Path, os.scandir(bed_out)))
    avg_lens = [(x, get_avg_len(x)) for x in files]

    [
        trim(
            file_path=x,
            seq_path=Path(join(POS_DIR, "seqs", x.name)).with_suffix(".sequence"),
            crop_path=Path(join(POS_DIR, "cropped", x.name)).with_suffix(".cropped"),
            n=n,
        )
        for x, n in avg_lens
    ]


def create_and_clean_negs():
    [
        create_negative(
            Path(x), Path(join(NEG_DIR, "bed_files", x.name)).with_suffix(".bed")
        )
        for x in os.scandir(DOWNLOADED_BED)
    ]
    run_beds(Path(NEG_DIR, "bed_files"), Path(NEG_DIR, "bed_output"))
    files = list(map(Path, os.scandir(Path(NEG_DIR, "bed_output"))))
    avg_lens = [(x, get_avg_len(x)) for x in files]
    [
        trim(
            file_path=x,
            seq_path=Path(join(NEG_DIR, "seqs", x.name)).with_suffix(".sequence"),
            crop_path=Path(join(NEG_DIR, "cropped", x.name)).with_suffix(".cropped"),
            n=n,
        )
        for x, n in avg_lens
    ]


if __name__ == "__main__":
    os.system(join(SCRIPT_DIR, 'get_all.sh')) # For testing you cacommented out once they are initially downloaded... 
    rmtree(OUT_DIR) # MAybe unneccesary but i was sick of the dirs being dirty before testing each time 
    init_dirs()
    create_and_clean_pos()
    create_and_clean_negs()
