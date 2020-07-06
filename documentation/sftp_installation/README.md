## Requirements ##

Connect to backend then:

`$ sudo apt-get install openssh-server`

`$ sudo adduser pollenisator`

`$ sudo usermod -s /bin/false pollenisator`

`$ sudo usermod -d / pollenisator`

`$ sudo mkdir -p /etc/Pollenisator/files/`

`$ sudo chown root.root /etc/Pollenisator`

`$ sudo chown pollenisator.pollenisator /etc/Pollenisator/files`

Add a password usng the following command for the new pollenisator user

`$ sudo passwd pollenisator`

Then open your ssh config file (located in /etc/ssh/sshd_config)
For example with nano

`$ sudo nano /etc/ssh/sshd_config`

And replace the line:
` Subsystem sftp /usr/lib/openssh/sftp-server`

By

`Subsystem sftp internal-sftp`

And add at the end of the file:

```
Match User pollenisator
	ChrootDirectory /etc/Pollenisator/
	PermitTunnel no
	X11Forwarding no
	AllowTcpForwarding no
	ForceCommand internal-sftp
	PasswordAuthentication yes
```

Then restart ssh service:

`$ sudo systemctl restart ssh`