#!/usr/bin/env python3
"""
turn a CSV spreadsheet of Genki chapter vocab into a YAML template file

run this from the base directory of the git repo so that the paths are correct
"""
import csv, sys, os


yaml_head = """sound_file: {sound_file}
skip_words: []
skip_on_beginning: 2
skip_with_new_category: true
skip_on_semicolon: true
uid: {uid}
sound_silence_threshold: 600
cards:"""

yaml_category = """- category: {category}
  vocabulary:"""

yaml_vocab = """  - japanese: {kana}
    english: {english}
    kanji: {kanji}"""

infile = sys.argv[1]
output = []

# example infile name: L13_02_supplemental_vocab.csv
chapter_num = os.path.basename(infile).split('_')[0].strip('L')
file_num = os.path.basename(infile).split('_')[1]
outbasename = '_'.join(os.path.basename(infile).split('_')[1:]).replace('csv', 'yaml')
outdir = os.path.join('data', 'genki_2', 'templates', 'L%s' % chapter_num)
outpath = os.path.join(outdir, outbasename)

def gen_uid(infile):
    genki_2_base_uid = 7000000000
    # TODO: infer the chapter and file index (e.g. 01_vocab.yaml 02_extra_vocab.yaml) from the infile
    return str(genki_2_base_uid + 100 * int(chapter_num) + int(file_num))

with open(infile, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    sound_file = None
    cur_category = None
    for row in csvreader:
        if not sound_file and row['sound_file']:
            output.append(yaml_head.format(sound_file=row['sound_file'], uid=gen_uid(infile)))
            
        if row['category']:
            output.append(yaml_category.format(category=row['category']))
            cur_category = row['category']
        # add the '(な)' if it is missing for 形容動詞 (な-adjectives)
        if cur_category == 'な-adjectives':
            if not row['kana'].endswith('(な)'):
                row['kana'] = row['kana'] + '(な)'
        # CSV naturally gives None type for empty columns but
        # something later in the scripts barfs on that type of input, we will try to assure
        # we write "''" into the yaml template instead
        for key in ['english', 'kanji']:
            if row[key] in [None, '']:
                row[key] = """\'\'"""
        
        output.append(yaml_vocab.format(kana=row['kana'],
                                english=row['english'],
                                kanji=row['kanji']))

#print('\n'.join(output))


if not os.path.exists(outpath) or input('overwrite existing %s ?(y/n)' % outpath) == 'y':
    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % outdir)
    outfile = open(outpath, 'w+')
    outfile.write('\n'.join(output) + '\n')
    outfile.flush()
    outfile.close()
else:
    print('not writing yaml file')

print(outpath)
