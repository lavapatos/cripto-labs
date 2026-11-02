FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash lab4 && passwd -d lab4
RUN mkdir -p /home/lab4/.ssh && chown lab4:lab4 /home/lab4/.ssh && chmod 700 /home/lab4/.ssh

COPY --chown=lab4:lab4 --chmod=600 authorized_keys /home/lab4/.ssh/authorized_keys
COPY sshd_config /etc/ssh/sshd_config

RUN rm -f /etc/ssh/ssh_host_* && ssh-keygen -q -t ed25519 -N '' -f /etc/ssh/ssh_host_ed25519_key
RUN mkdir -p /run/sshd && /usr/sbin/sshd -t -f /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]
