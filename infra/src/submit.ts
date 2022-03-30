import * as sdk from 'aws-sdk';
import * as ulid from 'ulid';
import CloudFormation from 'aws-sdk/clients/cloudformation.js';

const batch = new sdk.Batch();

const cloudFormation = new CloudFormation({ region: 'ap-southeast-2' });

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const environment = [
    { name: 'AWS_DEFAULT_REGION', value: 'ap-southeast-2' },
    { name: 'LINZ_CACHE_BUCKET', value: 'linz-lds-cache' },
    { name: 'LINZ_CORRELATION_ID', value: correlationId },
    { name: 'LINZ_HISTORICAL_IMAGERY_BUCKET', value: 'linz-historical-imagery-staging' },
    { name: 'LINZ_SSM_BUCKET_CONFIG_NAME', value: 'BucketConfig' },
  ];

  const stackInfo = await cloudFormation.describeStacks({ StackName: 'TopoProcessorBatch' }).promise();
  const stackOutputs = stackInfo.Stacks?.[0].Outputs;

  const jobDefinitionArn = stackOutputs?.find((f) => f.OutputKey === 'BatchJobArn')?.OutputValue;
  if (jobDefinitionArn == null) throw new Error('Unable to find CfnOutput "BatchJobArn"');
  const jobQueueArn = stackOutputs?.find((f) => f.OutputKey === 'BatchQueueArn')?.OutputValue;
  if (jobQueueArn == null) throw new Error('Unable to find CfnOutput "BatchQueueArn"');
  const tempBucketName = stackOutputs?.find((f) => f.OutputKey === 'TempBucketName')?.OutputValue;
  if (tempBucketName == null) throw new Error('Unable to find CfnOutput "TempBucketName"');
  const tempBucketReadRole = stackOutputs?.find((f) => f.OutputKey === 'LINZRoleReadArn')?.OutputValue;
  if (tempBucketReadRole == null) throw new Error('Unable to find CfnOutput "LINZRoleReadArn"');

  if (process.argv.length > 2) {
    for (let i = 2; i < process.argv.length; i++) {
      const res = await batch
        .submitJob({
          jobName: ['Job', correlationId].join('-'),
          jobQueue: jobQueueArn,
          jobDefinition: jobDefinitionArn,
          containerOverrides: {
            resourceRequirements: [{ type: 'MEMORY', value: '3600' }],
            command: buildCommandArguments(correlationId, tempBucketName, process.argv[i]),
            environment,
          },
        })
        .promise();
      console.log({ source: process.argv[i] }, '\n', res);
    }
  } else {
    console.log(
      'You need to provide a source (a list of S3 bucket folders or a list of survey ID to process. Check the README for more information.',
    );
  }
}

function buildCommandArguments(correlationId: string, tempBucket: string, source: string): string[] {
  const command: string[] = [];
  command.push('./upload');
  command.push('--correlationid');
  command.push(correlationId);
  command.push('--source');
  command.push(source);
  command.push('--target');
  command.push('s3://' + tempBucket + '/' + correlationId + '/');
  command.push('--datatype');
  command.push('imagery.historic');
  command.push('-v');

  return command;
}

main().catch(console.error);
