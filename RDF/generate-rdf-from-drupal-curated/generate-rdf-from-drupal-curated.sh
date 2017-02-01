declare -a arr_queries=("from-drupal-generate-regions-triples.sparql"
                "from-drupal-generate-license-triples.sparql"
				"from-drupal-generate-languages-triples.sparql"
				"from-drupal-generate-indicators-triples.sparql"
				"from-drupal-generate-datasets&organizations-triples.sparql"
                )
## now loop through the above array
for QUERY_FILE in "${arr_queries[@]}"
do
   echo "Retrieving $QUERY_FILE ..."
   # or do whatever with individual element of the array
   # wget output file
   OUTPUT_FILE=`date +"%Y%m%d"`-$QUERY_FILE.rdf
   # wget log file
   LOG_FILE=`date +"%Y%m%d"`-$QUERY_FILE.log
   # query file
   QUERY=`cat $QUERY_FILE`
   QUERY=$(python -c "import urllib, sys; print urllib.quote(sys.argv[1])"  "$QUERY")
   URL="http://landportal.info/sparql?default-graph-uri=&query=$QUERY&should-sponge=&format=application%2Frdf%2Bxml&timeout=0&debug=on"
   wget $URL -O $OUTPUT_FILE -o $LOG_FILE   
   ./clean-tags.sh $OUTPUT_FILE
done
