package main

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"os"
)

func CreateInput(id, time int) *dynamodb.UpdateItemInput {
	input := &dynamodb.UpdateItemInput{
		TableName: aws.String("dynamo-yujinis"),

		Key: map[string]*dynamodb.AttributeValue{
			"id": {
				N: aws.String(fmt.Sprintf("%d", id)),
			},
			"time": {
				N: aws.String(fmt.Sprintf("%d", time)),
			},
		},

		ReturnConsumedCapacity:      aws.String("INDEXES"),
		ReturnItemCollectionMetrics: aws.String("SIZE"),
		ReturnValues:                aws.String("ALL_NEW"),
	}
	return input
}

func main() {
	fmt.Println("aws-sdk-go")

	os.Setenv("AWS_PROFILE", "/Users/yujinis/.aws/credentials")

	sess, _ := session.NewSession(&aws.Config{
		Region:      aws.String("ap-northeast-1"),
		Credentials: credentials.NewSharedCredentials("", "default"),
	})

	ddb := dynamodb.New(sess)
	for i := 0; i < 100; i++ {
		res, err := ddb.UpdateItem(CreateInput(i, i*2000))
		if err != nil {
			panic(err.Error())
		}
		fmt.Println(res)
	}

}
