FROM kindest/node:v1.31.4

# We configure the NVIDIA Container Runtime to only trigger on the
# nvidia.cdi.k8s.io annotation and enable CDI in containerd
RUN apt-get update && \
    apt-get install -y gpg && \
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
      curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && \
    apt-get update && \
    apt-get install -y nvidia-container-toolkit && \
    nvidia-ctk config --set nvidia-container-runtime.modes.cdi.annotation-prefixes=nvidia.cdi.k8s.io/ && \
    nvidia-ctk runtime configure --runtime=containerd --set-as-default --cdi.enabled

COPY entrypoint /entrypoint

ENTRYPOINT [ "/entrypoint", "/sbin/init" ]
