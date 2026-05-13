#!/bin/bash

RECEITA=20000
FOLHA=6000

# Fator R
FATOR=$(echo "$FOLHA / $RECEITA" | bc -l)

# Simples III (~6%)
SIMPLES3=$(echo "$RECEITA * 0.06" | bc)

# Simples V (~15%)
SIMPLES5=$(echo "$RECEITA * 0.15" | bc)

# Presumido (~13%)
PRESUMIDO=$(echo "$RECEITA * 0.13" | bc)

echo "==== CENÁRIOS ===="
echo "Simples III: $SIMPLES3"
echo "Simples V: $SIMPLES5"
echo "Presumido: $PRESUMIDO"

# Escolha automática
MENOR=$SIMPLES3
REGIME="Simples Anexo III"

if (( $(echo "$SIMPLES5 < $MENOR" | bc -l) )); then
  MENOR=$SIMPLES5
  REGIME="Simples Anexo V"
fi

if (( $(echo "$PRESUMIDO < $MENOR" | bc -l) )); then
  MENOR=$PRESUMIDO
  REGIME="Lucro Presumido"
fi

echo ""
echo "👉 Melhor regime: $REGIME"
echo "💰 Imposto: R$ $MENOR"

echo ""
echo "Fator R: $FATOR"

