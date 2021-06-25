import json
import numpy as np
import pandas as pd

def get_qas_data():
    qas_data = {}
    with open('/home/cc/data/BioNLP_OST_2019/qas/bionlp_test_qas.json') as f:
        for line in f:
            item = json.loads(line)
            qid = item['qid']
            qas_data[qid] = item
    return qas_data

def main():
    qas_data = get_qas_data()
    data = []
    col_name_lst = ['qid', 'rel_name', 'subject', 'question', 'p_id', 'passage', 'answers', 'correct']
    with open('./bionlp_preds.json') as f:
        for line in f:
            item = json.loads(line)
            qid = item['qid']
            p_id_lst = item['p_id_lst']
            passage_lst = item['passages']
            answer_lst = item['answers']
            open_qa_score_lst = item['expert_scores']['open_qa']['scores']
            open_qa_max_idx = np.argmax(open_qa_score_lst)
            ensemble_max_idx = 0
            
            rel_name = item['rel_name']
            subject = item['subject']
            question = item['question']
           
            ref_answers = qas_data[qid]['answers']
            ref_answer_text = '\n'.join(ref_answers)
            detail_question = [
                qid, rel_name, subject, question, '', '', ref_answer_text, ''
            ]

            detail_open_qa = [
                qid, '', '', '', p_id_lst[open_qa_max_idx], passage_lst[open_qa_max_idx],
                answer_lst[open_qa_max_idx]['answer'], ''
            ]

            detail_ensemble = [
                qid, '', '', '', p_id_lst[ensemble_max_idx], passage_lst[ensemble_max_idx],
                answer_lst[ensemble_max_idx]['answer'], ''
            ]

            assert(len(detail_question) == len(col_name_lst))
            data.append(detail_question)

            assert(len(detail_open_qa) == len(col_name_lst))
            data.append(detail_open_qa)

            assert(len(detail_ensemble) == len(col_name_lst))
            data.append(detail_ensemble)
    
    df = pd.DataFrame(data, columns=col_name_lst)
    df.to_csv('bionlp_expert_top_preds.csv')

if __name__ == '__main__':
    main()
