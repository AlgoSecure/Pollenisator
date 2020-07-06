
# Tools recommendation #

These are the first tools to install for a decent pentest discovery step.

It is highly recommended to not hardcode any path in the bash commands and instead use the PATH variable so that your coworkers can set their environments easier. Or to use one common worker only.


## Table of Contents

Quick list of how to install those tools on a classic linux.

1. [Nmap](#nmap)
2. [WhatWeb](#whatweb)
3. [TestSSL](#testssl)
4. [Nikto](#nikto)
5. [Dirsearch](#dirsearch)
6. [Knockpy](#knockpy)
7. [SSH SCAN](#sshscan)
8. [crtsh](#crtsh)
9. [amap](#amap)
10. [smbmap](#smbmap)
11. [enum4linux](#enum4linux)

## Nmap <a name="nmap"></a> ##

The most well-known port scanner.

If you use it, remember that udp scanning requires root privileges, so you must start your worker with root privileges. Celery will prevent you to do so unless you declare the C_FORCE_ROOT variable to true by doing `export C_FORCE_ROOT="true"`.

See https://www.howtoforge.com/tutorial/nmap-on-linux/ to install.

## Whatweb <a name="whatweb"></a> ##

A tool to get informations on a web serveur.

See https://github.com/urbanadventurer/WhatWeb/wiki/Installation to install.

## TestSSL <a name="testssl"></a> ##

A tool to get a SSL evaluation of an open ssl port.

See https://github.com/drwetter/testssl.sh to install.

## Nikto <a name="nikto"></a> ##

A web vulnerability scanner tool.

See https://github.com/sullo/nikto to install.

## Dirsearch <a name="dirsearch"></a> ##

A tool that tries to list all directories of a website.

See https://github.com/maurosoria/dirsearch to install.


## Knockpy <a name="knockpy"></a> ##

A tool that tries to list all subdomains of a domain.

See https://github.com/guelfoweb/knock to install.

## Sublist3r <a name="sublister"></a> ##

A tool that tries to list all subdomains of a domain.

See https://github.com/aboul3la/Sublist3r to install.

## SSH scan <a name="sshscan"></a> ##

Analyze an ssh configuration.

https://github.com/mozilla/ssh_scan

## crtsh <a name="crtsh"></a> ##

Enumerate certificates associated with a given domain name

https://github.com/tdubs/crt.sh

## amap <a name="amap"></a> ##

Tries to guess the service running behind an open port

https://github.com/BlackArch/amap

## SmbMap <a name="smbmap"></a> ##

List files on samba shares

https://github.com/ShawnDEvans/smbmap

## enum4linux <a name="enum4linux"></a> ##

Enumerate AD infos

https://github.com/portcullislabs/enum4linux

## ikescan <a name="ikescan"></a> ##

Scan les échanges de clées des services isakmp

https://github.com/royhills/ike-scan
