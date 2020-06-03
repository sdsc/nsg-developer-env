# How to use VNC

Make sure that you have an instance that has a publicly accessible ip address.
We will use ssh tunnelling to create a secure connection to your vnc server. You
will also need a VNC client installed on your local machine that you will be
using to connect to your instance.

1. On your local machine, create an ssh tunnel:
    ```
    ssh -L 5901:127.0.0.1:5901 -C -N ubuntu@<remote-instance-ip>
    ```
2. On your local machine, use your VNC client to connect to localhost:5901 . The password is **nsg-dev** .