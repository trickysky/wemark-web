zip -r $1 * -x .git .gitignore .idea *.sh *.yml vendor/* config/lottery_settings.json tests/* env
scp $1 $3@$2:$1
rm $1
