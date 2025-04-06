export PYTHONPATH="${PYTHONPATH}:/home/yqm/bootdev/StaticSiteBuilder/src/"

python3 src/main.py
python3 -m http.server 8888 --directory public