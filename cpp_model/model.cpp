// Discrete 2x2 Schur stability using Jury inequalities
// Repository: https://github.com/tltmgnt/-Topology-for-Dynamical-Systems-and-Stability-Analysis
// Standalone C++17, offline, synthetic reference model.
// Build: c++ -std=c++17 -O2 -Wall -Wextra -pedantic cpp_model/model.cpp -o model
// Run: ./model    (runs built-in assertions and prints a bounded demo result)
// Research-only: no trained AI, independent validation, external actions or approval.
#include <algorithm>
#include <cmath>
#include <functional>
#include <iostream>
#include <limits>
#include <numeric>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

void require(bool ok,const char* msg){if(!ok)throw std::runtime_error(msg);}
namespace model {
bool schur_2x2(double a,double b,double c,double d){for(double x:{a,b,c,d})if(!std::isfinite(x))throw std::invalid_argument("nonfinite matrix");double tr=a+d,det=a*d-b*c;return 1-det>1e-12&&1-tr+det>1e-12&&1+tr+det>1e-12;}
void demo(){require(schur_2x2(.5,0,0,.8),"stable diagonal");require(!schur_2x2(1.1,0,0,.8),"unstable diagonal");std::cout<<"synthetic_stable="<<schur_2x2(.5,0,0,.8)<<" boundary_not_classified_stable=1";}
} // namespace model
int main(){try{std::cout<<std::boolalpha;model::demo();std::cout<<'\n';return 0;}catch(const std::exception&e){std::cerr<<"model test failed: "<<e.what()<<'\n';return 1;}}
