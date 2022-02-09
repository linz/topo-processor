import * as sdk from 'aws-sdk';
import * as ulid from 'ulid';
import CloudFormation from 'aws-sdk/clients/cloudformation.js';

const batch = new sdk.Batch();

const cloudFormation = new CloudFormation({ region: 'ap-southeast-2' });

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const environment = [{ name: 'LINZ_CORRELATION_ID', value: correlationId }];

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
          resourceRequirements: [
            {
              type: 'MEMORY',
              value: '3600',
            },
          ],
          command: buildCommandArguments(correlationId, BatchEc2InstanceRole, TopoProcessorBucket),
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}

function buildCommandArguments(
  correlationId: string,
  BatchEc2InstanceRole: string,
  TopoProcessorBucket: string,
): string[] {
  console.log({ BatchEc2InstanceRole });
  console.log({ TopoProcessorBucket });

  const command: string[] = [];
  command.push('./upload');
  command.push('--correlationid');
  command.push(correlationId);
  command.push('--source');
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
  command.push('-v');

  return command;
}

main().catch(console.error);
