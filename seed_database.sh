rm db.sqlite3 
rm -rf ./AllThingsBourbonAPI/migrations 
python3 manage.py migrate 
python3 manage.py makemigrations AllThingsBourbonAPI 
python3 manage.py migrate AllThingsBourbonAPI 
python3 manage.py loaddata users 
python3 manage.py loaddata bourbon_users
python3 manage.py loaddata bourbon_staff
python3 manage.py loaddata tokens 
python3 manage.py loaddata bourbon_types
python3 manage.py loaddata cocktail_types
python3 manage.py loaddata bourbons
python3 manage.py loaddata cocktails
python3 manage.py loaddata distilleries
python3 manage.py loaddata descriptors
python3 manage.py loaddata bourbons_tried
python3 manage.py loaddata cocktails_tried
python3 manage.py loaddata distilleries_visited