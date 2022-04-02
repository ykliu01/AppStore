# Construct the URI from the .env
DB_HOST=ec2-3-225-79-57.compute-1.amazonaws.com
DB_NAME=dcht2af34pga9a
DB_USER=ekbqbfqluaebne
DB_PORT=5432
DB_PASSWORD=a428a072a879f5441fc2c90098fd292b91ee775709bb4a0fe025a4eac23cd1ab

while IFS= read -r line
do
  if [[ $line == DB_HOST* ]]
  then
    DB_HOST=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_NAME* ]]
  then
    DB_NAME=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_USER* ]]
  then
    DB_USER=$(cut -d "=" -f2- <<< $line | tr -d \' )
  elif [[ $line == DB_PORT* ]]
  then
    DB_PORT=$(cut -d "=" -f2- <<< $line | tr -d \')
  elif [[ $line == DB_PASSWORD* ]]
  then
    DB_PASSWORD=$(cut -d "=" -f2- <<< $line | tr -d \')
  fi
done < ".env"

URI="postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

# Run the scripts to insert data.
psql ${URI} -f sql/AppStoreClean.sql
psql ${URI} -f sql/AppStoreSchema.sql
psql ${URI} -f sql/MRT.sql
psql ${URI} -f sql/students.sql
psql ${URI} -f sql/calculators.sql
psql ${URI} -f sql/loan.sql
psql ${URI} -f sql/AppStoreTestStudents.sql
