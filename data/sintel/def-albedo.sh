cp sources/source_albedo_test.txt sources/source_albedo_defect_mask_test.txt
cp sources/source_albedo_train.txt sources/source_albedo_defect_mask_train.txt

sed -i 's/albedo/albedo_defect_mask/g' sources/source_albedo_defect_mask_test.txt
sed -i 's/albedo/albedo_defect_mask/g' sources/source_albedo_defect_mask_train.txt