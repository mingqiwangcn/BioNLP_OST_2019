import csv
import glob
from tqdm import tqdm
import json
import os
from qa_engine.answer_ranker.rc_model import get_rc_model
from text_to_table.reader.albert.qa_data import data_to_examples

def read_rel_types(file_path):
    rel_type_set = set()
    with open(file_path) as f:
        for line in f:
            item = json.loads(line)
            rel_type = item[1]
            rel_type_set.add(rel_type)
    
    rel_type_lst = list(rel_type_set)
    return rel_type_lst

def get_qas_rels(file_path):
    qas_data = []
    rel_data = []
    with open(file_path) as f:
        for line in f:
            item = json.loads(line)
            qid = item[0]
            question = item[1]
            rel_type = item[2]
            template = item[3]
            subject = item[4]
            object_lst = item[5]
            qas_info = {
                'qid':qid,
                'question':question,
                'answers':object_lst,
                'subject':subject
            }
            rel_info = {
                'rel_type':rel_type,
                'template':template,
                'subject':subject,
                'objects':object_lst,
                'id':qid
            }
            qas_data.append(qas_info)
            rel_data.append(rel_info)
    
    return (qas_data, rel_data)

def get_open_qa(file_path, qas_data, reader):
    qas_map = index_qas_data(qas_data)
    data = {}
    qid_lst = []
    with open(file_path) as f:
        csv_reader = csv.reader(f)
        for idx, row_data in enumerate(csv_reader):
            if idx == 0:
                continue
            seq_no = row_data[0]
            qid = row_data[1]
            question = qas_map[qid]['question']
            passage = row_data[6]
            answer_text = row_data[7].strip()
            correct = row_data[8].lower()
            if qid not in data:
                qid_lst.append(qid)
                data[qid] = {
                    'qid':qid,
                    'question':question,
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
    
    item_lst = []
    for qid in qid_lst:
        item = data[qid]
        update_answers(item, reader)
        item_lst.append(item)

    return item_lst

def update_answers(item, reader):
    passage_lst = item['passages']
    answer_lst = item['answers']

    for idx, answer_info in enumerate(answer_lst):
        new_item = {
            'qid':item['qid'],
            'question':item['question'],
            'passages':[passage_lst[idx]],
            'p_id_lst':[idx]
        }
        new_batch_data = [new_item]
        batch_examples = data_to_examples(new_batch_data)
        reader_out = reader(batch_examples)
        preds = reader_out['preds']
        qas_id = '%s_%d' % (item['qid'], idx)
        pred_item = preds[qas_id]
        answer_text = pred_item['text']
        if answer_info[0]['answer'] == '':
            answer_info[0]['answer'] = answer_text
        else:
            if answer_text != answer_info[0]['answer']:
                if answer_info[0]['em'] == 1:
                    case_1 = (item['qid'] == 'bb_train_22') and (idx == 2)
                    case_2 = (item['qid'] == 'seedev_train_965') and (idx == 1)
                    case_3 = (item['qid'] == 'bb_train_195') and (idx == 1)
                    if case_1 or case_2 or case_3:
                        answer_info[0]['em'] = 0
                        answer_info[0]['f1'] = 0.0

                answer_info[0]['answer'] = answer_text

        pred_start_index = pred_item['start_index']
        pred_end_index = pred_item['end_index']
        
        if pred_start_index is None:
            pred_start_index = 0

        if pred_end_index is None:
            pred_end_index = 0
        
        answer_info[0]['start_index'] = pred_start_index
        answer_info[0]['end_index'] = pred_end_index

def index_qas_data(qas_data):
    qas_map = {}
    for qas_info in qas_data:
        qid = qas_info['qid']
        qas_map[qid] = qas_info
    return qas_map 

def index_rel_data(rel_data):
    rel_map = {}
    for rel_info in rel_data:
        qid = rel_info['id']
        rel_map[qid] = rel_info  
    return rel_map 

def update_qas_rel_objects(open_qa_data, qas_data, rel_data):
    qas_map = index_qas_data(qas_data)
    rel_map = index_rel_data(rel_data)
    for item in open_qa_data:
        qid = item['qid']
        answer_lst = item['answers']
        object_lst = rel_map[qid]['objects']
        object_set = set(object_lst)
        for answer in answer_lst:
            em = answer[0]['em']
            if em > 0:
                answer_text = answer[0]['answer']
                object_set.add(answer_text)
        updated_object_lst = list(object_set)
        rel_map[qid]['objects'] = updated_object_lst
        qas_map[qid]['answers'] = updated_object_lst

def output_data(f_o, data):
    for item in data:
        f_o.write(json.dumps(item) + '\n')

def get_reader():
    reader_path = '/home/cc/model/reader/albert/albert-base-v2/checkpoint_21000/model/'
    reader = get_rc_model('albert', reader_path, 0)
    return reader
  
def main():
    out_qas_file = './output/test_annotation_qas.json'
    out_rel_file = './output/test_annotation_rels.json'
    out_open_qa_file = './output/test_annotation_open_qa.json'
   
    reader =get_reader() 
    f_o_qas = open(out_qas_file, 'w')
    f_o_rel = open(out_rel_file, 'w')
    f_o_open_qa = open(out_open_qa_file, 'w')
    
    question_file = '../qas/sample_qas/sample_qids.txt'
    rel_type_lst = read_rel_types(question_file)
    for rel_type in tqdm(rel_type_lst):
        qas_rel_file = '../qas/sample_qas/%s_questions.txt' % rel_type
        qas_data, rel_data = get_qas_rels(qas_rel_file)
        annotation_file = '../annotation/task/%s_Annotation.csv' % rel_type
        open_qa_data = get_open_qa(annotation_file, qas_data, reader)
        update_qas_rel_objects(open_qa_data, qas_data, rel_data)
        output_data(f_o_qas, qas_data)
        output_data(f_o_rel, rel_data)
        output_data(f_o_open_qa, open_qa_data)
    f_o_qas.close()
    f_o_rel.close()
    f_o_open_qa.close()     


if __name__ == '__main__':
    main()
