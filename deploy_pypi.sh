python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf dist
rm -rf build
rm -rf *.egg-info
rm -rf microdb-*.*.*
version=$(cat version.txt)
git add .
git commit -m version$version
git push
sleep 30
pip install microdb --upgrade
read -sp 'enter something to finish' dummy
