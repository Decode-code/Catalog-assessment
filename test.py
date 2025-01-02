#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cctype>

using namespace std;

bool isNum(const string &s) {
    return !s.empty() && all_of(s.begin(), s.end(), ::isdigit);
}

int strToInt(const string &s) {
    return isNum(s) ? stoi(s) : 0;
}

int decode(int base, const string &val) {
    int res = 0;
    for (char c : val) res = res * base + (c - '0');
    return res;
}

double findConst(const vector<pair<int, int>> &pts) {
    double c = 0.0;
    for (size_t i = 0; i < pts.size(); ++i) {
        double term = pts[i].second;
        for (size_t j = 0; j < pts.size(); ++j) {
            if (i != j) {
                term *= static_cast<double>(-pts[j].first) / (pts[i].first - pts[j].first);
            }
        }
        c += term;
    }
    return c;
}

double calcConstFromFile(const string &fileName) {
    ifstream file(fileName);
    if (!file.is_open()) throw runtime_error("Cannot open file");

    stringstream buf;
    buf << file.rdbuf();
    file.close();

    map<string, pair<int, string>> ptsData;
    int k = 0;

    istringstream input(buf.str());
    string line;
    while (getline(input, line)) {
        line.erase(remove(line.begin(), line.end(), ' '), line.end());
        if (line.empty()) continue;

        if (line.find("\"keys\"") != string::npos) {
            size_t kPos = line.find("\"k\":");
            if (kPos != string::npos) {
                string kStr = line.substr(kPos + 4);
                k = strToInt(kStr.substr(0, kStr.find_first_not_of("0123456789")));
            }
            continue;
        }

        size_t colPos = line.find(":");
        if (colPos != string::npos) {
            string x = line.substr(0, colPos);
            x.erase(remove(x.begin(), x.end(), '"'), x.end());
            x.erase(remove(x.begin(), x.end(), ','), x.end());

            size_t bPos = line.find("\"base\"");
            size_t vPos = line.find("\"value\"");
            if (bPos != string::npos && vPos != string::npos) {
                size_t bStart = line.find("\"", bPos) + 1;
                size_t bEnd = line.find("\"", bStart);
                size_t vStart = line.find("\"", vPos) + 1;
                size_t vEnd = line.find("\"", vStart);

                string base = line.substr(bStart, bEnd - bStart);
                string val = line.substr(vStart, vEnd - vStart);

                ptsData[x] = {strToInt(base), val};
            }
        }
    }

    vector<pair<int, int>> pts;
    for (const auto &item : ptsData) {
        pts.emplace_back(strToInt(item.first), decode(item.second.first, item.second.second));
    }

    if (k <= 0 || pts.size() < static_cast<size_t>(k)) {
        throw invalid_argument("Invalid or insufficient points.");
    }

    return findConst(vector<pair<int, int>>(pts.begin(), pts.begin() + k));
}

int main() {
    string fileName = "input.json";
    try {
        cout << fixed << setprecision(6) << "Constant: " << calcConstFromFile(fileName) << endl;
    } catch (const exception &e) {
        cerr << "Error: " << e.what() << endl;
    }
    return 0;
}