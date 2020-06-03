# Create Cloud Image

There is an Ansible script that will install the dev stack on a Ubuntu machine.
You will need to run the Ansible script, then the cloud-init script to purge
cloud data from the machine. You will need to have Ansible installed on your
local machine to follow this guide.

1. Create an instance on SDSC cloud. You can follow the guide [here](https://sdsc-ucsd.atlassian.net/wiki/spaces/SC/pages/110034977/Getting+Started+with+Linux+Instances).
Make sure that you select "Ubuntu 18.04 LTS x86_64" as your source and have
set up ssh access (keypair, security group and floating ip).

2. Make sure that you are in create_image/ansible/ and then run the playbook.
This command will take some time to run.

    ```
    ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' -i <ip address of instance>, -u ubuntu  create_dev_env.yml
    ```

3. Make sure that you are in create_image/ and run the cloud-init script. Once
you run this command, you will not be able to ssh back into the instance.
    
    ```
    cat prepare_for_cloud_init.sh | ssh -l ubuntu <ip address of instance> /bin/bash
    ```

4. Go to the SDSC Cloud dashboard [instances page](https://dashboard.cloud.sdsc.edu/dashboard/project/instances/). Find the instance that you are working with. On
the very right, under the "Actions" row, click the dropdown arrow and select 
"Shut Off Instance".

5. Go to the SDSC Cloud dashboard [volumes page](https://dashboard.cloud.sdsc.edu/dashboard/project/volumes/). From there, find the volume attached to your instance that
you just shut down. On the very right, under the "Actions" row, click the
dropdown arrow and select "Create Snapshot".

6. Go to the SDSC Cloud dashboard [snapshots page](https://dashboard.cloud.sdsc.edu/dashboard/project/snapshots/). From there, find the snapshot you just created.
On the very right, under the "Actions" row, click the "Create Volume" button.

7. Go to the SDSC Cloud dashboard [volumes page](https://dashboard.cloud.sdsc.edu/dashboard/project/volumes/). From there, find the volume that you just created. On the 
very right, under the "Actions" row, click the dropdown arrow and select 
"Upload to Image". The image may take some time to upload. You can check on the
status by going to the SDSC Cloud dashboard [images page](https://dashboard.cloud.sdsc.edu/dashboard/project/images).
