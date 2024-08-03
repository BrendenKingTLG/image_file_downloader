export DATE_TAG=$(date +%Y%m%d)

docker build --no-cache -t osm-downloader:${DATE_TAG} .

CONTAINER_ID=$(docker create osm-downloader:${DATE_TAG})


docker cp ${CONTAINER_ID}:/app/last_downloaded.txt ./last_downloaded.txt

docker rm -v ${CONTAINER_ID}

echo "File last_updates has been copied to the local directory."