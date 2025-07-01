import streamlit as st
import paramiko

st.set_page_config(page_title="Remote Docker Manager")
st.title("🐳 Remote Docker via SSH (with password support)")

# SSH input
st.sidebar.header("🔐 SSH Connection")
ssh_ip = st.sidebar.text_input("Remote Host IP", placeholder="e.g. 192.168.1.10")
ssh_user = st.sidebar.text_input("Username", placeholder="e.g. ubuntu")
ssh_password = st.sidebar.text_input("Password", type="password")

# Reusable SSH command runner
def run_ssh_cmd(cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_ip, username=ssh_user, password=ssh_password)
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        
        if output:
            st.code(output)
        if error:
            st.error(error)
            
        return output or error
    except Exception as e:
        st.error(f"SSH Connection Failed: {e}")
        return None

if ssh_ip and ssh_user and ssh_password:
    st.success("SSH connection ready")

    menu = [
        "Pull Docker Image", "Run Docker Image", "Stop Container", "Start Container",
        "Remove Container", "List Images", "List Containers",
        "Push to DockerHub", "Install Docker"
    ]
    choice = st.selectbox("Select Docker Action", menu)

    if choice == "Pull Docker Image":
        image = st.text_input("Enter image name to pull:")
        if st.button("Pull"):
            run_ssh_cmd(f"docker pull {image}")

    elif choice == "Run Docker Image":
        image = st.text_input("Image name:")
        name = st.text_input("Container name:")
        if st.button("Run"):
            run_ssh_cmd(f"docker run -itd --name {name} {image}")

    elif choice == "Stop Container":
        name = st.text_input("Container name to stop:")
        if st.button("Stop"):
            run_ssh_cmd(f"docker stop {name}")

    elif choice == "Start Container":
        name = st.text_input("Container name to start:")
        if st.button("Start"):
            run_ssh_cmd(f"docker start {name}")

    elif choice == "Remove Container":
        name = st.text_input("Container name to remove:")
        if st.button("Remove"):
            run_ssh_cmd(f"docker rm -f {name}")

    elif choice == "List Images":
        if st.button("Show Images"):
            run_ssh_cmd("docker images")

    elif choice == "List Containers":
        if st.button("Show Containers"):
            run_ssh_cmd("docker ps -a")

    elif choice == "Push to DockerHub":
        local_image = st.text_input("Local image name:")
        dockerhub_user = st.text_input("DockerHub username:")
        repo_name = st.text_input("DockerHub repo/image name:")
        if st.button("Push"):
            run_ssh_cmd(f"docker tag {local_image} {dockerhub_user}/{repo_name}")
            run_ssh_cmd(f"docker push {dockerhub_user}/{repo_name}")

    elif choice == "Install Docker":
        if st.button("Install Docker"):
            run_ssh_cmd("sudo dnf -y install dnf-plugins-core")
            run_ssh_cmd("sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo")
            run_ssh_cmd("sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
            run_ssh_cmd("sudo systemctl start docker && sudo systemctl enable docker")
else:
    st.warning("Please enter SSH IP, Username, and Password in the sidebar.")
