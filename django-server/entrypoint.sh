if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Flush db and recreate it (migrate), load start data, 
# and collect static
# python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata fixtures/alpha_data.json
# python manage.py collectstatic --no-input --clear

exec "$@"
