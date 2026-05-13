#!/bin/bash

RECEITA=20000

echo "Receita: R$ $RECEITA"

# Simples (estimado)
SIMPLES=$(echo "$RECEITA * 0.06" | bc)

# Presumido
PRESUMIDO=$(echo "$RECEITA * 0.13" | bc)

echo "Simples Nacional: R$ $SIMPLES"
echo "Lucro Presumido: R$ $PRESUMIDO"

