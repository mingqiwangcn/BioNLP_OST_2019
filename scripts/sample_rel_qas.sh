cat rel_name_samples.txt | while read rel_name; do
    echo ${rel_name}
    ./sample_qas.sh ${rel_name}
done
