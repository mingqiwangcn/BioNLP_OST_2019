1)Generate all qas
python ~/code/fabric-qa/text_to_table/data_process/BioNLP_OST_2019/gen_qas.py --output_dir qas

2)Get part of qas
python ~/code/fabric-qa/text_to_table/data_process/BioNLP_OST_2019/get_qas_by_rel.py --data_tag qas/bionlp --rel_names GOF --output_tag temp/GOF
