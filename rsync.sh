# Run to make executable: chmod +x script.sh

rebuild_server(){
	ssh porchfest << "EOF"
	cd /home/django/porchfest
	source venv/bin/activate
	python manage.py collectstatic --noinput
	systemctl restart gunicorn
	systemctl reload nginx
EOF
}

deployweb(){
	DRY=""
    if [ "$1" = "--dry" ]; then
        DRY="n"
		echo "DRY DEPLOY"
    fi
	rsync -avz${DRY} --delete --exclude '__pycache__/' --exclude 'migrations/' website/ porchfest:/home/django/porchfest/website/
}

deploycore(){
	DRY=""
    if [ "$1" = "--dry" ]; then
        DRY="n"
		echo "DRY DEPLOY"
    fi
	rsync -avz${DRY} --delete --exclude '__pycache__/' --exclude 'migrations/' porchfestcore/ porchfest:/home/django/porchfest/porchfestcore/
}

deployapp(){
	DRY=""
	if [ "$1" = "--dry" ]; then
		DRY="n"
		echo "DRY DEPLOY"
	fi
	rsync -avz${DRY} --delete --exclude '__pycache__/' --exclude 'migrations/' porchfest/ porchfest:/home/django/porchfest/porchfest/
}


if [ "$1" == "deployweb" ]; then
	shift
	deployweb "$@"
elif [ "$1" == "deploycore" ]; then
	shift
	deploycore "$@"
elif [ "$1" == "deployapp" ]; then
	shift
	deployapp "$@"
elif [ "$1" == "rebuildserver" ]; then
	rebuild_server
else
	echo "$1"
	echo "Usage: $0 {deploy db | deploy theme | deploy content}"
fi