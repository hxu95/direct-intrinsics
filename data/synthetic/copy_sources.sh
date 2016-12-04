#! /bin/bash

cd sources

# 90 / 10 split
cp source_shadow_full.txt source_shadow_test.txt
cp source_shadow_full.txt source_shadow_train.txt

cp source_noshadow_full.txt source_noshadow_test.txt
cp source_noshadow_full.txt source_noshadow_train.txt

# scene split
cp source_shadow_full.txt source_shadow_test_2.txt
cp source_shadow_full.txt source_shadow_train_2.txt

cp source_noshadow_full.txt source_noshadow_test_2.txt
cp source_noshadow_full.txt source_noshadow_train_2.txt

#do the rest manually
