#include "line_align.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(line_align_py, m) {
    m.doc() = "Align multiple strings.";

    py::class_<LineAlign>(m, "LineAlign")
        .def(py::init<const std::unordered_map<std::u32string, float>&, float, float, char32_t>(),
             py::arg("substitutions") = noSubs,
             py::arg("gap") = -2.0,
             py::arg("skew") = -2.0,
             py::arg("gap_char") = U'⋄')
        .def("align", &LineAlign::align,
             "Get a multiple sequence alignment for a list of strings.",
             py::arg("strings"))
        .def("levenshtein", &LineAlign::levenshtein,
             "Get the levenshtein distance for 2 strings.")
        .def("levenshtein_all", &LineAlign::levenshtein_all,
             "Get the levenshtein distance for all pairs of strings in the list.");
}

/*
  <%
  cfg['compiler_args'] = ['-std=c++17']
  cfg['sources'] = ['line_align.cpp']
  setup_pybind11(cfg)
  %>
*/
