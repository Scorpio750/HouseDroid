#!/bin/bash
rm `find . | grep CMakeCache.txt`
rm -rf `find . | grep CMakeFiles`
rm `find . | grep cmake_install.cmake`
rm `find . | grep Makefile`
