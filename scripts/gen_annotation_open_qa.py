import csv
import glob
from tqdm import tqdm
import json
import os

def read_sample_questions(file_path):
    sample_questions = {}
    rel_type_set = set()
    with open(file_path) as f:
        for line in f:
            item = json.loads(line)
            qid = item[0]
            rel_type = item[1]
            sample_questions[qid] = {'rel_type':rel_type}
            rel_type_set.add(rel_type)

    return (sample_questions, rel_type_set)

def gen_data(annotation_file, qas_file):
    data = {}
    with open(file_path) as f:
        csv_reader = csv.reader(f)
        for idx, row_data in enumerate(csv_reader):
            if idx == 0:
                continue
            seq_no = row_data[0]
            qid = row_data[1]
            passage = row_data[6]
            answer_text = row_data[7].strip()
            correct = row_data[8].lower()
            if qid not in data:
                data[qid] = {
                    'qid':qid,
                    'passages':[],
                    'answers':[]
                }
            item = data[qid]
            pasage_lst = item['passages']
            pasage_lst.append(passage)
            em = 0
            f1 = 0.0
            if (answer_text != '') and (correct == 'yes'):
                em = 1
                f1 = 1.0
            answer_lst = item['answers']
            answer_info = {
                'answer':answer_text,
                'em':em,
                'f1':f1
            }
            answer_lst.append([answer_info])
    return data
              
def main():
    out_qas_file = './output/test_annotation_qas.json'
    out_rel_file = './output/test_annotation_rels'
    out_open_qa_file = './output/test_annotation_open_qa.json'
    with open(out_file, 'w') as f_o:
        for csv_file in tqdm(csv_file_lst):
            data = gen_data(csv_file)
            for qid in data:
                item = data[qid]
                f_o.write(json.dumps(item) + '\n')

if __name__ == '__main__':
    main()
