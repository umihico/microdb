git add version_digitgood.txt version_raw.txt
git commit -m "version ${version} ${commit_msg}"
git push
git stash
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist
rm -rf build
rm -rf *.egg-info
rm -rf microdb-*.*.*
version=$(cat version_digitgood.txt)
commit_msg=$(cat commit_message.txt)
git stash pop
