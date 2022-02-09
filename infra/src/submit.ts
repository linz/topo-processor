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
  ];

  const stackInfo = await cloudFormation.describeStacks({ StackName: 'Batch' }).promise();
  const stackOutputs = stackInfo.Stacks?.[0].Outputs;

  const JobDefinitionArn = stackOutputs?.find((f) => f.OutputKey === 'BatchJobArn')?.OutputValue;
  if (JobDefinitionArn == null) throw new Error('Unable to find CfnOutput "BatchJobArn"');
  const JobQueueArn = stackOutputs?.find((f) => f.OutputKey === 'BatchQueueArn')?.OutputValue;
  if (JobQueueArn == null) throw new Error('Unable to find CfnOutput "BatchQueueArn"');
  const BatchEc2InstanceRole = stackOutputs?.find((f) => f.OutputKey === 'BatchEc2InstanceRole')?.OutputValue;
  if (BatchEc2InstanceRole == null) throw new Error('Unable to find CfnOutput "BatchEc2InstanceRole"');
  const TopoProcessorBucket = stackOutputs?.find((f) => f.OutputKey === 'TopoProcessorBucket')?.OutputValue;
  if (TopoProcessorBucket == null) throw new Error('Unable to find CfnOutput "TopoProcessorBucket"');

  const stackInfo = await cloudFormation.describeStacks({ StackName: 'Batch' }).promise();
  const stackOutputs = stackInfo.Stacks?.[0].Outputs;

  const JobDefinitionArn = stackOutputs?.find((f) => f.OutputKey === 'BatchJobArn')?.OutputValue!;
  const JobQueueArn = stackOutputs?.find((f) => f.OutputKey === 'BatchQueueArn')?.OutputValue!;
  const BatchEc2InstanceRole = stackOutputs?.find((f) => f.OutputKey === 'BatchEc2InstanceRole')?.OutputValue!;
  const TopoProcessorBucket = stackOutputs?.find((f) => f.OutputKey === 'TopoProcessorBucket')?.OutputValue!;

  console.log({ JobDefinitionArn });
  console.log({ JobQueueArn });

  // Your logic to determine what to submit

  // TODO Just copied from template
  for (let jobId = 0; jobId < 1; jobId++) {
    const res = await batch
      .submitJob({
        jobName: ['Job', correlationId, jobId].join('-'),
        jobQueue: JobQueueArn,
        jobDefinition: JobDefinitionArn,
        containerOverrides: {
<<<<<<< HEAD
          resourceRequirements: [{ type: 'MEMORY', value: '3600' }],
          command: buildCommandArguments(correlationId, TopoProcessorBucket),
=======
          resourceRequirements: [
            {
              type: 'MEMORY',
              value: '3600',
            },
          ],
          command: buildCommandArguments(correlationId, BatchEc2InstanceRole, TopoProcessorBucket),
>>>>>>> fix: pass CfnOutputs to Topo Processor
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}

<<<<<<< HEAD
function buildCommandArguments(correlationId: string, tempBucket: string): string[] {
=======
function buildCommandArguments(
  correlationId: string,
  BatchEc2InstanceRole: string,
  TopoProcessorBucket: string,
): string[] {
  console.log({ BatchEc2InstanceRole });
  console.log({ TopoProcessorBucket });

>>>>>>> fix: pass CfnOutputs to Topo Processor
  const command: string[] = [];
  command.push('./upload');
  command.push('--correlationid');
  command.push(correlationId);
  command.push('--source');
<<<<<<< HEAD
  command.push('s3://' + tempBucket + '/input/');
  command.push('--target');
  command.push('s3://' + tempBucket + '/output/');
  command.push('--datatype');
  command.push('imagery.historic');
=======
  command.push('s3://' + TopoProcessorBucket + '/input/');
  command.push('--target');
  command.push('s3://' + TopoProcessorBucket + '/output/');
  command.push('--readrole');
  command.push(BatchEc2InstanceRole);
  command.push('--writerole');
  command.push(BatchEc2InstanceRole);
  command.push('--datatype');
  command.push('imagery.historic');
  command.push('--ldscacherole');
  command.push('placeholder');
>>>>>>> fix: pass CfnOutputs to Topo Processor
  command.push('-v');

  return command;
}

main().catch(console.error);
