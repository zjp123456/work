hive -e "
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
insert overwrite table tmp.zjp_desire_visit_user_count partition(dt)
select count(distinct(device_id)) as uv,dt
from tmp.zjp_desire_device_table group by dt;"
