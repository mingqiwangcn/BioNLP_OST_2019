rel=$1
data_dir=~/data/BioNLP_OST_2019
python ~/code/fabric-qa/text_to_table/data_process/BioNLP_OST_2019/sample_qas.py \
    --data_tag ${data_dir}/qas/bionlp \
    --rel_names ${rel} \
    --output_tag ${data_dir}/qas/sample_qas/${rel}
