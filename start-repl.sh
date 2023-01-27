if [ ! -d "venv" ]; then
    python3 -m venv venv --upgrade-deps \
    && venv/bin/pip3 install --no-cache-dir -U wheel \
    && venv/bin/pip3 install --no-cache-dir -Ur requirements.txt \
    && reset
fi

source venv/bin/activate
python3 -Bc "import pathlib; import shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
gunicorn --bind 0.0.0.0:$PORT web.wserver:app \
& python3 -m bot