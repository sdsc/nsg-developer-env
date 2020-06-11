# Running a Jupyter Notebook

## Start the Notebook Server
To start a notebook server, run the following command from the
development server:
``` bash
jupyter notebook --no-browser
```
Make sure that you leave your terminal open to keep the notebook
server up.

## Connecting to the Notebook Server
To securely connect to a notebook on a development instance, you
can either connect to the notebook using the VNC or use an ssh
tunnel to connect to the notebook directly.

### Using the VNC
1. Follow the instructions in the VNC guide to connect to the
VNC with a VNC client.

2. From within your VNC client, you can launch a browser with the following
command:
``` bash
google-chrome
```

3. In the browser, copy and paste the link that the notebook
command printed to the screen. Note that if you have problems
copying and pasting the link from your terminal to the VNC client,
you instead run the notebook server from a terminal within your
VNC client.


### Using an SSH Tunnel Directly
1. On your local machine, set up the ssh tunnel with the following command. Make
sure to keep the terminal open to keep the connection open:
``` bash
ssh -L <local-port>:127.0.0.1:<dev-instance-port> -C -N ubuntu@<dev-instance-ip>
```
\<dev-instance-port\> is the port that the jupyter notebook command has
included in its output (probably 8888). \<local-port\> is whatever port on your
local machine that you would like to access the notebook on. It can be any port
that is open, but if you change it to something other than
\<dev-instance-port\>, make sure that connect to that port in the next
step.

2. Open up a browser on your local computer and paste in the link from the
notebook server command. If \<local-port\> is different from
\<dev-instance-port\>, make sure to use \<local-port\>.
