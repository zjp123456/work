dt=`date -d yesterday +%Y-%m-%d`
hive -e "
set hive.exec.dynamic.partition.mode;
set hive.exec.dynamic.partition.mode=nostrict;
insert overwrite table tmp.zjp_desire_device_table partition(dt)
select device_id,tb2.dt from
(
select ac_tk,dt from
(
select cookie_map['app_access_token'] as ac_tk,dt
from
    wap_nginx_log
where
    dt='$dt'
    and class_name='zulily'
union all
select cookie_map['app_access_token'] as ac_tk,dt
from
    wap_nginx_log_in_app
where
    dt='$dt'
    and class_name='zulily'
) t group by ac_tk,dt
) tb1 join
(
select access_token,device_id,dt from mobile_app_log_new_orc where dt='$dt' group by access_token,device_id,dt
) tb2 on tb1.ac_tk=tb2.access_token and tb1.dt=tb2.dt group by device_id,tb2.dt"
