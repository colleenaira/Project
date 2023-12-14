FROM quay.io/vgteam/vg:v1.53.0

# Install graphviz
RUN apt-get update && apt-get install -y graphviz
