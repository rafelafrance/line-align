#!/usr/bin/env python3
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "line_align_py",
        sorted(glob("align/cpplib/*.cpp")),
    ),
]

setup(
    ext_modules=ext_modules,
)
