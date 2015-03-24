#coding=utf-8
'''
无线用户体验数据
2013-07-12
xinsui@meilishuo.com
'''
import sys
from common.statutil import  get_stat_db,get_config_db
from datetime import datetime, timedelta,date
from common.hivehelper import hivehelper
import pickle as pk
reload(sys)
sys.setdefaultencoding("utf-8")
hp = hivehelper()
statdb = get_stat_db()
statdb.autocommit(True)

shown_map = {
    '#':'#',
    '1#':'daily#',
    '2#':'clothes#',
    '3#':'cosmetic#',
    '1#0':'daily#',
    '1#1':'daily#',
    '1#2':'daily#',
    '1#3':'daily#',
    '2#1':'clothes#1',
    '2#2':'clothes#2',
    '2#3':'clothes#3',
    '2#4':'clothes#4',
    '2#5':'clothes#5',
    '3#1':'cosmetic#1',
    '3#2':'cosmetic#2',
    '3#3':'cosmetic#3',
    'total':'total'
}

pv_uv_map = {
    '#':'#',
    '1#':'daily#',
    '2#':'clothes#',
    '3#':'cosmetic#',
    '1#0':'daily#',
    '1#1':'daily#',
    '1#2':'daily#',
    '1#3':'daily#',
    '2#1':'clothes#1',
    '2#2':'clothes#2',
    '2#3':'clothes#3',
    '2#4':'clothes#4',
    '2#5':'clothes#5',
    '3#1':'cosmetic#1',
    '3#2':'cosmetic#2',
    '3#3':'cosmetic#3',
    'total':'total'
}
page_type_map = {
    '#':'概览',
    '1#':'特惠整体',
    '2#':'美衣整体',
    '3#':'美妆整体',
    '1#0':'特惠落地',
    '1#1':'特惠热销',
    '1#2':'特惠秒杀',
    '1#3':'特惠团购',
    '2#1':'美衣热销',
    '2#2':'美衣超值',
    '2#3':'美衣人气',
    '2#4':'美衣萌萌哒',
    '2#5':'美衣酷酷滴',
    '3#1':'美妆热销',
    '3#2':'美妆口碑',
    '3#3':'美妆超值',
    'total':'整体'
}

table_type_map = {
    '#':'0',
    '1#':'1',
    '2#':'1',
    '3#':'1',
    '1#0':'2',
    '1#1':'2',
    '1#2':'2',
    '1#3':'2',
    '2#1':'2',
    '2#2':'2',
    '2#3':'2',
    '2#4':'2',
    '2#5':'2',
    '3#1':'2',
    '3#2':'2',
    '3#3':'2',
    'total':'0'
}

def print_log(log):
    print log
    sys.stdout.flush()

def insert_shouq_order_info(theday):

    hql = ''' insert overwrite table shouq_order_info partition (dt='%s') select a.order_id,a.pid,split(a.pid,'\\\\.')[1],split(a.pid,'\\\\.')[2],split(a.pid,'\\\\.')[3],a.twitter_id,a.goods_id,a.price,a.amount,a.buyer_uid,to_date(from_unixtime(b.pay_time)),to_date(from_unixtime(b.ctime)),a.price*a.amount,b.source from ods_bat_goods_map a join ods_bat_order b on a.order_id=b.order_id where b.source like '9%%' ''' % (theday)
    print hql
    result = hp.hive_execute_all(hql)


def get_normal_data(theday):
    inster_sql = '''replace into t_dolphin_stat_shouq_info(dt,ftable,type,pv,uv,orderconfirm_pv,orderconfirm_uv,order_num,order_uid,pay_num,pay_uid,gmv,shown_pv,shown_uv,st_pv,st_uv,amount,totalprice) values %s'''
    value_parm = '''('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''
    cursor = statdb.cursor()
    
    #pv uv
    hql = ''' select method_name,cate_id,GROUPING__ID,count(1),count(distinct sessid) from (select if(method_name='main','daily',method_name) as method_name,if(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') is null,1,parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id')) as cate_id,sessid,user_id,visit_ip from msq_nginx_log where dt='%s' and concat(class_name,'#',method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic') union all select parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','page_name') as method_name,parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') as cate_id,sessid,user_id,visit_ip from msq_nginx_log where dt='%s' and concat(class_name,'#',method_name)='sq#normal_goods'  and parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','page_name') is not null and parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') is not null ) tmp group by method_name,cate_id with cube  ''' % (theday,theday)
    print hql
    pv_result={}
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        key_mark=str(r[0])+"#"+str(r[1])
        tmp['pv'],tmp['uv']=r[3:]
        pv_result[key_mark]=tmp
    
    #pv uv 总体
    hql = ''' select count(1),count(distinct sessid) from msq_nginx_log where dt='%s' and concat(class_name,'#',method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic','sq#normal_goods','sq#detail', 'sq#orderconfirm', 'sq#ordercreate', 'sq#orderDetail', 'user#coupon', 'user#order_list', 'sq#user', 'sq#tuan', 'sq#expressInfo', 'sq#cart', 'sq#qq_first' ) ''' % (theday)
    print hql
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        tmp['pv'],tmp['uv']=r[0:]
        pv_result['total']=tmp

    #单宝pv，uv
    hql = ''' select case when refer_method_name='' and split(query_params['d_r'], '-')[1]=1 then 'daily' when refer_method_name='' and split(query_params['d_r'], '-')[1]=2 then 'clothes' when refer_method_name='' and split(query_params['d_r'], '-')[1]=3 then 'cosmetic' when refer_method_name='main' then 'daily' else null end,if(parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id') is null,1,parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id')),GROUPING__ID,count(1),count(distinct visit_ip) from msq_nginx_log where dt='%s' and class_name='sq' and method_name='detail' and ( concat(refer_class_name,'#',refer_method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic') or query_params['d_r'] is not null ) group by case when refer_method_name='' and split(query_params['d_r'], '-')[1]=1 then 'daily' when refer_method_name='' and split(query_params['d_r'], '-')[1]=2 then 'clothes' when refer_method_name='' and split(query_params['d_r'], '-')[1]=3 then 'cosmetic' when refer_method_name='main' then 'daily' else null end,if(parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id') is null,1,parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id')) with cube''' % (theday)
    #hql = ''' select if(refer_method_name='main','daily',refer_method_name),if(parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id') is null,1,parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id')),GROUPING__ID,count(1),count(distinct visit_ip) from msq_nginx_log where dt='%s' and class_name='sq' and method_name='detail' and concat(refer_class_name,'#',refer_method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic') group by if(refer_method_name='main','daily',refer_method_name),if(parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id') is null,1,parse_url(concat('http://sense.meilishuo.com',refer),'QUERY','cate_id')) with cube  ''' % (theday)
    print hql
    st_pv_result={}
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        key_mark=str(r[0])+"#"+str(r[1])
        tmp['pv'],tmp['uv']=r[3:]
        st_pv_result[key_mark]=tmp

    #单宝总体pv，uv
    hql = ''' select count(1),count(distinct sessid) from msq_nginx_log where dt='%s' and concat(class_name,'#',method_name) in ('sq#detail') ''' % (theday)
    print hql
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        tmp['pv'],tmp['uv']=r[0:]
        st_pv_result['total']=tmp
    
    #下单数据
    #hql = ''' select fenye_id,place_id,GROUPING__ID,count(distinct if(ctime='%s',order_id,NULL)),count(distinct if(ctime='%s',buyer_uid,NULL)),count(distinct if(pay_time='%s',order_id,NULL)),count(distinct if(pay_time='%s',buyer_uid,NULL)),sum(if(pay_time='%s',total_price,0)),sum(if(pay_time='%s',amount,0)),sum(if(ctime='%s',total_price,0)) from shouq_order_info where dt='%s' and fenye_id!='' and place_id!='' group by fenye_id,place_id with cube ''' % (theday,theday,theday,theday,theday,theday,theday,theday)
    hql = '''select * from(select fenye_id,place_id,GROUPING__ID as gid,count(distinct if(ctime='%s',order_id,NULL)),count(distinct if(ctime='%s',buyer_uid,NULL)),count(distinct if(pay_time='%s',order_id,NULL)),count(distinct if(pay_time='%s',buyer_uid,NULL)),sum(if(pay_time='%s',total_price,0)),sum(if(pay_time='%s',amount,0)),sum(if(ctime='%s',total_price,0)) from shouq_order_info where dt='%s' group by fenye_id,place_id with cube) t where fenye_id in('1','2','3')  ''' % (theday,theday,theday,theday,theday,theday,theday,theday)
    #hql = '''select * from shouq_order_info where dt='2015-02-27' '''
    print hql
    order_result = {}
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        key_mark=str(r[0])+"#"+str(r[1])
        if key_mark == '#' and r[2] != '0':#不是汇总记录
            continue
        if r[1]=='' and r[2]=='3':
            continue
        tmp['order_num'],tmp['order_uid'],tmp['pay_num'],tmp['pay_uid'],tmp['gmv'],tmp['amount'],tmp['totalprice'] = r[3:]
        order_result[key_mark]=tmp
    order_result['total'] = order_result['#']

    #order_corfirm数据
    hql = '''select split(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','goods_pid'),'\\\\.')[2],split(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','goods_pid'),'\\\\.')[3],GROUPING__ID,count(1),count(distinct visit_ip) from msq_nginx_log where dt='%s' and class_name='sq' and method_name='orderconfirm'  group by split(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','goods_pid'),'\\\\.')[2],split(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','goods_pid'),'\\\\.')[3] with cube   ''' % (theday)
    print hql
    order_corfirm_result={}
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        key_mark=str(r[0])+"#"+str(r[1])
        tmp['pv'],tmp['uv']=r[3:]
        order_corfirm_result[key_mark]=tmp
    order_corfirm_result['total'] = order_corfirm_result['#']

    #shown数据
    hql = ''' select t1.page_name,t1.cate_id,GROUPING__ID,sum(count_num),count(distinct twitter_id) from (select parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','page_name') as page_name,parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') as cate_id,twitter_id, count(*) count_num from shouq_show_log LATERAL VIEW  explode(map_keys(twitter_list_info))  twitter_ids as twitter_id where dt='%s' and class_name='sq' and method_name='normal_goods' and parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','page_name') is not null and parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') is not null group by parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','page_name'),parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id'),twitter_id union all select if(method_name='main','daily',method_name) as page_name,if(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') is null ,1,parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') ) as cate_id,twitter_id, count(*) count_num from shouq_show_log LATERAL VIEW  explode(map_keys(twitter_list_info))  twitter_ids as twitter_id where dt='%s' and concat(class_name,'#',method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic') group by if(method_name='main','daily',method_name),if(parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') is null ,1,parse_url(concat('http://sense.meilishuo.com',uri),'QUERY','cate_id') ) ,twitter_id) t1 group by t1.page_name,t1.cate_id with cube ''' % (theday,theday)
    print hql
    shown_result = {}
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        key_mark=str(r[0])+"#"+str(r[1])
        tmp['pv'],tmp['uv']=r[3:]
        shown_result[key_mark]=tmp

    #总体展现量
    #hql = '''select sum(count_num),count(distinct twitter_id) from (select twitter_id, count(*) count_num from shouq_show_log LATERAL VIEW  explode(map_keys(twitter_list_info))  twitter_ids as twitter_id where dt='%s' and concat(class_name,'#',method_name) in ('sq#main','mall#clothes','mall#daily','mall#cosmetic','sq#normal_goods') group by twitter_id ) t1''' % (theday)
    hql = '''select sum(count_num),count(distinct twitter_id) from (select twitter_id, count(*) count_num from shouq_show_log LATERAL VIEW  explode(map_keys(twitter_list_info))  twitter_ids as twitter_id where dt='%s' and twitter_id>0 group by twitter_id ) t1''' % (theday)
    print hql
    result = hp.hive_execute_all(hql)
    for r in result:
        tmp={}
        tmp['pv'],tmp['uv']=r[0:]
        shown_result['total']=tmp

    print pv_result
    print order_result
    print order_corfirm_result
    print shown_result

    for item in page_type_map:
        sku = value_parm % (theday,page_type_map[item],table_type_map[item],pv_result.get(pv_uv_map.get(item,'no_key'),{}).get('pv',0),pv_result.get(pv_uv_map.get(item,'no_key'),{}).get('uv',0),order_corfirm_result.get(item,{}).get('pv',0),order_corfirm_result.get(item,{}).get('uv',0),order_result.get(item,{}).get('order_num',0),order_result.get(item,{}).get('order_uid',0),order_result.get(item,{}).get('pay_num',0),order_result.get(item,{}).get('pay_uid',0),order_result.get(item,{}).get('gmv',0),shown_result.get(shown_map.get(item,'no_key'),{}).get('pv',0),shown_result.get(shown_map.get(item,'no_key'),{}).get('uv',0),st_pv_result.get(pv_uv_map.get(item,'no_key'),{}).get('pv',0),st_pv_result.get(pv_uv_map.get(item,'no_key'),{}).get('uv',0),order_result.get(item,{}).get('amount',0),order_result.get(item,{}).get('totalprice',0))
        try:
            print inster_sql % sku
            cursor.execute(inster_sql % sku)
        except Exception, e:
            print inster_sql % sku
    cursor.close()

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
    print_log('job set up from %s to %s' % (fromdate, todate))

    while fromdate <= todate:
        print_log('start job for %s' % fromdate)
        insert_shouq_order_info(fromdate)
        get_normal_data(fromdate)
        fromdate += timedelta(days=1)
    print_log('all job is done from %s to %s' %(fromdate,todate))

if __name__=='__main__':
    main()
