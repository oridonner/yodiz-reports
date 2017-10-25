source_dir=postgres/issues
target_dir=postgres/build

farm_hosts=(
tbl_issues.sql
vw_issues.sql
vw_issues_mtd.sql
vw_issues_user.sql
vw_issues_severity.sql
)

echo > $target_dir/issues_builder.sql
for i in ${farm_hosts[@]}; do
    sed '/^\s*$/d' $source_dir/$i >> $target_dir/issues_builder.sql
    cat <(echo) <(echo)>> $target_dir/issues_builder.sql
done
