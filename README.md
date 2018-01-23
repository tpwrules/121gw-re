# 121gw-re
Reverse engineering the EEVBlog 121GW

If you're just here to learn about the meter, start with the wiki up top.

* The `pdfs` directory contains official documentation on the multimeter hardware (manuals, datasheets, etc.).
* The `binaries` directory contains the firmware and bootloader release binaries.
* The `database` directory contains the IDA database for the firmware. Please read the [DATABASE readme](database/DATABASE.md) before doing anything with it.

### Routines & Tables
The `routines` directory contains reimplemented routines from the firmware. These can be implemented in any reasonable language that will not require a large amount of external libraries. Preference is given to those which work to teach about the routine. Read and run the `meas_ohms_calc_50M_offset.py` code for a demonstration.

The `tables` directory contains C header definitions for the various firmware tables. When writing such a file, keep in mind the following:
* Use appropriate datatypes, e.g. `const`, `unsigned int`, or `uint16_t`.
* Annotate the different sections of the table with their use.
* IDA is sometimes incorrect about displaying signed numbers; use the correct signed-ness in the definition.
* The table can almost certainly be found in the .c file output by IDA. Just clean up the above issues and it's good to go.

## Contributing
There are several ways to contribute to the project.

* If you have a GitHub account, you can freely edit the wiki. Check the Questions page and see if you can answer one of them.
* If you would like to contribute to the IDA database, please read the instructions in the [DATABASE readme](database/DATABASE.md).
* If you would like to contribute a file, such as a dump for `binaries` or a new example for `routines`, please either open an issue and provide a link to the file, or fork the repository and create a pull request.