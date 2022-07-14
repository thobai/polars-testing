ARG polars_build_type=pip

#
# Polars from pip
#
FROM python:3.10.4-slim-bullseye as polars_pip
RUN pip3 install polars

#
# Polars from source
#
FROM python:3.10.4-slim-bullseye as polars_source
ENV polars_ver="source"

ENV RUSTUP_HOME=/rust
ENV CARGO_HOME=/cargo 
ENV PATH=/cargo/bin:/rust/bin:$PATH

RUN pip3 install maturin==0.12.18

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ca-certificates \
        curl \
        git \
        ssh \
        libssl-dev \
        pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN echo "(curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly --no-modify-path) && source /cargo/env && rustup default nightly" > /install-rust.sh && \
#    chmod 755 /install-rust.sh

# RUN /install-rust.sh

ADD docker-install-rust.sh /
RUN chmod +x /docker-install-rust.sh ; \
    /docker-install-rust.sh ; 

# RUN git clone https://github.com/pola-rs/polars.git /polars

# RUN echo "Installing polars from source..." && \
#         cd /polars/py-polars && maturin develop --rustc-extra-args="-C target-cpu=native" --release && \
#         pip3 install /polars/py-polars/target/wheels/*manylinux*.whl ;
# RUN rm -rf /polars

#
# General build
#
FROM polars_${polars_build_type}

COPY polars_test.py /
COPY requirements.txt /

RUN pip3 install -r /requirements.txt

CMD /polars_test.py