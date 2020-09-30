FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
ARG SSHPASSWORD=pollenisator123
RUN apt-get update
RUN apt-get install -y gnupg2
RUN apt-get install -y apt-transport-https wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list
# Dependencies
# whatweb as whatweb
# nikto as nikto
# dnsrecon as dnsrecon
RUN apt-get update && \
	apt-get install -y python3 && \
	apt-get install -y python3.7 python3.7-dev && \
	apt-get install -y python3-tk && \
	apt-get install -y wget && \
	apt-get install -y curl && \
	apt-get install -y nmap && \
	apt-get install -y git && \
	apt-get install -y dnsutils && \
	apt-get install -y nikto && \
	apt-get install -y dnsrecon && \
	apt-get install -y python3-dev && \
	apt-get install -y libssl-dev && \
	apt-get install -y libffi-dev && \
	apt-get install -y mongodb-org-tools && \
	apt-get install -y python-requests && \
	apt-get install -y ruby ruby-dev && \
	apt-get install -y bsdmainutils && \
	apt-get install -y smbclient && \
	apt-get install -y python-dev && \
	apt-get install -y python3-pip && \
	apt-get install -y nano && \
	apt-get install -y build-essential
RUN wget https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
RUN python3 get-pip.py

RUN apt-get install -y autoconf
# Test SSL as testssl.sh
RUN git clone --depth 1 https://github.com/drwetter/testssl.sh.git /home/testssl.sh && \
	chmod +x /home/testssl.sh/testssl.sh && \
	ln -s /home/testssl.sh/testssl.sh /usr/bin/testssl.sh


RUN pip3 install --upgrade setuptools
# Pollenisator
RUN git clone https://github.com/AlgoSecure/Pollenisator.git /home/Pollenisator && \
	python3 -m pip install -r /home/Pollenisator/requirements.txt
# Dirsearch as dirsearch.py
RUN git clone https://github.com/maurosoria/dirsearch.git /home/dirsearch/ && \
	chmod +x /home/dirsearch/dirsearch.py && \
	ln -s /home/dirsearch/dirsearch.py /usr/bin/dirsearch.py
# Knockpy as knockpy.py
RUN apt-get install -y python-dnspython python-pip
RUN python2 -m pip install setuptools
RUN git clone https://github.com/guelfoweb/knock.git /home/knock && \
	cd /home/knock && \
	chmod +x /home/knock/knockpy/knockpy.py && \
	python2 /home/knock/setup.py install && \
	ln -s /home/knock/knockpy/knockpy.py /usr/bin/knockpy.py && \
	cp -r /home/knock/knockpy/wordlist /usr/bin/wordlist

# Sublist3r as sublist3r.py
RUN git clone https://github.com/aboul3la/Sublist3r.git /home/sublist3r/ && \
	pip3 install -r /home/sublist3r/requirements.txt && \
	chmod +x /home/sublist3r/sublist3r.py && \
	ln -s /home/sublist3r/sublist3r.py /usr/bin/sublist3r.py
# SSH scan as ssh_scan
RUN gem install ssh_scan


# crtsh as crtsh.py
COPY crtsh /home/crtsh
RUN pip3 install feedparser && \
	chmod +x /home/crtsh/crtsh.py && \
	ln -s /home/crtsh/crtsh.py /usr/bin/crtsh.py

# amap as amap
RUN git clone https://github.com/BlackArch/amap/ /home/amap/
WORKDIR /home/amap
RUN ./configure && make && make install


# Smbmap as smbmap.py
RUN git clone https://github.com/ShawnDEvans/smbmap /home/smbmap && \
	pip3 install -r /home/smbmap/requirements.txt && \
	chmod +x /home/smbmap/smbmap.py && \
	ln -s /home/smbmap/smbmap.py /usr/bin/smbmap.py
# enum4linux as enum4linux.pl
RUN git clone https://github.com/portcullislabs/enum4linux /home/enum4linux && \
	chmod +x /home/enum4linux/enum4linux.pl && \
	ln -s /home/enum4linux/enum4linux.pl /usr/bin/enum4linux.pl
# ikescan as 
RUN git clone https://github.com/royhills/ike-scan /home/ike-scan
WORKDIR /home/ike-scan
RUN autoreconf --install && ./configure --with-openssl && make && make check && make install

# WhatWeb
RUN wget https://codeload.github.com/urbanadventurer/WhatWeb/tar.gz/v0.4.9 -O /tmp/whatweb.tar.gz && \
	cd /home && \
	tar xvfz /tmp/whatweb.tar.gz && \
	mv WhatWeb-0.4.9 whatweb && \
	rm /tmp/whatweb.tar.gz && \
	ln -s /home/whatweb/whatweb /usr/bin/whatweb
# bluekeep scanner
RUN git clone https://github.com/robertdavidgraham/rdpscan /home/rdpscan && cd /home/rdpscan && make && ln -s /home/rdpscan/rdpscan /usr/bin/rdpscan
# EternalBlue
RUN wget https://svn.nmap.org/nmap/scripts/smb-vuln-ms17-010.nse -O /usr/share/nmap/scripts/smb-vuln-ms17-010.nse
#Searchsploit
RUN git clone https://github.com/offensive-security/exploitdb.git /opt/exploitdb
RUN sed 's|path_array+=(.*)|path_array+=("/opt/exploitdb")|g' /opt/exploitdb/.searchsploit_rc > ~/.searchsploit_rc
RUN ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit
#OPenrelay
COPY smtp-open-relay.nse /usr/share/nmap/scripts/smtp-open-relay.nse

# Set timezone
ENV TZ Europe/Paris

#CME
RUN python3.7 /get-pip.py
RUN rm /get-pip.py
RUN git clone --recursive https://github.com/byt3bl33d3r/CrackMapExec /home/cme/
WORKDIR /home/cme/
RUN python3.7 -m pip install --upgrade pynacl
RUN python3.7 -m pip install --upgrade cryptography
RUN python3.7 -m pip install --upgrade asn1crypto
RUN pip install .
RUN cme smb
#
WORKDIR /home/Pollenisator/
ARG CACHEBUST=1
RUN git pull
COPY config /home/Pollenisator/config
RUN chmod +x /home/Pollenisator/startWorker.sh
## SERVER 
RUN apt-get install -y openssh-server libcurl3 mongodb-org-shell mongodb-org-server mongodb-org
RUN mkdir -p /data/db
RUN adduser pollenisator && usermod -s /bin/false pollenisator && usermod -d / pollenisator && mkdir -p /etc/Pollenisator/files/ && chown root.root /etc/Pollenisator && chown pollenisator.pollenisator /etc/Pollenisator/files
RUN echo "pollenisator:$SSHPASSWORD" | chpasswd
RUN sed -i 's/Subsystem\tsftp\t\/usr\/lib\/openssh\/sftp-server/Subsystem sftp internal-sftp/g' /etc/ssh/sshd_config
RUN echo "Match User pollenisator\n\tChrootDirectory /etc/Pollenisator/\n\tPermitTunnel no\n\tX11Forwarding no\n\tAllowTcpForwarding no\n\tForceCommand internal-sftp\n\tPasswordAuthentication yes\n" >> /etc/ssh/sshd_config
RUN service ssh stop
RUN service ssh start
## CLIENT
RUN apt-get install -y python3-tk python3-pil python3-pil.imagetk xsel xdg-utils gedit
RUN python3 -m pip install -r requirements.txt
COPY start.sh /home/Pollenisator/start.sh
ENV DISPLAY :0
CMD ["/bin/sh", "-c", "./start.sh"]
