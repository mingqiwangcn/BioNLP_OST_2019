rel=$1
python ~/code/fabric-qa/text_to_table/data_process/BioNLP_OST_2019/sample_qas.py --data_tag qas/bionlp --rel_names ${rel} --output_tag sample_qas/${rel}
