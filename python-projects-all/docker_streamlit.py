import streamlit as st
import os
import subprocess
import pandas as pd


st.set_page_config(page_title="Remote Docker Manager")
st.title("🐳 Remote Docker via SSH")

# SSH credentials input
st.sidebar.header("🔐 SSH Connection")
ssh_ip = st.sidebar.text_input("Remote Host IP", placeholder="e.g. 192.168.1.10")
ssh_user = st.sidebar.text_input("Username", placeholder="e.g. ubuntu")

def run_ssh_cmd(cmd, show_output=True):
    full_cmd = f"ssh {ssh_user}@{ssh_ip} {cmd}"
    st.code(f"$ {full_cmd}")

    try:
        result = subprocess.check_output(full_cmd, shell=True, text=True)
        if show_output:
            st.code(result)
        return result
    except subprocess.CalledProcessError as e:
        error_output = e.output or str(e)
        if show_output:
            st.error(f"❌ Error:\n{error_output}")
        return error_output

if ssh_ip and ssh_user:
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
    st.warning("Please enter SSH IP and Username in the sidebar.")

