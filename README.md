# SentenceSplit-Microservice
API for sentence splitting: https://kyhk5y2ub3.execute-api.us-west-2.amazonaws.com/dev

## Usage
- The API accepts only `POST` requests, expects `JSON` input and produces `JSON` output.
- Make sure to also provide some value for `x-access-token` header, otherwise the access will be forbidden (ask the administrators for a valid token).
- The request body should contain `text` key with some string to split, then the response body will be a list of corresponding sentences.
