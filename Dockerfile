FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common && \
    apt-get -y --no-install-recommends install gnuradio-dev git cmake build-essential libvolk2-dev pkg-config libbladerf-dev libosmosdr-dev gr-osmosdr
WORKDIR /root/
RUN git clone https://github.com/Nuand/gr-bladeRF
WORKDIR /root/gr-bladeRF/build
RUN cmake .. && make install && ldconfig
COPY freqpuzzle.py /root/freqpuzzle.py
ENTRYPOINT ["/usr/bin/python3", "/root/freqpuzzle.py"]
