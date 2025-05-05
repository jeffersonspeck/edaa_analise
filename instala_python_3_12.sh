#!/bin/bash

set -e

echo "Verificando versões instaladas..."
compgen -c python | sort | uniq

echo "Atualizando pacotes..."
sudo apt update

echo "Removendo versões antigas (exceto python3-base)..."
# Remove versões comuns antigas (ajuste conforme necessário)
sudo apt remove -y python3.6 python3.7 python3.8 python3.9 python3.10 python3.11 || true

echo "Instalando dependências para compilação (caso necessário)..."
sudo apt install -y software-properties-common

echo "Adicionando repositório de Python 3.12..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

echo "Instalando Python 3.12 e pip..."
sudo apt install -y python3.12 python3.12-venv python3.12-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

echo "Atualizando links simbólicos..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
sudo update-alternatives --set python3 /usr/bin/python3.12

sudo ln -sf /usr/local/bin/pip3.12 /usr/bin/pip3 || sudo ln -sf /usr/bin/pip3.12 /usr/bin/pip3

echo "Verificação final:"
python3 --version
pip3 --version
