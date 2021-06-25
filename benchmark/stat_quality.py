import csv
import numpy as np

def main():
    with open('./bionlp_pred_labels.csv', 'r') as f:
        reader = csv.reader(f)
        data = {}
        for idx, line in enumerate(reader):
            if idx == 0:
                continue
            qid = line[0]
            rel_name = line[1]
            label = line[2]
            if qid not in data:
                data[qid] = []

            item_lst = data[qid]
            item_lst.append({'qid':qid, 'rel_name':rel_name, 'label':label})
    process_data(data)

def process_data(data):
    rel_name_data = {}
    for qid in data:
        item_lst = data[qid]
        assert(len(item_lst) == 3)
        rel_name = item_lst[0]['rel_name']
        open_qa_label = item_lst[1]['label']
        ensemble_label = item_lst[2]['label']

        assert(rel_name != '')
        assert (open_qa_label in ['Y', 'N'])
        assert (ensemble_label in ['Y', 'N'])

        open_qa_correct = int(open_qa_label == 'Y')
        ensemble_correct = int(ensemble_label == 'Y')

        if rel_name not in rel_name_data:
            rel_name_data[rel_name] = {'open_qa':[], 'ensemble':[]}
        
        pred_info = rel_name_data[rel_name]
        open_qa_lst = pred_info['open_qa']
        open_qa_lst.append(open_qa_correct)
        ensemble_lst = pred_info['ensemble']
        ensemble_lst.append(ensemble_correct)
    
    start_data(rel_name_data)

def start_data(rel_name_data):
    for rel_name in rel_name_data:
        pred_info = rel_name_data[rel_name]
        open_qa_lst = pred_info['open_qa']
        open_qa_em = round(np.mean(open_qa_lst) * 100, 2)
        ensemble_lst = pred_info['ensemble']
        ensemble_em = round(np.mean(ensemble_lst) * 100, 2)
        assert(len(open_qa_lst) == len(ensemble_lst))
        print(rel_name, len(open_qa_lst), open_qa_em, ensemble_em)


main()
