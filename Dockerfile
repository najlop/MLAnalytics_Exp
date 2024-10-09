# To build locally:
# docker build . -t flask
# docker run --name flask -p 8501:8501 -p 2222:2222 -v ./lightcurveruntime:/lightcurveruntime --rm flask

FROM mambaorg/micromamba:1.5.9

USER root

WORKDIR /app/

# possibly with --chown=$MAMBA_USER:$MAMBA_USER
# TODO: what folders actually need to be copied?
COPY --chown=$MAMBA_USER:$MAMBA_USER ArielGPT ArielGPT
COPY --chown=$MAMBA_USER:$MAMBA_USER entrypoint.sh .
COPY --chown=$MAMBA_USER:$MAMBA_USER app.py .

# TODO: review packages
COPY --chown=$MAMBA_USER:$MAMBA_USER environment_fromhistory.yml .

RUN micromamba create -c conda-forge -n arielgpt python=3.11 && \
    micromamba install --yes --file environment_fromhistory.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  # (otherwise python will not be found)


# Install curl using apt (Debian-based images)
# https://learn.microsoft.com/en-us/azure/app-service/configure-custom-container?tabs=debian&pivots=container-linux#enable-ssh
# Start and enable SSH
RUN apt-get update \
&& apt-get install -y --no-install-recommends sudo \
&& apt-get install -y --no-install-recommends dialog \
&& apt-get install -y --no-install-recommends openssh-server \
&& echo "root:Docker!" | chpasswd \
&& chmod u+x /app/entrypoint.sh

# Azure SSH config
COPY sshd_config /etc/ssh/

RUN echo ${MAMBA_USER}" ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch back to the default non-root user (micromamba user)
USER $MAMBA_USER

# Expose streamlit and SSH ports
EXPOSE 8501 2222

ENTRYPOINT [ "./entrypoint.sh" ]
