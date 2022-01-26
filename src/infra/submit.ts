import * as sdk from 'aws-sdk';
import * as ulid from 'ulid';

const batch = new sdk.Batch();

const JobDefinitionArn = 'JobDefArnGoesHere';
const JobQueueArn = 'JobQueueArnGoesHere';

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const environment = [{ name: 'LINZ_CORRELATION_ID', value: correlationId }];

  // Your logic to determine what to submit
  
  // TODO Just copied from template
  for (let jobId = 0; jobId < 3; jobId++) {
    const res = await batch
      .submitJob({
        jobName: ['Job', correlationId, jobId].join('-'),
        jobQueue: JobQueueArn,
        jobDefinition: JobDefinitionArn,
        containerOverrides: {
          memory: 128,
          command: buildCommandArguments(),
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}


function buildCommandArguments(correlationId: string, jobName: string, fileList: string[]): string[] {
  const command: string[] = [];
  command.push('--correlation-id');
  command.push(correlationId);
  command.push('--job-name');
  command.push('--aws-read-role');
  // command.push(configuration.roles.read);
  // command.push('--aws-write-role');
  // command.push(configuration.roles.write);
  // command.push('--aws-read-bucket');
  // command.push(configuration.buckets.read);
  // command.push('--aws-write-bucket');
  // command.push(configuration.buckets.write);
  command.push(jobName);
  command.push('--source');
  command.push(fileList.join(';'));
  command.push('--target');
  command.push();
  command.push('--datatype');
  command.push();

  return command;
}

main().catch(console.error);
