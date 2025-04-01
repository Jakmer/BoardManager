#!/bin/sh

echo "------------------------------------------"
if [ ! -f /usr/local/bin/mj ]; then
    echo "Installing mj.py to /usr/local/bin"
    sudo cp src/mj.py /usr/local/bin/mj
    echo "File mj.py installed to /usr/local/bin"
else
    echo "File mj.py already exists in /usr/local/bin"
fi
echo "------------------------------------------"

echo "------------------------------------------"
if [ ! -f "$HOME/.local/lib/python3.10/site-packages/mj_utils.py" ]; then
    cp src/mj_utils.py "$HOME/.local/lib/python3.10/site-packages"
    echo "File mj_utils.py installed in $HOME/.local/lib/python3.10/site-packages"
else
    echo "File mj_utils.py already exists in $HOME/.local/lib/python3.10/site-packages"
fi
echo "------------------------------------------"

echo "------------------------------------------"
if ! pip show argcomplete > /dev/null 2>&1; then
    pip install argcomplete
    echo "Lib argcomplete installed"
else
    echo "Lib argcomplete is already installed"
fi
echo "------------------------------------------"

echo "------------------------------------------"
if ! grep -q 'eval "$(register-python-argcomplete mj)"' "$HOME/.bashrc"; then
    echo 'eval "$(register-python-argcomplete mj)"' >> "$HOME/.bashrc"
    echo 'Line: eval "$(register-python-argcomplete mj)" added to ~/.bashrc'
else
    echo "Line already exists in .bashrc"
fi
echo "------------------------------------------"

