# Run to make executable: chmod +x script.sh

deployweb(){
	DRY=""
    if [ "$1" = "--dry" ]; then
        DRY="n"   # rsync uses `-n` for dry run
    fi
	echo "DRY DEPLOY"
	rsync -avz${DRY} --delete --exclude '__pycache__/' --exclude 'migrations/' website/ porchfest:/home/django/porchfest/website/	
}

deploycore(){
	DRY=""
    if [ "$1" = "--dry" ]; then
        DRY="n"   # rsync uses `-n` for dry run
    fi
	echo "DRY DEPLOY"
	rsync -avz${DRY} --delete --exclude '__pycache__/' --exclude 'migrations/' porchfestcore/ porchfest:/home/django/porchfest/porchfestcore/	
}


if [ "$1" == "deployweb" ]; then
	shift
	deployweb "$@"
elif [ "$1" == "deploycore" ]; then
	shift
	deploycore "$@"
else
	echo "$1"
	echo "Usage: $0 {deploy db | deploy theme | deploy content}"
fi