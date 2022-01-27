import * as sdk from "aws-sdk";
import * as ulid from "ulid";

const batch = new sdk.Batch();

const JobDefinitionArn = "";
const JobQueueArn = "";

async function main(): Promise<void> {
  const correlationId = ulid.ulid();
  console.log({ correlationId });

  const environment = [{ name: "LINZ_CORRELATION_ID", value: correlationId }];

  // Your logic to determine what to submit

  // TODO Just copied from template
  for (let jobId = 0; jobId < 1; jobId++) {
    const res = await batch
      .submitJob({
        jobName: ["Job", correlationId, jobId].join("-"),
        jobQueue: JobQueueArn,
        jobDefinition: JobDefinitionArn,
        containerOverrides: {
          resourceRequirements: [
            {
              type: "MEMORY",
              value: "512",
            },
          ],
          command: buildCommandArguments(correlationId),
          environment,
        },
      })
      .promise();

    console.log(res);
  }
}

function buildCommandArguments(correlationId: string) {
  const command: string[] = [];
  // command.push('./validate')
  command.push("./upload");
  command.push("--correlationid");
  command.push(correlationId);
  // command.push('--job-name');
  // command.push(jobName);
  command.push("--source");
  command.push(
    "s3://linz-historical-imagery-staging/backup9/Supplied Films/CROWN_1124/"
  );
  command.push("--target");
  command.push("s3://megantestbucket/test-tp-batch/");
  command.push("--datatype");
  command.push("imagery.historic");
  command.push("-v");

  return command;
}

main().catch(console.error);
