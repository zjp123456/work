for((i=1;i<2;i++))
do
#dt=`date -d "$i day ago 2015-03-11" +%Y-%m-%d`
#dt1=`date -d "$i day ago 2015-02-09" +%Y-%m-%d`
dt=`date -d yesterday +%Y-%m-%d`
dt1=`date -d "31 day ago $dt" +%Y-%m-%d`
echo $dt
echo $dt1
hive -e "insert overwrite table tmp.zjp_desire_user_active_degree partition(dt='$dt')
select count(distinct a.device_id),
           count(distinct case when b.dt=date_add(a.dt,1) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,2) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,3) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,4) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,5) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,6) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,7) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,15) then b.device_id end),
           count(distinct case when b.dt=date_add(a.dt,30) then b.device_id end),a.dt
from
(
select dt,device_id
from tmp.zjp_desire_device_table  
where dt>='$dt1'  and dt<='$dt' 
group by dt,device_id
) a
left outer join
(
select dt,device_id
from tmp.zjp_desire_device_table  
where dt>='$dt1'  and dt<='$dt'
group by dt,device_id
) b
on a.device_id=b.device_id
group by a.dt limit 40;"
done
