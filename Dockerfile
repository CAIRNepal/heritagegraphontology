FROM ghcr.io/dgarijo/widoco:v1.4.23

# Use root to avoid permission issues
USER 0

# Workdir inside container
WORKDIR /app

# Copy your ontology file into container
COPY HeritageGraph.ttl /input/HeritageGraph.ttl

# Create output folder
RUN mkdir -p /output

# Run Widoco to generate docs
RUN java -jar /widoco/widoco-1.4.23-jar-with-dependencies.jar \
    -ontFile /input/HeritageGraph.ttl \
    -outFolder /output \
    -lang en \
    -rewriteAll \
    -webVowl

# Rename index-en.html → index.html
RUN if [ -f /output/index-en.html ]; then mv /output/index-en.html /output/index.html; fi

# Expose output folder as volume
VOLUME ["/output"]
