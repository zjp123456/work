for((i=1;i<2;i++))
do
#dt=`date -d "$i day ago 2015-03-12" +%Y-%m-%d`
dt=`date -d yesterday +%Y-%m-%d`
hive -e "insert overwrite table tmp.zjp_desire_new_user_retention partition(dt='$dt') 
select a.first_dt,
          count(distinct a.device_id) as newdevice,
          count(distinct case when b.dt=date_add(a.first_dt,1)  then a.device_id end) as onedayreturn,
          count(distinct case when (b.dt<=date_add(a.first_dt,7) and b.dt>a.first_dt) then a.device_id end) as sevendayreturn,
          count(distinct case when (b.dt<=date_add(a.first_dt,30) and b.dt>a.first_dt) then a.device_id end) as thirtydayreturn
from
(
select device_id,min(dt) as first_dt
from
    tmp.zjp_desire_device_table
where
    dt<='$dt'
group by device_id
) a
left outer join
(
select
    device_id,
    dt
from
    tmp.zjp_desire_device_table
where
    dt<='$dt'
) b
on a.device_id=b.device_id
group by a.first_dt order by a.first_dt desc limit 40;"
done
