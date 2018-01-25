// this file contains the tables used by the
// meas_calc_ac_freq_dependent_offset_core
// and meas_calc_ac_freq_dependent_offset_core_for_ACV_5_50V routines

// input lookup tables, in Hz
// 10KHz used for modes ACV at ranges 500V and 600V, plus ACuA/mA/A all ranges
int mcafdoc_infreq_tbl_10khz[7] = { 50, 400, 1000, 3000, 5000, 7000, 10000 };
// 100KHz used for all ACmV ranges
int mcafdoc_infreq_tbl_100khz[9] = { 50, 400, 1000, 10000, 30000, 50000, 70000, 90000, 100000 };

// correction tables for the above modes and ranges
// first row is used if input <= 5000 counts, second used otherwise
int mcafdoc_corr_tbl_acmv50[2][9] = {
    { 0,  3,  0, -2,  1, 18, 47, 81, 100 },
    { 0, -5, -1,  7, 40, 70, 90, 98, 100 }
};

int mcafdoc_corr_tbl_acmv500[2][9] = {
    { 0,  1, -1, -2, -1, 15, 45, 82, 100 },
    { 0, -2, -1,  3, 19, 40, 65, 88, 100 }
};

int mcafdoc_corr_tbl_acv500[2][7] = {
    { 0, 2, 22, 78, 98, 99, 100 },
    { 0, 2, 22, 77, 96, 99, 100 }
};

int mcafdoc_corr_tbl_acv600[2][7] = {
    { 0, 2, 22, 85, 95, 99, 100 },
    { 0, 2, 22, 77, 95, 99, 100 } // second row effectively unused
};

int mcafdoc_corr_tbl_acuA[2][7] = {
  { 0, -10,  3, 20, 35, 55, 100 },
  { 0, -20, -8,  2, 16, 43, 100 }
};

int mcafdoc_corr_tbl_acmA[2][7] = {
  { 0, -10,  3, 20, 40, 55, 100 },
  { 0, -15, -4,  7, 20, 47, 100 }
};
