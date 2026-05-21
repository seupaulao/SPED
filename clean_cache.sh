#!/bin/bash
cd /home/s817842443/PAULOJR/Estudos/SPED

# Remove __pycache__ do rastreamento do Git
git rm -r --cached __pycache__ 2>/dev/null

# Remove todos os .pyc do rastreamento
find . -name "*.pyc" -exec git rm --cached {} \; 2>/dev/null

# Commit
git commit -m "Remove __pycache__ and .pyc files from git tracking"

echo "Limpeza completa!"
