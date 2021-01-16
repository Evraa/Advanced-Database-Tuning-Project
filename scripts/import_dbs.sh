colls=( users matches stadiums teams )

for c in ${colls[@]}
do
  mongoimport -d adv_db_prj_2 -c 
  mongoimport --db adv_db_prj_2  --collection $c --file ../queries/$c.json --jsonArray    
done
