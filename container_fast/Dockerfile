FROM ubuntu:latest

USER root

RUN apt update && \
  apt-get install -y wget && \
  apt install -y curl && \
  apt install unzip && \
  wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh && \
  bash /Miniconda3-py310_23.3.1-0-Linux-x86_64.sh -b && \
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
  ls && \
  unzip awscliv2.zip && \
  ./aws/install

ENV PATH /root/miniconda3/bin:$PATH

RUN conda create -n openfast_env -y && \
    conda install -c conda-forge openfast=3.5.0 -y

COPY openfast /openfast/

WORKDIR /openfast/

CMD ["./process_wrapper_first_fleet.sh"]