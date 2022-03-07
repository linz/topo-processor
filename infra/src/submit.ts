import * as sdk from 'aws-sdk';
import * as ulid from 'ulid';
import CloudFormation from 'aws-sdk/clients/cloudformation.js';

const batch = new sdk.Batch();

const cloudFormation = new CloudFormation({ region: 'ap-southeast-2' });

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const stackInfo = await cloudFormation.describeStacks({ StackName: 'TopoProcessorBatch' }).promise();
  const stackOutputs = stackInfo.Stacks?.[0].Outputs;

  const JobDefinitionArn = stackOutputs?.find((f) => f.OutputKey === 'BatchJobArn')?.OutputValue;
  if (JobDefinitionArn == null) throw new Error('Unable to find CfnOutput "BatchJobArn"');
  const JobQueueArn = stackOutputs?.find((f) => f.OutputKey === 'BatchQueueArn')?.OutputValue;
  if (JobQueueArn == null) throw new Error('Unable to find CfnOutput "BatchQueueArn"');
  const TempBucketName = stackOutputs?.find((f) => f.OutputKey === 'TempBucketName')?.OutputValue;
  if (TempBucketName == null) throw new Error('Unable to find CfnOutput "TempBucketName"');

  const environment = [
    { name: 'AWS_DEFAULT_REGION', value: 'ap-southeast-2' },
    { name: 'LINZ_CACHE_BUCKET', value: 'linz-lds-cache' },
    { name: 'LINZ_CORRELATION_ID', value: correlationId },
    { name: 'LINZ_HISTORICAL_IMAGERY_BUCKET', value: 'linz-historical-imagery-staging' },
    { name: 'LINZ_SSM_BUCKET_CONFIG_NAME', value: 'BucketConfig' },
  ];

  for (let jobId = 0; jobId < 1; jobId++) {
    const res = await batch
      .submitJob({
        jobName: ['Job', correlationId, jobId].join('-'),
        jobQueue: JobQueueArn,
        jobDefinition: JobDefinitionArn,
        containerOverrides: {
          resourceRequirements: [{ type: 'MEMORY', value: '3600' }],

          command: buildCommandArguments(correlationId, TempBucketName),
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}

// TODO: historical imagery input source

function buildCommandArguments(correlationId: string, tempBucket: string): string[] {
  const command: string[] = [];
  command.push('./upload');
  command.push('--correlationid');
  command.push(correlationId);
  command.push('--source');
  command.push('9490');
  command.push('--target');
  command.push('s3://' + tempBucket + '/' + correlationId + '/');
  command.push('--datatype');
  command.push('imagery.historic');
  command.push('-v');

  return command;
}

main().catch(console.error);
