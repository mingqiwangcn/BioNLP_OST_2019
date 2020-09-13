rel_name=$1
cd ~/code/fabric-qa/text_to_table/baseline/ir_rc
./run_bionlp.sh ~/data/BioNLP_OST_2019/qas/sample_qas ${rel_name} 80
