package main

import (
	"fmt"
	"os"
	"strconv"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

func main(){

	if len(os.Args) < 4 {
		fmt.Printf("%s bucket file\n",os.Args[0])
		os.Exit(-1)
	}

	bucket := os.Args[1]
	fname  := os.Args[2]
	copies,err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Errorf("failed to parse argument %v",err)
		os.Exit(-1)
	}

	sess := session.Must(session.NewSession())
	uploader := s3manager.NewUploader(sess)
	f, err := os.Open(fname)
	if err != nil {
		fmt.Errorf("failed to open file %q %v",fname,err)
		os.Exit(-1)
	}

	res, err := uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(fname),
		Body:   f,
	})
	if err != nil {
		fmt.Errorf("failed to upload file %v",err)
		os.Exit(-1)
	}
	fmt.Printf("file uploaded to, %s\n", aws.StringValue(&res.Location))

	svc := s3.New(sess)
	for i := 0; i<copies; i++ {
		input := &s3.CopyObjectInput{
			Bucket: aws.String(bucket),
			CopySource: aws.String(fname),
			Key: aws.String(fmt.Sprintf("%d-%s",fname,i)),
		}

		res, err := svc.CopyObject(input)
		if err != nil {
			fmt.Errorf("failed to copy file %v",err)
			os.Exit(-1)
		}
		fmt.Println(res)
	}

}

