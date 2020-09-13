if [ "$#" -ne 1 ]; then
    echo "Usage: ./gen_exp_data.sh [rel_name]"
    exit
fi
rel_name=$1
cd ~/code/fabric-qa/text_to_table/data_process/BioNLP_OST_2019
expert_rel_data_dir=~/code/fabric-qa/text_to_table/albert_relation/data/bionlp
python create_albert_rel_data.py --questions ~/data/BioNLP_OST_2019/qas/sample_qas/${rel_name}_questions.txt \
        --preds ~/code/fabric-qa/text_to_table/baseline/ir_rc/output/bionlp/${rel_name}_top_80/preds_detail.txt \
        --output ${expert_rel_data_dir}/${rel_name}_sample_dev.json
cd ~/code/fabric-qa/text_to_table/albert_relation
out_dir=~/code/fabric-qa/text_to_table/albert_relation/output/bionlp/${rel_name}
if [ ! -d "${out_dir}" ]; then
    mkdir ${out_dir}
fi
./eval_boionlp.sh ${out_dir} ${rel_name} 10
cd ${out_dir}
../../../gen_expt_rel_analysis.sh ${rel_name}
