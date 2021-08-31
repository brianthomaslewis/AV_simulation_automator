import json


def merge_json_files(file_list, output_fp):
    result = []
    for f1 in file_list:
        with open(f1, 'r') as infile:
            result.append(json.load(infile))

    with open(output_fp, 'w') as output_file:
        output_file.write('[\n')
        output_file.write(', \n'.join(map(json.dumps, result)))
        output_file.write('\n]')
