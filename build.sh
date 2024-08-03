# Determine date range for tagging
export DATE_TAG=$(date +%Y%m%d)

# Build the image
docker build -t osm-downloader:${DATE_TAG} .
docker run --rm -v $(pwd):/app osm-downloader:${DATE_TAG}
