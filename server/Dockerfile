FROM mongo
ARG SSHPASSWORD=pollenisator123
RUN apt-get update
RUN apt-get install -y openssh-server
RUN adduser pollenisator && usermod -s /bin/false pollenisator && usermod -d / pollenisator && mkdir -p /etc/Pollenisator/files/ && chown root.root /etc/Pollenisator && chown pollenisator.pollenisator /etc/Pollenisator/files
RUN echo "pollenisator:$SSHPASSWORD" | chpasswd
RUN sed -i 's/Subsystem\tsftp\t\/usr\/lib\/openssh\/sftp-server/Subsystem sftp internal-sftp/g' /etc/ssh/sshd_config
RUN echo "Match User pollenisator\n\tChrootDirectory /etc/Pollenisator/\n\tPermitTunnel no\n\tX11Forwarding no\n\tAllowTcpForwarding no\n\tForceCommand internal-sftp\n\tPasswordAuthentication yes\n" >> /etc/ssh/sshd_config
RUN service ssh stop
RUN service ssh start
EXPOSE 22
EXPOSE 27017
CMD ["/bin/sh", "-c", "service ssh restart && mongod --bind_ip_all"]
