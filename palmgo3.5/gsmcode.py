err_angle_gps_count = 0
gps_angle_sheet_row = 0

for k in range(len(list_gpss)):
    vec_angle = None
    inc_angle = None
    gps = list_gpss[k]

    if k > 0:
        last_gps = list_gpss[k - 1]
        vec_angle = gs.cal_angle(last_gps.gps_long, last_gps.gps_lat, gps.gps_long, gps.gps_lat)
        inc_angle = gs.cal_inc_angle(vec_angle, gps.gps_angle)
    if vec_angle is not None and inc_angle is not None:
        if gps.gps_angle < 0 or gps.gps_angle > 360:
            gps_angle_sheet_row = gps_angle_sheet_row + 1
            gps_angle_sheet.write(gps_angle_sheet_row, 0, 'angle_scope')
            gps_angle_sheet.write(gps_angle_sheet_row, 1, gps.std_time_str)
            gps_angle_sheet.write(gps_angle_sheet_row, 2, gps.utc_time_str)
            gps_angle_sheet.write(gps_angle_sheet_row, 3, '{:.2f}'.format(gps.gps_angle))
            gps_angle_sheet.write(gps_angle_sheet_row, 4, '-')
            gps_angle_sheet.write(gps_angle_sheet_row, 5, '-')

            err_angle_gps_count = err_angle_gps_count + 1

        elif inc_angle > cp.match_angle_threshold / 2.:
            gps_angle_sheet_row = gps_angle_sheet_row + 1
            gps_angle_sheet.write(gps_angle_sheet_row, 0, 'inc_angle')
            gps_angle_sheet.write(gps_angle_sheet_row, 1, gps.std_time_str)
            gps_angle_sheet.write(gps_angle_sheet_row, 2, gps.utc_time_str)
            gps_angle_sheet.write(gps_angle_sheet_row, 3, '{:.2f}'.format(gps.gps_angle))
            gps_angle_sheet.write(gps_angle_sheet_row, 4, '{:.2f}'.format(vec_angle))
            gps_angle_sheet.write(gps_angle_sheet_row, 5, '{:.2f}'.format(inc_angle))

            err_angle_gps_count = err_angle_gps_count + 1