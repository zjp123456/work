#coding=utf-8
import sys
import os
from common.statutil import  get_stat_db,get_config_db
from datetime import datetime, timedelta,date
from common.hivehelper import hivehelper
import pickle as pk
reload(sys)
sys.setdefaultencoding("utf-8")
hp = hivehelper()
statdb = get_stat_db()
statdb.autocommit(True)


def insert_pay_time_info(theday):
    pre_date=theday-timedelta(days =1) 
    hql = "insert overwrite table tmp.zjp_desire_pay_info partition (dt='%s') select twitter_id,pay_time,purchase_num from(select twitter_id from ods_cheetah_style where twitter_id!=0) a left outer join(select twitter_id as tid,unix_timestamp(pay_time) as pay_time,sum(if(to_date(pay_time)='%s',purchase_num,0)) as purchase_num from dm.dm_order_4analyst where (order_create_dt='%s' or order_create_dt='%s') and to_date(pay_time)!='1970-01-01' group by twitter_id,unix_timestamp(pay_time)) b on a.twitter_id=b.tid"% (theday,theday,theday,pre_date)
    print hql
    result = hp.hive_execute_all(hql)

def get_pay_info_data(theday):
    cursor=statdb.cursor()
    hql="select twitter_id,pay_time,purchase_num from tmp.zjp_desire_pay_info where dt='%s'" % (theday)
    print hql
    times_result={}
    max_sell_amount=0
    result=hp.hive_execute_all(hql)
    final_max_purchase_num={}
    for r in result:
        if r[0] in times_result:
            tmp_dict=times_result[r[0]]
            tmp_dict[r[1]]=r[2]
            times_result[r[0]]=tmp_dict
        else:
            tmp_dict={}
	    tmp_dict[r[1]]=r[2]
            times_result[r[0]]=tmp_dict
    for (k,v) in times_result.items():
	start_time=0
        max_purchase_num=0
        tmp=sorted(v.iteritems(),key=lambda d:d[0])
        print "dict[%s] =" % k,tmp
        for i in tmp:
            if i[0]=='None':
                continue
            purchase_num=int(i[1])
            for j in tmp:
                if int(j[0])-int(i[0])>0 and int(j[0])-int(i[0])<=3600:
                    purchase_num=purchase_num+int(j[1])
            if purchase_num > max_purchase_num:
                max_purchase_num=purchase_num
        final_max_purchase_num[k]=max_purchase_num
    print final_max_purchase_num
    write_result_to_file(final_max_purchase_num,theday)

def write_result_to_file(result,theday):
    file_name="desire_tid_result.txt"
    file_object=open(file_name,'w')
    for (k,v) in result.items():
        line=str(k)+'\t'+str(v)+'\n'
        file_object.write(line)   
    file_object.close()
    cmd='./load_sale_rate_data.sh '+str(theday)
    print cmd
    os.system(cmd)
def get_opts():
    if len(sys.argv) < 2:
        fromdate = date.today() - timedelta(days = 1)
    if len(sys.argv) == 2:
        fromdate = (datetime.strptime(sys.argv[1], '%Y-%m-%d')).date()
    if len(sys.argv) > 2:
        fromdate = (datetime.strptime(sys.argv[1], '%Y-%m-%d')).date()
        days = int(sys.argv[2])
    else:
        days = 1
    todate = fromdate + timedelta(days=days-1)
    return fromdate, todate


def main():
    fromdate, todate = get_opts()
    while fromdate <= todate:
        insert_pay_time_info(fromdate)
        get_pay_info_data(fromdate)
        fromdate += timedelta(days=1)

if __name__=='__main__':
    main()
