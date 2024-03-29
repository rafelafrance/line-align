#!/usr/bin/env python3
from glob import glob

from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "line_align",
        sorted(glob("char_matrix/cpplib/*.cpp")),  # noqa: PTH207
    ),
]

setup(
    ext_modules=ext_modules,
)
