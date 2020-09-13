cat rel_name_samples.txt | while read rel_name; do
    echo ${rel_name}
    ./gen_ir_rc_data.sh ${rel_name}
done
