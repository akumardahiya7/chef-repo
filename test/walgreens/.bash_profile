# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi


# User specific environment and startup programs
export JAVA_HOME=/usr/jdk64/jdk1.8.0_112

#PATH=$PATH:$HOME/.local/bin:$HOME/bin
PATH=$JAVA_HOME/bin:$PATH:$HOME/.local/bin:$HOME/bin

export PATH

