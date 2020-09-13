rel_name=$1
cd ~/code/fabric-qa/text_to_table/baseline/ir_rc
./run_bionlp.sh sample_qas ${rel_name} 80
