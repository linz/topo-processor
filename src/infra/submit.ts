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
          command: ['Job' + jobId],
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}

main().catch(console.error);
