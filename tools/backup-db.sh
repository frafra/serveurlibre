#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
mkdir -p ../backup
cp serveurlibre.db ../backup/serveurlibre-$(date +%d%m%Y-%H%M).db
