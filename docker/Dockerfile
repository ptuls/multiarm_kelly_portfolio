FROM jupyter/scipy-notebook

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends pybind11-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_UID

COPY app/requirements.txt /app/requirements.txt

# Upgrade pip and wheel.
# Install requirements using pip, but they get installed to conda's space :D
# Generate a jupyter config then unceremoniously change it to increase the kernel activity timeout.
# Enable notebook extensions.
RUN pip install -U pip wheel && \
    pip install -r /app/requirements.txt && \
    yes | jupyter notebook --generate-config && \
    echo "\nc.MappingKernelManager.kernel_info_timeout = 600\n" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "\nc.NotebookApp.allow_remote_access = True\n" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    jupyter nbextension enable --py widgetsnbextension
