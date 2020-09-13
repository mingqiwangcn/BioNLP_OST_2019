rel_name=$1
dir1=~/code/fabric-qa/text_to_table/baseline/ir_rc/output/bionlp/${rel_name}_top_80
if [ -d $dir1 ]; then
    rm -rf $dir1
    echo "$dir1 deleted"
else
    echo "$dir1 does not exists"
fi
dir2=~/code/fabric-qa/text_to_table/albert_relation/output/bionlp/${rel_name}
if [ -d $dir2 ]; then
    rm -rf $dir2
    echo "$dir2 deleted"
else
    echo "$dir2 does not exists"
fi


