# teapot
flask server to run on rpi zero

## dependencies
* flask `$sudo pip install flast`
* gunicorn `$sudo pip install gunicorn`
* supervisor `$sudo install supervisor`

## how to
* install the dependencies
* test the flask and gunicorn with $gunicorn app:app --bind 0.0.0.0
* update the teapot.conf(used for supervisor) file and create mentioned log folder (/var/log/teapot)
* copy the teapot.conf to /etc/supervisor/conf.d/teapot.conf
* reload the supervisor with $sudo supervisorctl reload

## end points
GET /dc?PIN get the current dc for the PIN (PIN should be either 12 or 13)

POST /dc set the dc for the PIN (PIN should be either 12 or 13)
`curl -H "Content-Type: application/json" -X POST -d '{"dc":0,"pin":12,"freq":300}' http://192.168.2.231:5000/dc`

GET /lux returns lux values from wired lux sensor
