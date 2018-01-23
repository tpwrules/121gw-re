// this file contains the table cal_ohms_50M_factor_tbl, used by
// meas_ohms_calc_50M_offset()

const int cal_ohms_50M_factor_tbl[26] = {
    // input map
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60,
    // output map
    0, 37, 65, 85, 100, 100, 100, 87, 70, 40, 0, -37, -65
};
