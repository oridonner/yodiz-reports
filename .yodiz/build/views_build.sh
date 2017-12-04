#!/bin/bash
target_dir=.yodiz/build

echo > $target_dir/views_build.sql

for dir in $(find ./.yodiz/db_objects/ | grep "views" | grep -ve "./.yodiz/db_objects/build/views_build.sql" | sort);do
    [[ -d $dir ]] && continue # if directory then skip
    #skip log
    #if echo $dir | grep -q "_log.sql"; then
    #   continue;
    #fi
    sed '/^\s*$/d' "$dir" >> "$target_dir/views_build.sql"
    cat <(echo) <(echo) >> $target_dir/views_build.sql
done