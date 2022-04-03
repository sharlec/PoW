. start.sh

fuser -k 5000/tcp
export FLASK_ENV=development
flask run