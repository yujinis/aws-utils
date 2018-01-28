<?php

//  Need to two arguments, s3 and bucket_key
if( count($argv) != 3) {
    exit(-1);
}

// ----- Signature -----
// HTTP-Verb
$httpVerb = 'GET' . "\n";
 
// Content-MD5
$contentMd5 = "\n";
 
// Content-Type
$contentType = "\n";
 
// Date
$datetime = new DateTime('now', new DateTimeZone('UTC'));
$date = $datetime->format(DateTime::RFC1123) . "\n";
 
// CanonicalizedAmzHeaders
$canonicalizedAmzHeaders = '';

// S3
$s3 = $argv[1];

// Bucket/Key name 
$bucket_key = $argv[2];

// CanonicalizedResource
//$canonicalizedResource = '/';
$canonicalizedResource = $bucket_key;
 
// StringToSign
$stringToSign = $httpVerb . $contentMd5 . $contentType . $date
              . $canonicalizedAmzHeaders . $canonicalizedResource;
 
// Signature
$hash = hash_hmac('sha1', $stringToSign, getenv("AWS_SECRET_KEY_ID"), true);
$signature = base64_encode($hash);

// Authorization
$authorization = 'AWS ' . getenv("AWS_ACCESS_KEY_ID") . ':' . $signature;

print $authorization;
print PHP_EOL;

// ----- HTTP Request -----
// Gets list of buckets.
$ch = curl_init($s3 . $bucket_key );
$headers = array(
    'Authorization: ' . $authorization,
    'Date: ' . $date,
);

curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$body = curl_exec($ch);
curl_close($ch);

print $body;
print PHP_EOL;

?>
