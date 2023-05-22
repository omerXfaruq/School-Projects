CXX = mpicxx
CXXFLAGS = -O2 -fopenmp -std=c++11
TARGETS = seq apsp

.PHONY: all
all: $(TARGETS)

.PHONY: clean
clean:
	rm -f $(TARGETS) $(TARGETS:=.o)
