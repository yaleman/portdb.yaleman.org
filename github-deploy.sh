#!/bin/bash

set -e

echo "REPO: $GITHUB_REPOSITORY"
echo "ACTOR: $GITHUB_ACTOR"

remote_repo="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
remote_branch=${GH_PAGES_BRANCH:=gh-pages}

echo 'Building site 👷 '
poetry run pelican "${PELICAN_CONTENT_FOLDER:=content}" -o output -s "${PELICAN_CONFIG_FILE:=publishconf.py}"

echo 'Publishing to GitHub Pages 📤 '
pushd output
git init
git remote add deploy "$remote_repo"
git checkout $remote_branch || git checkout --orphan $remote_branch
git config user.name "${GITHUB_ACTOR}"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"
if [ "$GH_PAGES_CNAME" != "none" ]
then
    echo "$GH_PAGES_CNAME" > CNAME
fi
git add .

echo -n 'Files to Commit:' && find "$(pwd)" | wc -l
git commit -m "[ci skip] Automated deployment to GitHub Pages on $(date +%s%3N)"
git push deploy $remote_branch --force
rm -fr .git
popd

echo 'Successfully 🎉🕺💃 🎉 deployed to interwebs 🕸'