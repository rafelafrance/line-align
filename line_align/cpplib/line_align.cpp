#include "line_align.hpp"
#include <algorithm>
#include <codecvt>
#include <cstddef>
#include <exception>
#include <iostream>
#include <iterator>
#include <limits>
#include <locale>
#include <numeric>
#include <sstream>
#include <utility>


// A utility function for converting a string from UTF-32 to UTF-8
std::string convert_32_8(const std::u32string &wides) {
    std::wstring_convert<std::codecvt_utf8<char32_t>, char32_t> conv;
    return conv.to_bytes(wides);
}

// A utility function for converting a string from UTF-8 to UTF-32
std::u32string convert_8_32(const std::string &bytes) {
    std::wstring_convert<std::codecvt_utf8<char32_t>, char32_t> conv;
    return conv.from_bytes(bytes);
}

LineAlign::LineAlign(
    const std::unordered_map<std::u32string, float>& substitutions,
    float gap,
    float skew,
    char32_t gap_char
)
{
    this->substitutions = substitutions;
    this->gap = gap;
    this->skew = skew;
    this->gap_char = gap_char;
}


// Modified from: https://en.wikipedia.org/wiki/Levenshtein_distance
int64_t LineAlign::levenshtein(
    const std::u32string &s,
    const std::u32string &t
) const
{
    const int64_t m = s.length();
    const int64_t n = t.length();

    std::vector<int64_t> v0(n + 1);
    std::vector<int64_t> v1(n + 1);

    for (int64_t i = 0; i <= n; ++i) {
        v0[i] = i;
    }

    for (int64_t i = 0; i < m; ++i) {
        v1[0] = i + 1;

        for (int64_t j = 0; j < n; ++j) {
            int64_t del = v0[j + 1] + 1;
            int64_t ins = v1[j] + 1;
            int64_t sub = s[i] == t[j] ? v0[j] : v0[j] + 1;

            int64_t min = del < ins ? del : ins;
            min = min < sub ? min : sub;

            v1[j + 1] = min;
        }
        v0.swap(v1);
    }
    return v0[n];
}


std::vector<std::tuple<int64_t, int64_t, int64_t>>
 LineAlign::levenshtein_all(const std::vector<std::u32string> &strings) const {
    const int64_t len = strings.size();

    std::vector<std::tuple<int64_t, int64_t, int64_t>> results;

    for (int64_t i = 0; i < len - 1; ++i) {
        for (int64_t j = i + 1; j < len; ++j) {
            auto dist = levenshtein(strings[i], strings[j]);
            results.push_back(std::make_tuple(dist, i, j));
        }
    }

    std::stable_sort(results.begin(), results.end(),
                     [](auto const &tuple1, auto const &tuple2) {
                         return std::get<0>(tuple1) < std::get<0>(tuple2);
                     });

    return results;
}

// Structures supporting the align() function.
enum TraceDir { none, diag, left, up };
struct Trace {
    float val;
    float up;
    float left;
    TraceDir dir;
    Trace() : val(0.0), up(0.0), left(0.0), dir(none) {}
};
typedef std::vector<std::vector<Trace>> TraceMatrix;


/* Implementation notes:
 * Building strings backwards in an attempt to prevent string copies in the backtrace loop.
 */
std::vector<std::u32string>
LineAlign::align(const std::vector<std::u32string> &lines) const {
    if (lines.size() <= 1) {
        return lines;
    }
    std::vector<std::u32string> aligned;
    aligned.push_back(lines[0]);

    for (size_t ln = 1; ln < lines.size(); ++ln) {
        // Build the matrix
        size_t rows = aligned[0].length();
        size_t cols = lines[ln].length();
        size_t rows_p1 = rows + 1;
        size_t cols_p1 = cols + 1;

        TraceMatrix trace(rows_p1, std::vector<Trace>(cols_p1));

        float penalty = this->gap;
        for (size_t row = 1; row < rows_p1; ++row) {
            trace[row][0].val = penalty;
            trace[row][0].up = penalty;
            trace[row][0].left = penalty;
            trace[row][0].dir = up;
            penalty += this->skew;
        }

        penalty = this->gap;
        for (size_t col = 1; col < cols_p1; ++col) {
            trace[0][col].val = penalty;
            trace[0][col].up = penalty;
            trace[0][col].left = penalty;
            trace[0][col].dir = left;
            penalty += this->skew;
        }

        for (size_t row = 1; row < rows_p1; ++row) {
            for (size_t col = 1; col < cols_p1; ++col) {
                Trace &cell = trace[row][col];
                Trace &cell_up = trace[row - 1][col];
                Trace &cell_left = trace[row][col - 1];

                cell.up = std::max({cell_up.up + this->skew, cell_up.val + this->gap});
                cell.left = std::max({
                    cell_left.left + this->skew, cell_left.val + this->gap});

                float diag_val = std::numeric_limits<float>::lowest();
                for (size_t k = 0; k < aligned.size(); ++k) {
                    char32_t aligned_char = aligned[k][rows - row];
                    char32_t lines_char = lines[ln][cols - col];

                    if (aligned_char == this->gap_char) {
                        continue;
                    }

                    if (aligned_char > lines_char) {
                        std::swap(lines_char, aligned_char);
                    }

                    std::u32string key = U"";
                    key += aligned_char;
                    key += lines_char;
                    float value;
                    try {
                        value = this->substitutions.at(key);
                    } catch (std::out_of_range &e) {
                        std::stringstream err;
                        err << "One of '" << convert_32_8(key)
                            << "' these characters are missing from the "
                            << "substitution matrix.";
                        throw std::invalid_argument(err.str());
                    }
                    diag_val = value > diag_val ? value : diag_val;
                }
                diag_val += trace[row - 1][col - 1].val;
                cell.val = std::max({diag_val, cell.up, cell.left});

                if (cell.val == diag_val) {
                    cell.dir = diag;
                } else if (cell.val == cell.up) {
                    cell.dir = up;
                } else {
                    cell.dir = left;
                }
            }
        }

        // Trace-back
        int64_t row = rows;
        int64_t col = cols;
        std::u32string new_line;

        std::vector<std::u32string> new_aligned;
        for (size_t k = 0; k < aligned.size(); ++k) {
            new_aligned.push_back(U"");
        }

        while (true) {
            Trace cell = trace[row][col];
            if (cell.dir == none) {
                break;
            }

            if (cell.dir == diag) {
                for (size_t k = 0; k < aligned.size(); ++k) {
                    new_aligned[k] += aligned[k][rows - row];
                }
                new_line += lines[ln][cols - col];
                --row;
                --col;
            } else if (cell.dir == up) {
                for (size_t k = 0; k < aligned.size(); ++k) {
                    new_aligned[k] += aligned[k][rows - row];
                }
                new_line += this->gap_char;
                --row;
            } else {
                for (size_t k = 0; k < aligned.size(); ++k) {
                    new_aligned[k] += this->gap_char;
                }
                new_line += lines[ln][cols - col];
                --col;
            }
        }
        new_aligned.push_back(new_line);
        aligned = new_aligned;
    }

    return aligned;
}
