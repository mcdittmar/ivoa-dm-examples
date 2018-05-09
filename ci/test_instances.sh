#!/bin/bash

test_instance () {
    local status=0

    input=$1.jovial
    output=$1.vot.xml

    ${JOVIAL} -i ${input} > ${output}

    # test is successful if the output validates. If the output doesn't validate the contents of the file may have
    # useful information, so we dump the contents of the file.
    xmllint --schema $SCHEMA --noout ${output} || { status=1; cat ${output}; }

    return $status
}

status=0

# get all filenames that end with .jovial and pass them to the test function, with the extension stripped.
for i in $(ls *.jovial); do
    test_instance ${i%.jovial} || status=-1;
done;

# Exit if any error where found previously, or if the git index is not clean, i.e. there are outdated output
# files. If there is a failure, log the git difference.
[[ $status = 0 ]] && git diff-index --quiet HEAD -- || { git --no-pager diff; exit $status; }
