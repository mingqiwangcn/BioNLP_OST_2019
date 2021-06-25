from predictor import OpenRel
import json
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('qas_data', type=str)
    args = parser.parse_args()
    return args

def get_query_lst(args):
    file_path = '/home/cc/data/BioNLP_OST_2019/qas/%s' % args.qas_data
    query_lst = []
    with open(file_path) as f:
        for line in f:
            item = json.loads(line)
            query_lst.append(item)
    return query_lst

def main():
    args = get_args()
    open_rel = OpenRel(
                ir_host='127.0.0.1',
                ir_port=9200,
                ir_index='pubmed',
                model_dir='../model', 
                cuda=0)
    query_lst = get_query_lst(args)
    res_lst = open_rel.search(query_lst)
    out_file = 'bionlp_preds.json'
    with open(out_file, 'w') as f_o:
        for res in res_lst:
            f_o.write(json.dumps(res) + '\n')


if __name__ == '__main__':
    main()
