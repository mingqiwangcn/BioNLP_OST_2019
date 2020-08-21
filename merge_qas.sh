#!/bin/bash
for file_path in **/*_questions.txt; do
    cat ${file_path} >> bionlp_questions.txt
done
for file_path in **/*_answers.txt; do
    cat ${file_path} >> bionlp_answers.txt
done
