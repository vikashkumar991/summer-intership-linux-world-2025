import streamlit as st
import subprocess
import os
import base64
import io
import json
import requests
import paramiko
from PIL import Image
import google.generativeai as genai
from datetime import datetime
import time
import re
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="DevOps Multi-Tool",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-box {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #00cec9 0%, #55a3ff 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .command-output {
        background: #2d3748;
        color: #68d391;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        border-left: 4px solid #68d391;
    }
    
    .ai-response {
        background: linear-gradient(135deg, #3c5a58 0%, #7f324b 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'command_history' not in st.session_state:
    st.session_state.command_history = []
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []

# Sidebar menu
st.sidebar.markdown("## 🚀 DevOps Multi-Tool")
st.sidebar.markdown("---")

menu_option = st.sidebar.selectbox(
    "Select Tool",
    ["🏠 Home", "📱 JavaScript Tools", "🐧 Linux Commander", "🐳 Docker Manager", "🤖 AI Prompt Engineer"]
)

st.sidebar.markdown("### 🔒 SSH Connection Setup")

ssh_host = st.sidebar.text_input("🌐 Host/IP Address", placeholder="192.168.1.100")
ssh_username = st.sidebar.text_input("👤 Username", placeholder="ubuntu")
ssh_port = st.sidebar.number_input("🔌 Port", value=22, min_value=1, max_value=65535)
ssh_password = st.sidebar.text_input("🔐 Password", type="password")

if st.sidebar.button("🔗 Test SSH Connection"):
    if ssh_host and ssh_username and ssh_password:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password, timeout=10)
            ssh.close()
            st.sidebar.success("✅ SSH Connection Successful!")
            st.session_state.ssh_connected = True  # Set connection state
        except Exception as e:
            st.sidebar.error(f"❌ Connection Failed: {str(e)}")
            st.session_state.ssh_connected = False
    else:
        st.sidebar.error("❌ Please fill in all connection details")

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚀 Advanced DevOps Multi-Tool Platform</h1>
    <p>Your all-in-one solution for JavaScript utilities, Linux operations, Docker management, and AI assistance</p>
</div>
""", unsafe_allow_html=True)

# Home Page
if menu_option == "🏠 Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h3>📱 JavaScript Tools</h3>
            <p>• Image capture and processing</p>
            <p>• WhatsApp integration</p>
            <p>• File download utilities</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🐧 Linux Commander</h3>
            <p>• Remote command execution</p>
            <p>• SSH connectivity</p>
            <p>• Real-time output display</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h3>🐳 Docker Manager</h3>
            <p>• Container management</p>
            <p>• Image operations</p>
            <p>• Dockerfile generation</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h3>🤖 AI Prompt Engineer</h3>
            <p>• Automated command execution</p>
            <p>• Intelligent prompt processing</p>
            <p>• Gemini AI integration</p>
        </div>
        """, unsafe_allow_html=True)

# JavaScript Tools
elif menu_option == "📱 JavaScript Tools":
    st.markdown("## 📱 JavaScript Utilities")
    
    tab1, tab2, tab3 = st.tabs(["📷 Image Capture", "📱 WhatsApp Integration", "📥 File Download"])
    
    with tab1:
        st.markdown("### 📷 Image Capture Tool")

        image = st.camera_input("📷 Capture Image from Camera")

        if image is not None:
            img = Image.open(image)
            col1, col2 = st.columns(2)

            with col1:
                st.image(img, caption="Captured Image", use_column_width=True)

            with col2:
                st.markdown("### Image Properties")
                st.write(f"**Format:** {img.format}")
                st.write(f"**Size:** {img.size}")
                st.write(f"**Mode:** {img.mode}")

                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_data = buffer.getvalue()

                st.download_button(
                    label="📥 Download Captured Image",
                    data=img_data,
                    file_name="captured_image.png",
                    mime="image/png"
                )
    
    with tab2:
        st.markdown("### 📱 WhatsApp Integration")
        st.info("WhatsApp Web API integration for sending images")
        
        phone_number = st.text_input("📞 Phone Number (with country code)", placeholder="+1234567890")
        message_text = st.text_area("💬 Message Text", placeholder="Hello! Sending you an image.")
        
        if st.button("📤 Send to WhatsApp"):
            if phone_number and message_text:
                # WhatsApp Web URL format
                whatsapp_url = f"https://wa.me/{phone_number.replace('+', '')}?text={message_text.replace(' ', '%20')}"
                st.markdown(f"[🔗 Click to open WhatsApp]({whatsapp_url})")
                st.success("✅ WhatsApp link generated successfully!")
            else:
                st.error("❌ Please fill in all fields")
    
    with tab3:
        st.markdown("### 📥 File Download Utilities")
        
        # Sample files for download
        sample_data = {
            "sample.txt": "This is a sample text file generated by the DevOps Multi-Tool!",
            "config.json": json.dumps({"app": "DevOps Multi-Tool", "version": "1.0", "features": ["JS", "Linux", "Docker", "AI"]}, indent=2),
            "script.sh": "#!/bin/bash\necho 'Hello from DevOps Multi-Tool!'\ndate\n"
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "📄 Download Text File",
                data=sample_data["sample.txt"],
                file_name="sample.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                "📋 Download JSON Config",
                data=sample_data["config.json"],
                file_name="config.json",
                mime="application/json"
            )
        
        with col3:
            st.download_button(
                "📜 Download Shell Script",
                data=sample_data["script.sh"],
                file_name="script.sh",
                mime="text/plain"
            )

# Linux Commander
elif menu_option == "🐧 Linux Commander":
    st.markdown("## 🐧 Linux Command Executor")
    
    st.markdown("### 💻 Remote Command Execution")
    
    command = st.text_input("⌨️ Enter Command", placeholder="ls -la")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Execute Command"):
            if command and 'ssh_host' in locals() and ssh_host:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
                    
                    stdin, stdout, stderr = ssh.exec_command(command)
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    
                    st.session_state.command_history.append({
                        'command': command,
                        'output': output,
                        'error': error,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    if output:
                        st.markdown(f"""
                        <div class="command-output">
                            <strong>Output:</strong><br>
                            <pre>{output}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if error:
                        st.markdown(f"""
                        <div class="error-box">
                            <strong>Error:</strong><br>
                            <pre>{error}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    ssh.close()
                except Exception as e:
                    st.error(f"❌ Execution failed: {str(e)}")
            else:
                st.error("❌ Please enter a command and ensure SSH connection is configured")
    
    with col2:
        if st.button("📜 Show Command History"):
            if st.session_state.command_history:
                for i, cmd in enumerate(reversed(st.session_state.command_history[-5:])):
                    st.markdown(f"""
                    <div class="command-output">
                        <strong>#{len(st.session_state.command_history)-i}: {cmd['command']}</strong><br>
                        <small>{cmd['timestamp']}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Docker Manager
elif menu_option == "🐳 Docker Manager":
    st.markdown("## 🐳 Docker Operations Manager")
    if ssh_host and ssh_username and ssh_password:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
            
            tab1, tab2, tab3 = st.tabs(["📦 Image Management", "🏗️ Container Operations", "📝 Dockerfile Generator"])

            with tab1:
                st.markdown("### 📦 Docker Image Management")
                col1, col2 = st.columns(2)

                with col1:
                    image_name = st.text_input("🏷️ Image Name", placeholder="python:3.9")
                    if st.button("⬇️ Pull Image"):
                        if image_name:
                            with st.spinner("Pulling image via SSH..."):
                                stdin, stdout, stderr = ssh.exec_command(f"docker pull {image_name}")
                                result = stdout.read().decode()
                                error = stderr.read().decode()
                                if error:
                                    st.error(f"❌ {error}")
                                else:
                                    st.success(f"✅ Pulled: {image_name}")
                                    st.code(result)
                        
                    if st.button("⬇️ Run Image"):
                        if image_name:
                            with st.spinner("Running image via SSH..."):
                                stdin, stdout, stderr = ssh.exec_command(f"docker run -itd {image_name}")
                                result = stdout.read().decode()
                                error = stderr.read().decode()
                                if error:
                                    st.error(f"❌ {error}")
                                else:
                                    st.success(f"✅ Running: {image_name}")
                                    st.code(result)

                with col2:
                    if st.button("📋 List Images"):
                        stdin, stdout, stderr = ssh.exec_command("docker images")
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.code(result)

            with tab2:
                st.markdown("### 🏗️ Container Operations")
                container_name = st.text_input("📦 Container Name", placeholder="my-container")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("▶️ Start Container") and container_name:
                        stdin, stdout, stderr = ssh.exec_command(f"docker start {container_name}")
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            st.error(error)
                        else:
                            st.success(f"✅ Started: {container_name}")

                with col2:
                    if st.button("⏹️ Stop Container") and container_name:
                        stdin, stdout, stderr = ssh.exec_command(f"docker stop {container_name}")
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            st.error(error)
                        else:
                            st.success(f"✅ Stopped: {container_name}")

                with col3:
                    if st.button("📊 List Containers"):
                        stdin, stdout, stderr = ssh.exec_command("docker ps -a")
                        result = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            st.error(error)
                        else:
                            st.code(result)

            with tab3:
                st.markdown("### 📝 Dockerfile Generator")
                col1, col2 = st.columns(2)
                with col1:
                    base_image = st.selectbox("🏗️ Base Image", ["python:3.9", "node:16", "nginx:alpine", "ubuntu:20.04", "alpine:latest"])
                    app_type = st.selectbox("📱 Application Type", ["Python Flask", "Node.js Express", "Static Website", "Custom"])
                    port = st.number_input("🔌 Expose Port", value=8000)
                with col2:
                    workdir = st.text_input("📁 Working Directory", value="/app")
                    copy_files = st.text_input("📋 Files to Copy", value=". .")
                    run_command = st.text_input("🚀 Run Command", value="python app.py")

                if st.button("🔨 Generate Dockerfile"):
                    dockerfile_content = f"""FROM {base_image}

    WORKDIR {workdir}

    COPY {copy_files}

    RUN apt-get update && apt-get install -y \\
        curl \\
        && rm -rf /var/lib/apt/lists/*

    EXPOSE {port}

    CMD [\"{run_command.split()[0]}\", \"{' '.join(run_command.split()[1:])}\"]
    """
                    st.code(dockerfile_content, language="dockerfile")
                    st.download_button("📥 Download Dockerfile", dockerfile_content, file_name="Dockerfile")
                ssh.close()
        except Exception as e:
            st.error(f"❌ Execution failed: {e}")
    else:
        st.error("❌ Please fill in all connection details")

# AI Prompt Engineer
elif menu_option == "🤖 AI Prompt Engineer":
    st.markdown("## 🤖 AI-Powered Prompt Engineer")
    
    # Gemini AI configuration
    st.sidebar.markdown("### 🔧 AI Configuration")
    api_key = st.sidebar.text_input("🔑 Gemini API Key", type="password", 
                                   help="Enter your Google Gemini API key")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    user_prompt = st.text_area("💬 Enter your prompt", placeholder="Pull the docker image of python\nMake a dockerfile for a Flask application\nShow me Linux commands for file permissions", height=150)

    col1, col2 = st.columns([3, 1])

    with col1:
        execute_clicked = st.button("🚀 Execute AI Prompt", disabled=not api_key)

    if execute_clicked and user_prompt and api_key:
        with st.spinner("🧠 AI is processing your request..."):
            try:
                analysis_prompt = f'''
                Analyze this user prompt and determine what action should be taken:
                "{user_prompt}"

                Respond in JSON format with:
                {{
                    "action_type": "docker_pull|docker_build|dockerfile_create|linux_command|general_help",
                    "command": "the exact command to execute",
                    "explanation": "brief explanation of what will be done",
                    "parameters": {{"key": "value pairs of relevant parameters"}}
                }}
                '''

                response = model.generate_content(analysis_prompt)
                try:
                    ai_analysis = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
                except:
                    ai_analysis = {
                        "action_type": "general_help",
                        "command": "",
                        "explanation": "Providing general assistance",
                        "parameters": {}
                    }

                st.markdown(f"""
                <div class="ai-response">
                    <h4>🤖 AI Analysis</h4>
                    <p><strong>Action:</strong> {ai_analysis.get('action_type')}</p>
                    <p><strong>Explanation:</strong> {ai_analysis.get('explanation')}</p>
                </div>
                """, unsafe_allow_html=True)

                command = ai_analysis.get('command', '')
                if ai_analysis['action_type'] == 'linux_command' and command:
                    st.markdown("### 💻 Executing Linux Command")
                    st.info(f"Command: `{command}`")
                    run_cmd = st.button("▶️ Execute on Remote")
                    if run_cmd:
                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
                            stdin, stdout, stderr = ssh.exec_command(command)
                            output = stdout.read().decode()
                            error = stderr.read().decode()

                            if output:
                                st.markdown(f"<pre>{output}</pre>", unsafe_allow_html=True)
                            if error:
                                st.markdown(f"<pre style='color:red;'>{error}</pre>", unsafe_allow_html=True)
                            ssh.close()
                        except Exception as e:
                            st.error(f"❌ SSH execution error: {str(e)}")

                elif ai_analysis['action_type'] == 'docker_pull' and command:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
                        stdin, stdout, stderr = ssh.exec_command(command)
                        output = stdout.read().decode()
                        error = stderr.read().decode()
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.success("✅ Docker image pulled via SSH")
                            st.code(output)
                        ssh.close()
                    except Exception as e:
                        st.error(f"❌ SSH error: {str(e)}")

                elif ai_analysis['action_type'] == 'dockerfile_create':
                    dockerfile_prompt = f"Create a Dockerfile based on this request: {user_prompt}"
                    dockerfile_response = model.generate_content(dockerfile_prompt)
                    dockerfile_content = dockerfile_response.text.strip()
                    st.markdown("### 📝 Generated Dockerfile")
                    st.code(dockerfile_content, language="dockerfile")
                    st.download_button("📅 Download Dockerfile", data=dockerfile_content, file_name="Dockerfile", mime="text/plain")

                else:
                    general_response = model.generate_content(user_prompt)
                    st.markdown(f"""
                    <div class="ai-response">
                        <h4>🤖 AI Response</h4>
                        <p>{general_response.text}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.session_state.ai_history.append({
                    'prompt': user_prompt,
                    'response': ai_analysis,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            except Exception as e:
                st.error(f"❌ AI processing failed: {str(e)}")

    with col2:
        if st.button("📚 Show AI History"):
            if st.session_state.ai_history:
                st.markdown("### 📚 Recent AI Interactions")
                for i, interaction in enumerate(reversed(st.session_state.ai_history[-3:])):
                    st.markdown(f"""
                    <div class="ai-response">
                        <strong>#{len(st.session_state.ai_history)-i}:</strong> {interaction['prompt'][:50]}...<br>
                        <small>{interaction['timestamp']}</small>
                    </div>
                    """, unsafe_allow_html=True)

    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🐍 Python Docker"):
            st.text_area("Auto-generated prompt:", "Pull the docker image of python:3.9-slim", key="python_docker")

    with col2:
        if st.button("🌐 Node.js Setup"):
            st.text_area("Auto-generated prompt:", "Create a dockerfile for a Node.js Express application", key="nodejs_setup")

    with col3:
        if st.button("🐧 Linux Commands"):
            st.text_area("Auto-generated prompt:", "Show me essential Linux commands for system administration", key="linux_commands")

    with col4:
        if st.button("📊 System Info"):
            st.text_area("Auto-generated prompt:", "Display system information and resource usage", key="system_info")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🚀 DevOps Multi-Tool Platform | Built with Streamlit & AI | 
    <a href="#" style="color: #667eea;">Documentation</a> | 
    <a href="#" style="color: #667eea;">Support</a>
</div>
""", unsafe_allow_html=True)