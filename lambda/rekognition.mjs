import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { RekognitionClient, DetectLabelsCommand } from "@aws-sdk/client-rekognition";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";

const region = process.env.AWS_REGION || 'us-west-1';
const s3Client = new S3Client({ region });
const rekognitionClient = new RekognitionClient({ region });
const dynamoDBClient = new DynamoDBClient({ region });
const tableName = process.env.TABLE_NAME || 'RekognitionResults';

export const handler = async (event) => {
    console.log(`Region: ${region}`);

    try {
        const bucket = event.Records[0].s3.bucket.name;
        const key = event.Records[0].s3.object.key;

        // Get the image from S3
        const getObjectParams = { Bucket: bucket, Key: key };
        const imageObject = await s3Client.send(new GetObjectCommand(getObjectParams));
        const imageBytes = await streamToBuffer(imageObject.Body);

        // Detect labels using Rekognition
        const detectLabelsParams = {
            Image: { Bytes: imageBytes },
            MaxLabels: 10
        };
        const detectLabelsResponse = await rekognitionClient.send(new DetectLabelsCommand(detectLabelsParams));
        const labels = detectLabelsResponse.Labels;

        console.log('detectLabelsParams ',detectLabelsParams);
        console.log('labels ',labels);

        // Store the results in DynamoDB
        const putItemParams = {
            TableName: tableName,
            Item: {
                ImageID: { S: key },
                Labels: { S: JSON.stringify(labels) }
            }
        };
        await dynamoDBClient.send(new PutItemCommand(putItemParams));

        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Image processed successfully', labels: labels })
        };
    } catch (error) {
        console.error('Error processing image:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Error processing image', error: error.message })
        };
    }
};

// Helper function to convert stream to buffer
const streamToBuffer = (stream) => new Promise((resolve, reject) => {
    const chunks = [];
    stream.on('data', (chunk) => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks)));
    stream.on('error', reject);
});