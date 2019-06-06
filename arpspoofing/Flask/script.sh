#!/bin/bash

# URLs
login_url="http://10.0.1.10/login"
index_url="http://10.0.1.10/index"
cookie_path=$( mktemp /tmp/cookie-XXXXXXXXXXXX )
temporal_file=$( mktemp /tmp/html-XXXXXXXXXXXX )

while true;  do

	# Getting CSRF token / Pidiendo la página.
	token=$(curl -s  $login_url --cookie $cookie_path --cookie-jar $cookie_path | awk -F 'value' '/csrf_token/ {print $2}' | cut -d"\"" -f2 2> /dev/null )
	token=$(echo $token | awk '{print $1;}')
	
	# Enviando las credenciales de login
	username=syper
	data="username=$username&password=53Cre71234@!&csrf_token=$token"
	
	# login
	sleep 3
	curl -s -X POST $login_url?next=%2Findex --data $data --cookie $cookie_path --cookie-jar $cookie_path #-o $temporal_file
	
	# index que simula el redirect
	curl -s -L  $index_url  --cookie $cookie_path --cookie-jar $cookie_path #-o $temporal_file
	
	$sleep 3
	
	# Debemos hacer alguna consulta de algo: por ejemplo, cuánto saldo tengo
	curl -s http://10.0.1.10/user/$username --cookie $cookie_path --cookie-jar $cookie_path 
	
	$sleep 3
	
	# Logout
	curl -s http://10.0.1.10/logout --cookie $cookie_path --cookie-jar $cookie_path
	
	rm $cookie_path
	rm $temporal_file
	
	sleep 60;

done;
