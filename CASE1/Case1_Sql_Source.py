# -*- coding:utf-8 -*-

import cx_Oracle       

class Init:
    def Connection(connectionString):
       return cx_Oracle.connect(connectionString["user_ID"],
                                connectionString["user_PW"],
                                connectionString["database_IP"] + ":" + connectionString["database_Port"] + "/" + connectionString["database_Sid"])

class FormatSQL:
    def Query_IsExist_Case1Err():
        sql = ""
        sql += "select LOT_ID, UPLOADFLAG from (select lot_id,cust_device," + "\n"
        sql += "\t(select data7  from wip_sitdef@link_cpkmes1  where data_type = 'CUSDEV INF' and factory='MESPLUS'  and key1='QUL' and key2=cust_device ) Nick," + "\n"
        sql += "\tsch_type," + "\n"
        sql += "\t(select count(*)         from t_ksy_runlotstrip_cur where a_lot_id=M.lot_id ) ST_CNT," + "\n"
        sql += "\t(select min(assign_time) from t_ksy_runlotstrip_cur where a_lot_id=M.lot_id ) Started," + "\n"
        sql += "\t(select max(strip_id)    from t_ksy_runlotstrip_cur where a_lot_id=M.lot_id ) one_sample_strip_id," + "\n"
        sql += "\tassy_out_time," + "\n"
        sql += "\t(select distinct \'Y\'" + "\n"
        sql += "\tfrom t_ksy_runlotstrip_cur" + "\n"
        sql += "where a_lot_id=M.lot_id and rownum=1) PCB2d," + "\n"
        sql += "\t(select DATA1||'-'||decode(data2, ' ', \'Reserved\', null, \'Not Register\' , data2)||\'-\'||DATA3" + "\n"
        sql += "\t\tfrom uptdat@link_cpkmes1 where FACTORY=\'ASSEMBLY\'   AND table_name = \'QUL_GENEALOGY_LOT\'   and KEY1=M.LOT_ID  ) UploadfLAG," + "\n"
        sql += "\t\tMPMGR.KSY_CHKPCSD_WHEN_MANIFEST@LINK_CPKMES1(\'IS_MANI\',LOT_ID) ISMANI," + "\n"
        sql += "\t\tMPMGR.KSY_CHKPCSD_WHEN_MANIFEST@LINK_CPKMES1(\'IS_GENE\',LOT_ID) ISGENE, ''" + "\n"
        sql += "\tfrom wip_lotinf@link_cpkmes1 M" + "\n"
        sql += "\t\twhere cust_id=\'QUL\'" + "\n"
        sql += "\t\tand assy_out_time > to_char(sysdate-30,\'yyyymmddhh24miss\')" + "\n"
        sql += "\t\tand assy_out_time > to_char(sysdate-30,\'yyyymmddhh24miss\')" + "\n"
        sql += "\t\tand MPMGR.KSY_CHKPCSD_WHEN_MANIFEST@LINK_CPKMES1(\'IS_MANI\',LOT_ID) =\'Y\'" + "\n"
        sql += "\t\tand MPMGR.KSY_CHKPCSD_WHEN_MANIFEST@LINK_CPKMES1(\'IS_GENE\',LOT_ID) =\'Y\'" + "\n"
        sql += "\torder by 8) \n\twhere UPLOADFLAG LIKE \'E%\'" + "\n"
        return sql

    def Query_getDataComLocationNull(lotId):
        sql = ""
        sql += "SELECT equip_id," + "\n"
        sql += "\tstrip_id," + "\n"
        sql += "\tcom_location," + "\n"
        sql += "\tTO_CHAR(created_time, 'YYYY-MM-DD HH24:MI:SS') AS CRATED_TIME" + "\n"
        sql += "FROM   ccm.t_sip_ccm_d_sg" + "\n"
        sql += "WHERE  strip_id IN (SELECT strip_id" + "\n"
        sql += "\t\tFROM   t_ksy_runlotstrip_cur " + "\n"
        sql += "\t\tWHERE  a_lot_id = '" + lotId + "')" + "\n"
        sql += "\tAND com_part IS NULL" + "\n"
        sql += "\tAND rownum < 5" + "\n"
        return sql
        
        

    def Procedure_PKG_KSY_SIP_RECOVER_RECOVER_GENE_SMT_CASE1(lotid_list):
        sql = ""
        sql += "DECLARE " + "\n"
        sql += "\tP_RETURN_MSG VARCHAR2(1000);" + "\n"
        sql += "BEGIN" + "\n"
        for i in lotid_list: sql += "\tPKG_KSY_SIP_RECOVER.RECOVER_GENE_SMT_CASE1(\'" + i + "\',P_RETURN_MSG);" + "\n"
        sql += "END ;"
        sql += '\n'
        return sql

    def Query_DataIsOkay(lotid_list):
        sql = ""
        sql += "SELECT LOT_ID, MPMGR.KSY_CHKPCSD_WHEN_MANIFEST@LINK_CPKMES1('IS_GENE_OK',LOT_ID) " + "\n"
        sql += "FROM WIP_LOTINF@LINK_CPKMES1" + "\n"
        sql += "\tWHERE LOT_ID IN ("
        for i in range(len(lotid_list)):
            sql += '\''
            sql += lotid_list[i]
            sql +='\''
            if(len(lotid_list) - 1 != i): sql += ','
        sql += ')'
        sql += '\n'
        return sql

    def Query_UpdateUTP(lotid):
        import time
        from random import randint
        
        sql = ""
        sql += "UPDATE UPTDAT@LINK_CPKMES1" + '\n'
        sql += "\tSET DATA1 = \' \'," + '\n'
        sql += "\t    DATA2 = \' \'," + '\n'
        sql += "\t    DATA3 = \' \'," + '\n'
        sql += "\t    DATA5 = \'Resend:" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + "\'" + "," + "\n"
        sql += "\t    DATA10 = "  + '\'' + str(randint(1, 3)) + '\'' + "\n" 
        sql += "WHERE FACTORY=\'ASSEMBLY\'" + "\n"
        sql += "\tAND TABLE_NAME = \'QUL_GENEALOGY_LOT\'" + "\n"
        sql += "\tAND KEY1 IN (\'" + lotid + '\');'
        sql += '\n'
        return sql

    def Query_UpdateUTP_DataCheck(lotid):
        sql = ""
        sql += "SELECT * FROM UPTDAT@LINK_CPKMES1 " 
        sql += "WHERE FACTORY=\'ASSEMBLY\' " 
        sql += "AND TABLE_NAME = \'QUL_GENEALOGY_LOT\' "
        sql += "AND KEY1 IN(\'" + lotid + "\');"
        return sql

    

class SqlGet:
    def Data_Case1Err_LotID(connection):
        
        cursor = connection.cursor()
        cursor.execute(FormatSQL.Query_IsExist_Case1Err())
    
        lotid_list = []
        for data in cursor: lotid_list.append([data[0],data[1]])
        return lotid_list
  

   
   
   
