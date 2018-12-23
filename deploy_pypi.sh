
version=$(cat version_texts/version_digitgood.txt)
commit_msg=$(cat version_texts/commit_message.txt)
git add version_texts/version_digitgood.txt version_texts/version_raw.txt version_texts/commit_message.txt
git commit -m "version ${version} ${commit_msg}"
git push
git stash
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist
rm -rf build
rm -rf *.egg-info
rm -rf microdb-*.*.*
git stash pop
