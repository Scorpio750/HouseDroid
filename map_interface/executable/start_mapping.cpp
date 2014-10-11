#include "Map.hpp"
#include <stdio.h>

using namespace std;

int main(int argc, char *argv[]) {
  Map room(0, 100, 0, 100);
  room.set(150, 150, 196);
  room.set(250, 150, 196);
  room.set(250, 250, 196);
  room.dumpToFolder("testimages");
  return 0;
}
