#!/bin/bash
target_dir=.yodiz/build

echo > $target_dir/yodizdb_build.sql

for dir in $(find ./.yodiz/db_objects/ | grep "\.sql$" | grep -ve "./.yodiz/db_objects/build/yodizdb_build.sql" | sort);do
    [[ -d $dir ]] && continue # if directory then skip
    sed '/^\s*$/d' "$dir" >> "$target_dir/yodizdb_build.sql"
    cat <(echo) <(echo) >> $target_dir/yodizdb_build.sql
done