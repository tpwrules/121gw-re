This directory contains the multimeter firmware as an IDA 6.6 database. For the benefit of those who do not have access to the correct version of IDA, the database has been exported as both a C and assembly listing. The memory map, enumeration, and structure definitions are present as well.

## Contributing to the Database
If you would like to contribute to the database, please open an issue and describe the contribution you wish to make. This simplifies merging databases and dealing with disparate IDA versions. Appropriate contributions include naming variables and functions, specifying types, and supplying information to help understand a particular routine (naming local variables, annotating `if` statements, etc.). Any other information, such as behaivor of a routine, system architecture, and so on, belongs on the wiki.

# Information

### Conventions

* Functions and variables that aren't totally understood are named as such, using words like `maybe` or `probably`.
* Functions that are completely understood are marked green (right click and select Mark as decompiled). However, there are quite a lot of functions that are understood but not marked as such, so don't rely on that particular metadata.
* Globals that are only used for one function are prefixed with that function's name or abbreviation of such.

### IDA Issues

* IDA is unfortunately somewhat poor at decompiling control flow. This leaves a lot of messy nested `if` statements with `goto`s everywhere. Occasionally, I have added comments to explain the comparison operations being performed. This work needs to be expanded on.
* IDA does mess up decompilation, producing a completely wrong function. If you come across this, be sure to comment this!

### Notes

* The STM32 HAL library uses a large number of functions and structures to control the hardware. This hasn't really been investigated, except to the extent necessary to determine other behavior. If you find functions that are lots of pointer math (`*(a1 + 4) = 5`) or only twiddle hardware registers (around 0x40000000), they are almost certainly part of the HAL.
* There shouldn't really be any large mysteries in or modifications to make to the database. Most of the work will be in reading the code and documenting its behavior on the wiki.