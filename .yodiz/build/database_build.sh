#!/bin/bash
target_dir=.yodiz/build

echo > $target_dir/database_build.sql

for dir in $(find ./.yodiz/db_objects/ | grep "\.sql$" | grep -ve "./.yodiz/db_objects/build/database_build.sql" | sort);do
    [[ -d $dir ]] && continue # if directory then skip
    #skip log
    #if echo $dir | grep -q "_log.sql"; then
    #   continue;
    #fi
    sed '/^\s*$/d' "$dir" >> "$target_dir/database_build.sql"
    cat <(echo) <(echo) >> $target_dir/database_build.sql
done