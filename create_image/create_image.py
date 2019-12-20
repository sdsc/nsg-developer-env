import cred
import os
import openstack
import socket
import stat
import subprocess
from time import sleep


def main():

    conn = openstack.connect(
        auth_url=cred.uth_url,
        project_name=cred.project_name,
        username=cred.username,
        password=cred.password,
        region_name='SDSC',
        user_domain_name="Default",
        project_domain_id='default'
    )
    
    try:
        volume = None
        keypair = None
        security_group = None
        floating_ip = None
        server = None
        private_key_file = None

        network = conn.network.find_network('nsg-devs_network')
        network_dict = {'uuid': network.id}
        flavor = conn.compute.find_flavor('m1.medium')
        image = conn.compute.find_image('Ubuntu 18.04 LTS x86_64')
        ext_network = conn.network.find_network('ext-net')


        volume = conn.block_storage.create_volume(size=20)
        print('created volume')

        keypair = conn.compute.create_keypair(name='image_creation_keypair')
        print('keypair created')

        security_group = conn.network.create_security_group(name='ssh_security_group_for_ansible')
        print('security group created')

        security_group_rule = conn.network.create_security_group_rule(
            direction='ingress', security_group_id=security_group.id,
            port_range_min=22, port_range_max=22, ethertype='IPv4', 
            protocol='tcp'
            )
        print('security group rule created')

        floating_ip = conn.network.create_ip(floating_network_id=ext_network.id)
        print('floating ip created')

        server = conn.compute.create_server(
            name='NewServer', flavorRef=flavor.id, imageRef=image.id,
            networks=[network_dict], key_name=keypair.name, block_dev_mapping =[{'vda': volume.id}]
            )
        conn.compute.wait_for_server(server)
        print('server created')

        conn.compute.add_floating_ip_to_server(server, floating_ip.floating_ip_address)
        conn.compute.add_security_group_to_server(server, security_group)
        print(f'floating ip {floating_ip.floating_ip_address} added to server')

        wait_for_ssh_port(floating_ip.floating_ip_address, 5, 20)
        configure_server(floating_ip.floating_ip_address, keypair.private_key)
        conn.compute.create_server_image(server, 'test-image')

        val = input("Press Enter to Destroy: ") 

    except Exception as e:
        print(e)

    finally:
        if volume is not None:
            conn.block_storage.delete_volume(volume)
            print('deleted volume')

        if keypair is not None:
            conn.compute.delete_keypair(keypair)
            print('keypair deleted')

        if server is not None:
            if floating_ip is not None:
                conn.compute.remove_floating_ip_from_server(server, floating_ip.floating_ip_address)

            if security_group is not None:
                conn.compute.remove_security_group_from_server(server, security_group)

            conn.compute.delete_server(server)
            print('server deleted')

        if floating_ip is not None:
            conn.network.delete_ip(floating_ip)
            print('floating ip deleted')
        
        if security_group is not None:
            conn.network.delete_security_group(security_group)
            print('security group deleted')

def configure_server(ip, private_key_string):
    try:
        os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'False'
        private_key_file = open('private_key', 'w')
        print('private key file created')
        private_key_file.write(private_key_string)
        private_key_file.flush()
        absolute_file_path = os.path.abspath(private_key_file.name)
        os.chmod(absolute_file_path, stat.S_IREAD | stat.S_IWRITE)
        print(absolute_file_path)
        cmd = f'ansible-playbook -i {ip}, -u ubuntu --private-key {absolute_file_path} ansible/create_dev_env.yml'
        print(cmd)
                
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        print(process.returncode)

        cmd = f'cat prepare_for_cloud_init.sh | ssh -o StrictHostKeyChecking=no -i {absolute_file_path} -l ubuntu {ip} /bin/bash'
        print(cmd)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        print(process.returncode)

    except Exception as e:
        print(e)

    finally:
        if private_key_file is not None:
            name = private_key_file.name
            private_key_file.close()
            os.remove(name)
            print('private key file deleted')

def wait_for_ssh_port(ip, interval_seconds, num_attempts):
    num_tries = 0

    while(num_tries < num_attempts):
        if port_is_open(ip, 22):
            return
        else:
            num_tries = num_tries + 1
            sleep(interval_seconds)
            
    raise TimeoutError(f'Port 22 was not open after {num_attempts} attempts')

def port_is_open(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

if __name__ == "__main__":
    main()