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

# if __name__ == '__main__':
#     json_list = ['../output_json/individual/miami_2021-06-28_17-43-48_test_title_veh_3_lt_1_ut_2.json',
#                  '../output_json/individual/miami_2021-06-28_17-43-49_test_title_veh_4_lt_1_ut_2.json',
#                  '../output_json/individual/miami_2021-06-28_17-43-50_test_title_veh_5_lt_1_ut_2.json']
#     # print(json_list)
#     merge_json_files(json_list, '../output_json/collection/test_title.json')
