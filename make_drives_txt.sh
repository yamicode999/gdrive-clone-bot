#!/bin/bash

echo -e "Walk through this interactive script to make the drives.txt file which will be used for multi drives/folders search.\n"

if [ -e drives.txt ]; then
    lines=$(<drives.txt)
    if [ -n "$lines" ]; then
        echo -e "$lines\n"
        while true; do
            read -p "Do you wish to keep the above details that you previously added? (y/n) : " choice
            if [ $choice == 'y' ] || [ $choice == 'Y' ]; then
                msg="$lines\n"
                break
            elif [ $choice == 'n' ] || [ $choice == 'N' ]; then
                break
            else
                echo -e "Don't fuck around! Enter a valid response."
                continue
            fi
        done
    fi
fi

echo ""
read -p "How many drives/folders do you want to add? : " num

for (( count=1; count<=$num; count++ )); do
    echo -e "\n> DRIVE - $count\n"
    read -p "Enter Drive NAME                 : " name
    read -p "Enter Drive ID                   : " id
    read -p "Enter Drive INDEX URL (optional) : " index

    if [ -z "$name" ] || [ -z "$id" ]; then
        echo -e "\nERROR! Please do not leave the name or id field blank."
        exit 1
    fi

    name=$(echo $name | tr ' ' '_')
    if [ -n "$index" ]; then
        if [ "${index: -1}" == "/" ]; then
            index="${index%?}"
        fi
    else
        index=""
    fi

    msg+="$name $id $index\n"
done

echo -e "$msg" > drives.txt
echo -e "\nDone!"
