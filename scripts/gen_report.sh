rel_name=$1
./sample_qas.sh ${rel_name} ; ./gen_ir_rc_data.sh ${rel_name} ; ./gen_exp_data.sh ${rel_name}
