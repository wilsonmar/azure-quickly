# aliases.sh in https://github.com/wilsonmar/git-utilities
# NOTE: Functions are in functions.sh for Mac only.
# Both called from ~/.bash_profile for Bash or ~/.zshrc for zsh
# on both MacOS and git bash on Windows.

EDITOR="code"  # code = Visual Studio Code; subl = Sublime Text
alias edit="code"   # change this, not your habitual editor name
alias ebp="$EDITOR ~/.bash_profile && source ~/.bash_profile"
alias sbp='source ~/.bash_profile'
alias rs='exec -l $SHELL'

alias ..='cd ..'
alias c="clear"  # screen
alias h='history'
alias x='exit'
alias p="pwd"   # present working directory

alias kp="ps auxwww"  # the "kp" alias ("que pasa")
alias j='jobs -l'

alias now='date +"%Y-%m-%d %T +%s"'

# Only on MacOS, not git bash on Windows MINGW64:
#if [ "$(uname)" == "Darwin" ]; then  # it's on a Mac:
#   alias vers="sw_vers"
#   function gd() { # get dirty
#	[[ $(git status 2> /dev/null | tail -n1) != *"working directory clean"* ]] && echo "*"
#   }
#  function gas() { git status ;  git add . -A ; git commit -m "$1" ; git push; }
#   function gsa() { git stash save "$1" -a; git stash list; }  # -a = all (untracked, ignored)
#fi

alias cf="find . -print | wc -l"  # count files in folder.
alias lf="ls -p"      # list folders only
alias dir='ls -alrT'  # for windows habits
alias l='ls -FalhGT'  # T for year
alias ll='ls -FalhGT'  # T for year
alias lt="ls -ltaT"   # list by date
# Last 30 files updated anywhere:
alias f50='stat -f "%m%t%Sm %N" /tmp/* | sort -rn | head -50 | cut -f2- 2>/dev/null'

#     catn filename to show text file without comment (#) lines:
alias catn="grep -Ev '''^(#|$)'''"

# wireless en0, wired en1: PRIVATE_IP address:
alias en0="ipconfig getifaddr en0"  # like 172.20.1.91 or 192.168.1.253
   #alias myip="ifconfig en0 | grep inet | grep -v inet6 | cut -d ' ' -f2" 
   # ip route get 1 | awk '{print $NF;exit}'

# These all return the public ip like https://www.whatismyip.com/:
alias pubip="curl -s ifconfig.me"  # public IP
alias ipinfo="curl ipinfo.io"  # returns JSON containing country and zip of IP
#alias pubip="curl https://checkip.amazonaws.com"  # public IP
#alias mac="curl http://canhazip.com"  # public IP 

alias aam='open -a "/Applications/Utilities/Activity Monitor.app"'  # See CPU usage by app
alias ramfree="top -l 1 -s 0 | grep PhysMem"  # PhysMem: 30G used (3693M wired), 1993M unused.
alias spacefree="du -h | awk 'END{print $1}'"
alias wanip4='dig @resolver1.opendns.com ANY myip.opendns.com +short'
alias wanip6='dig @resolver1.opendns.com AAAA myip.opendns.com +short -6'

alias ga='git add . -A'  # --patch
alias gb='git branch -avv'
alias gbs='git status -s -b;git add . -A;git commit --quiet -m"Update";git push'
alias get='git fetch;' # git pull + merge
alias gf='git fetch origin master;git diff master..origin/master'
alias gfu='git fetch upstream;git diff HEAD @{u} --name-only'
alias gc='git commit -m --quiet' # requires you to type a commit message
alias gcm='git checkout master'
alias gl='git log --pretty=format:"%h %s %ad" --graph --since=1.days --date=relative;git log --show-signature -n 1'
alias gl1="git log --graph --all --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr)%Creset' --abbrev-commit --date=relative"
alias gl2="git log --graph --all --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"
alias gmo='git merge origin/master'
alias gmf='git merge --no-ff'
alias gp='git push'
alias gpom='git push -u origin master'
alias grm='git rm $(git ls-files --deleted)'
alias gri='git rebase -i'
alias grl='git reflog -n 7'
alias grh='git reset --hard'
alias grl='git reflog -n 7'
alias grv='git remote -v'
alias gsl='git config user.email;git status -s -b; git stash list'
alias gss='git stash show'
alias hb="hub browse"
alias grx="rm .git/merge"  # Remove merge
alias gsk="gpg --list-secret-keys --keyid-format LONG"
alias gst="gpg show-ref --tags"
# alias githead='?'

alias ven="virtualenv venv"
alias vbc="source venv/bin/activate"
alias vde="deactivate"

alias tf="terraform $1"  # provide a parameter
alias tfa="terraform apply"
alias tfd="terraform destroy"
alias tfs="terraform show"

alias ddk="killall com.docker.osx.hyperkit.linux"   # docker restart
alias dps="docker ps"                               # docker processes list
alias dcl="docker container ls -aq"                 # docker list active container

alias dpa="docker container prune --force"          # Remove all stopped containers

# To avoid "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
if [ -f "/var/run/docker.pid" ]; then  # NOT found:
   alias dsa="docker stop $(docker container ls -aq )" # docker stop active container
   alias dpx="docker rm -v $(docker ps -aq -f status=exited)"  # Remove stopped containers
fi
alias mk8s="minikube delete;minikube start --driver=docker --memory=4096"

#if command -v docker >/dev/null; then  # installed in /usr/local/bin/docker
#   echo "Docker installed, so ..."
#   alias dockx="docker stop $(docker ps -a -q);docker rm -f $(docker ps -a -q)"
#fi
# See https://github.com/ysmike/dotfiles/blob/master/bash/.aliases
# More: https://www.cyberciti.biz/tips/bash-aliases-mac-centos-linux-unix.html

alias wmx='cd $HOME/gmail_acct/azure-quickly'
alias wmf='cd $HOME/gmail_acct/futures'
alias wmo='cd $HOME/gmail_acct/wilsonmar.github.io/_posts'
alias wmb='cd $HOME/gmail_acct/DevSecOps/bash'
alias wmp='cd $HOME/gmail_acct/python-samples'
alias wmgo='cd $HOME/gmail_acct/golang-samples'

alias micd='cd $HOME/McK-Internal'
alias mpcd='cd $HOME/McK-Private'
alias mycd='cd $HOME/McK-Playground'
alias mecd='cd $HOME/McK-Enterprise-Automation/onefirmgithub-vault-scripts'

alias mitt='cd $HOME/McK-Internal-Test'
alias mptt='cd $HOME/McK-Private-Test'
alias mytt='cd $HOME/McK-Playground-Test'

alias keys="catn $HOME/gmail_acct/git-utilities/aliases.sh"
