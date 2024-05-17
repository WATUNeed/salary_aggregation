docker cp dump/ mongo:dump/
bsondump /dump/sampleDB/sample_collection.bson > collection.json
mongoimport -d sampleDB -c sample_collection --uri="mongodb://user:password@localhost:27017" --authenticationDatabase admin -v < collection.json