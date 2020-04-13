
def error_lot():
    sql = ""
    sql += "SELECT LOT_ID, "
    sql += "    UPLOADFLAG "
    sql += "FROM   (SELECT lot_id, "
    sql += "               cust_device, "
    sql += "               (SELECT data7 "
    sql += "                FROM   wip_sitdef@link_cpkmes1 "
    sql += "                WHERE  data_type = 'CUSDEV INF' "
    sql += "                       AND factory = 'MESPLUS' "
    sql += "                       AND key1 = 'QUL' "
    sql += "                       AND key2 = cust_device) "
    sql += "               Nick, "
    sql += "               sch_type, "
    sql += "               (SELECT Count(*) "
    sql += "                FROM   t_ksy_runlotstrip_cur "
    sql += "                WHERE  a_lot_id = M.lot_id) "
    sql += "               ST_CNT, "
    sql += "               (SELECT Min(assign_time) "
    sql += "                FROM   t_ksy_runlotstrip_cur "
    sql += "                WHERE  a_lot_id = M.lot_id) "
    sql += "               Started, "
    sql += "               (SELECT Max(strip_id) "
    sql += "                FROM   t_ksy_runlotstrip_cur "
    sql += "                WHERE  a_lot_id = M.lot_id) "
    sql += "                      one_sample_strip_id, "
    sql += "               assy_out_time, "
    sql += "               (SELECT DISTINCT 'Y' "
    sql += "                FROM   t_ksy_runlotstrip_cur "
    sql += "                WHERE  a_lot_id = M.lot_id "
    sql += "                       AND rownum = 1) "
    sql += "               PCB2d, "
    sql += "               (SELECT data1 "
    sql += "                       || '-' "
    sql += "                       || Decode(data2, ' ', 'Reserved', "
    sql += "                                        NULL, 'Not Register', "
    sql += "                                        data2) "
    sql += "                       || '-' "
    sql += "                       || data3 "
    sql += "                       || ' : ' "
    sql += "                       || data4 "
    sql += "                       || ' : ' "
    sql += "                       || data5 "
    sql += "                       || ':' "
    sql += "                       || data10 "
    sql += "                FROM   uptdat@link_cpkmes1 "
    sql += "                WHERE  factory = 'ASSEMBLY' "
    sql += "                       AND table_name = 'QUL_GENEALOGY_LOT' "
    sql += "                       AND key1 = M.lot_id) "
    sql += "                      UploadfLAG, "
    sql += "               mpmgr.Ksy_chkpcsd_when_manifest@link_cpkmes1('IS_MANI', lot_id) "
    sql += "               ISMANI, "
    sql += "               mpmgr.Ksy_chkpcsd_when_manifest@link_cpkmes1('IS_GENE', lot_id) "
    sql += "               ISGENE, "
    sql += "               '' "
    sql += "        FROM   wip_lotinf@link_cpkmes1 M "
    sql += "        WHERE  cust_id = 'QUL' "
    sql += "               AND assy_out_time > To_char(sysdate - 6, 'yyyymmddhh24miss') "
    sql += "               AND mpmgr.Ksy_chkpcsd_when_manifest@link_cpkmes1('IS_MANI', "
    sql += "                   lot_id) = "
    sql += "                   'Y' "
    sql += "               AND mpmgr.Ksy_chkpcsd_when_manifest@link_cpkmes1('IS_GENE', "
    sql += "                   lot_id) = "
    sql += "                   'Y' "
    sql += "        ORDER  BY 8) "
    sql += "WHERE  uploadflag LIKE 'E%' "

    return sql



def utp_info(lot):
    sql = " SELECT * "
    sql = "FROM   uptdat@link_cpkmes1 "
    sql = "WHERE  factory = 'ASSEMBLY' "
    sql = "       AND table_name = 'QUL_GENEALOGY_LOT' " 
    sql = "       AND key1 IN( '{0}' )" 

    return sql.format(lot)



import time
from random import randint

def upt(lot):
    sysdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    random_data = str(randint(1, 3))

    sql = "UPDATE UPTDAT@LINK_CPKMES1"
    sql += "	SET DATA1 = ' ',"
    sql += "	    DATA2 = ' ','"
    sql += "	    DATA3 = ' ',"
    sql += "	    DATA5 = 'Resend: {0}',"
    sql += "	    DATA10 = '{1}'"
    sql += "WHERE FACTORY='ASSEMBLY'"
    sql += "	AND TABLE_NAME = 'QUL_GENEALOGY_LOT'"
    sql += "	AND KEY1 IN ('{2}')"

    return sql.format(sysdate, random_data, lot)

def recover(lot):
    sql = ""
    sql += "DECLARE "
    sql += "    p_return_msg VARCHAR2(1000);" 
    sql += "BEGIN "
    sql += "    pkg_ksy_sip_recover.Recover_gene_smt_case1('{0}', p_return_msg); "
    sql += "    COMMIT; "
    sql += "    dbms_output.Put_line(p_return_msg); "
    sql += "END; "

    return sql.format(lot)



def result_check(lot):
    sql = ""
    sql += "SELECT lot_id, "
    sql += "    mpmgr.Ksy_chkpcsd_when_manifest@link_cpkmes1('IS_GENE_OK', lot_id) "
    sql += "FROM   wip_lotinf@link_cpkmes1 "
    sql += "WHERE  lot_id IN ('{0}')"

    return sql.format(lot)



