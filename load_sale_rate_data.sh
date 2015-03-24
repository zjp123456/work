echo "hahhahahhah"
echo $1
hive -e "load data local inpath '/home/jipengzeng/desire/liucheng/desire_tid_result.txt' overwrite into table tmp.zjp_desire_twitter_sales_rate partition(dt='$1')";

