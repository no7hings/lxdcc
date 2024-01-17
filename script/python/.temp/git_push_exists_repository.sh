git config --global user.name "dongchangbao"
git config --global user.email "dongchangbao@papegames.net"

cd /data/f/myworkspace/lxdcc

git remote rename origin old-origin
git remote add origin https://gitlab.nikkigames.cn/papepipe/lxdcc.git
git push -f -u origin --all
git push -f -u origin --tags

