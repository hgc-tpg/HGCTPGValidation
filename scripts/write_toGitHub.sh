#!/bin/bash
# This script has two purposes:
# 1) Generate a temporary token
# 2) Write into the PR thread in GitHub 

# Usage: ./HGCTPGValidation/scripts/write_toGitHub.sh $url $MESSAGE

echo '===> Write into the PR thread.'

# Check if there are 2 arguments supplied to the script
if (( $# != 2 ))
then
  echo "Usage: ./HGCTPGValidation/scripts/write_toGitHub.sh $url $MESSAGE"
  exit 1
fi

url="$1"
MESSAGE="$2"

# Generate a token, the command "set +x" is mandatory
set +x exec >> log_Jenkins; 
module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; 
module purge; module load python/3.9.9; 
# For the organization hgc-tpg
python /data/jenkins/workspace/create_token_hgc-tpg.py > /tmp/github_token
# For the organization test-org-hgctpg
#python /data/jenkins/workspace/create_token.py > /tmp/github_token

# Compose the url to be used for printing the message in the GitHub PR thread
# In the string "url" replace "pull" with "issues" and add at the end "comments"
url_comments1="${url/pull/issues}/comments"
# In the string "url_comments1" replace "github.com" with "api.github.com/repos"
url_comments2="${url_comments1/github.com/api.github.com/repos}"
GITHUB_ACCESS_TOKEN=$(cat /tmp/github_token)
if [[ -z "${GITHUB_ACCESS_TOKEN}" ]]; then
    echo 'The github access token has not been generated.'
else
    echo "{\"body\": \"$MESSAGE\"}"
    curl -X POST -H "Authorization: Bearer $GITHUB_ACCESS_TOKEN " \
     -H "Accept: application/vnd.github+json" \
     -d "{\"body\": \"$MESSAGE\"}"  \
     "$url_comments2"
fi
rm -f /tmp/github_token

