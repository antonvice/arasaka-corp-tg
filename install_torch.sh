#!/bin/bash

ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
    poetry add https://download.pytorch.org/whl/cpu/torch-2.1.2-cp39-none-manylinux1_x86_64.whl
elif [ "$ARCH" = "aarch64" ]; then
    poetry add https://download.pytorch.org/whl/cpu/torch-2.1.2-cp39-none-macosx_11_0_arm64.whl
else
    echo "Unsupported architecture"
    exit 1
fi