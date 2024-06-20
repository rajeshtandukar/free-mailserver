erase_prev_server_installations = 'rm -rf mailu /mailu'
cmd_install_sed = 'yum install sed 1 > /dev/null'
cmd_install_lsof_and_unzip = "yum install -y lsof unzip"
cmd_check_install_or_update_docker = ''' if [ -x "$(command -v docker)" ]; then
    echo "Installed docker"
else
    echo "Install docker"
fi '''
cmd_install_yum_utils = 'yum install -y yum-utils'
cmd_add_yum_repo = 'yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo'
cmd_install_docker = 'yum install docker-ce docker-ce-cli containerd.io -y'
cmd_check_docker_compose = '(ls /usr/local/bin/docker-compose >> /dev/null 2>&1 && echo yes) || echo no'
cmd_download_docker_compose = 'curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
cmd_permissions_docker_compose = 'chmod +x /usr/local/bin/docker-compose'
cmd_docker_compose_version = 'docker-compose --version'
cmd_create_directory = 'mkdir -p /mailu'
cmd_change_mail_ectory = 'cd /mailu;'
cmd_copy_contents = 'cp -rf mailu/* /mailu'
cmd_start_docker_engine = 'systemctl restart docker; systemctl enable docker'
cmd_stop_docker_compose ='docker-compose stop'
cmd_start_docker_compose = 'docker-compose up -d'
cmd_start_docker_compose_mail_server = 'docker-compose -p mailu up -d'
password="ad!234@#%"
cmd_kill_ports = 'kill $(lsof -t -i:995); kill $(lsof -t -i:80); kill $(lsof -t -i:443); kill $(lsof -t -i:25); kill $(lsof -t -i:465); kill $(lsof -t -i:587); kill $(lsof -t -i:110) ;kill $(lsof -t -i:995); kill $(lsof -t -i:143); kill $(lsof -t -i:993)'
def yml_file_sed_cmd(ip):
  return "sed -i 's/{{MAIL_SERVER_IP}}/'" + ip + "'/' mailu/docker-compose.yml"
def env_file_sed_cmd(domain):
  return "sed -i 's/{{MAIL_SERVER_DOMAIN}}/'" + domain + "'/' mailu/mailu.env"
def cmd_create_mail_admin_user(admin, domain, password):
  return 'cd /mailu; docker-compose -p mailu exec -T admin flask mailu admin {} {} "{}"'.format(admin,domain,password)
