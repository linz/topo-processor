import * as sdk from 'aws-sdk';
import * as ulid from 'ulid';
import CloudFormation from 'aws-sdk/clients/cloudformation.js';

const batch = new sdk.Batch();

const cloudFormation = new CloudFormation({ region: 'ap-southeast-2' });

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const environment = [
    { name: 'LINZ_CORRELATION_ID', value: correlationId },
    { name: 'LINZ_SSM_BUCKET_CONFIG_NAME', value: 'BucketConfig' },
    { name: 'LINZ_CACHE_BUCKET', value: 'linz-lds-cache' },
    { name: 'AWS_DEFAULT_REGION', value: 'ap-southeast-2' },
  ];

  const stackInfo = await cloudFormation.describeStacks({ StackName: 'TopoProcessorBatch' }).promise();
  const stackOutputs = stackInfo.Stacks?.[0].Outputs;

  const JobDefinitionArn = stackOutputs?.find((f) => f.OutputKey === 'BatchJobArn')?.OutputValue;
  if (JobDefinitionArn == null) throw new Error('Unable to find CfnOutput "BatchJobArn"');
  const JobQueueArn = stackOutputs?.find((f) => f.OutputKey === 'BatchQueueArn')?.OutputValue;
  if (JobQueueArn == null) throw new Error('Unable to find CfnOutput "BatchQueueArn"');
  const TempBucketName = stackOutputs?.find((f) => f.OutputKey === 'TempBucketName')?.OutputValue;
  if (TempBucketName == null) throw new Error('Unable to find CfnOutput "TempBucketName"');

  if (process.argv.length > 2) {
    for (let i = 2; i < process.argv.length; i++) {
      const res = await batch
        .submitJob({
          jobName: ['Job', correlationId].join('-'),
          jobQueue: JobQueueArn,
          jobDefinition: JobDefinitionArn,
          containerOverrides: {
            resourceRequirements: [{ type: 'MEMORY', value: '3600' }],

            command: buildCommandArguments(correlationId, TempBucketName, process.argv[i]),
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
