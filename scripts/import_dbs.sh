colls=( users matches stadiums teams )

for c in ${colls[@]}
do
  mongoimport -d adv_db_prj -c 
  mongoimport --db adv_db_prj  --collection $c --file ../queries/$c.json --jsonArray    
done
